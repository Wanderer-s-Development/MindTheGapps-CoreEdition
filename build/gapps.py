#!/usr/bin/env python3
from datetime import datetime, timezone
from pathlib import Path
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import zipfile

ANDROIDV, SDKV = ("17.0.0", 37)

GAPPS_TOP = Path(__file__).resolve().parents[1]
GAPPS_BUILD = GAPPS_TOP / "build"
GAPPS_BUILD_APKTOOL = GAPPS_BUILD / "apktool" / "apktool_3.0.2.jar"
GAPPS_BUILD_META = GAPPS_BUILD / "meta"
GAPPS_BUILD_SIGN = GAPPS_BUILD / "sign"
GAPPS_BUILD_SIGN_APKSIGNER = GAPPS_BUILD_SIGN / "apksigner.jar"
GAPPS_BUILD_SIGN_SIGNAPK = GAPPS_BUILD_SIGN / "signapk.jar"
GAPPS_BUILD_SIGN_TESTKEY = GAPPS_BUILD_SIGN / "testkey"

GAPPS_OUT = GAPPS_TOP / "out"
GAPPS_OVERLAY = GAPPS_TOP / "overlay"

PROPRIETARY_COMMON = GAPPS_TOP / "common" / "proprietary"


def run_command(*args, **kwargs) -> subprocess.CompletedProcess:
    ret = subprocess.run(*args, **kwargs)

    if ret.returncode != 0:
        cmd = " ".join([str(x) for x in ret.args])
        s = f'Failed to run command "{cmd}":\n'
        s += f"stdout:\n{ret.stdout}\n"
        s += f"stderr:\n{ret.stderr}\n"
        raise ValueError(s)

    return ret


def build_package(garch: str, cpuarch: str, variant: str, timestamp: str) -> Path:
    """
    Builds a specific variant: 'core' or 'telephony'.
    Outputs zip as:
      MindTheGapps-{ANDROIDV}-{garch}-Core-{timestamp}.zip
      MindTheGapps-{ANDROIDV}-{garch}-Telephony-{timestamp}.zip
    """
    variant = variant.lower()
    variant_title = "Core" if variant == "core" else "Telephony"
    
    print(f"\n========================================================")
    print(f"Building MindTheGapps {variant_title} for {garch} ({cpuarch})")
    print(f"========================================================")

    out_dir = GAPPS_OUT / f"{garch}_{variant}"
    out_system = out_dir / "system"
    out_metainf = out_dir / "META-INF"
    out_addond = out_system / "addon.d"

    zip_basename = GAPPS_OUT / f"MindTheGapps-{ANDROIDV}-{garch}-{variant_title}-{timestamp}"
    zip_basename_unsigned = Path(f"{zip_basename}-unsigned")
    zip_filename = Path(f"{zip_basename}.zip")
    zip_filename_unsigned = Path(f"{zip_basename_unsigned}.zip")

    # Clean working directory
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_system.mkdir(parents=True, exist_ok=True)

    # 1. Build overlays
    for overlay in GAPPS_OVERLAY.iterdir():
        if not overlay.is_dir():
            continue

        partition = "product"
        with open(overlay / "Android.bp") as f:
            for line in f.readlines():
                if line.endswith("_specific: true\n"):
                    partition, _ = line.strip().split("_specific: true")

        overlay_target_dir = out_system / partition / "overlay"
        overlay_target_dir.mkdir(parents=True, exist_ok=True)
        overlay_target = overlay_target_dir / f"{overlay.name}.apk"

        run_command(
            [
                "java",
                "-Xmx2048m",
                "-jar",
                GAPPS_BUILD_APKTOOL,
                "b",
                overlay,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        with zipfile.ZipFile(overlay_target, "w") as z:
            for src, filename, compress_type in [
                (
                    overlay / "build/apk/resources.arsc",
                    "resources.arsc",
                    zipfile.ZIP_STORED,
                ),
                (
                    overlay / "build/apk/AndroidManifest.xml",
                    "AndroidManifest.xml",
                    zipfile.ZIP_DEFLATED,
                ),
            ]:
                info = zipfile.ZipInfo(filename, (2009, 1, 1, 0, 0, 0))
                info.compress_type = compress_type
                with open(src, "rb") as f:
                    z.writestr(info, f.read())

        run_command(
            [
                "java",
                "-Xmx2048m",
                "-jar",
                GAPPS_BUILD_SIGN_APKSIGNER,
                "sign",
                "--key",
                f"{GAPPS_BUILD_SIGN_TESTKEY}.pk8",
                "--cert",
                f"{GAPPS_BUILD_SIGN_TESTKEY}.x509.pem",
                overlay_target,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if os.path.exists(f"{overlay_target}.idsig"):
            os.remove(f"{overlay_target}.idsig")

    # 2. Copy addon.d scripts
    out_addond.mkdir(parents=True, exist_ok=True)
    shutil.copy2(GAPPS_TOP / "addond_head", out_addond)

    if variant == "core":
        # In Core edition, do NOT remove stock Dialer, Messaging, or Contacts!
        core_addond_tail = """EOF
}

case "$1" in
  backup)
    list_files | while read FILE DUMMY; do
      backup_file $S/$FILE
    done
  ;;
  restore)
    list_files | while read FILE REPLACEMENT; do
      R=""
      [ -n "$REPLACEMENT" ] && R="$S/$REPLACEMENT"
      [ -f "$C/$S/$FILE" ] && restore_file $S/$FILE $R
    done
  ;;
  pre-backup)
    # Stub
  ;;
  post-backup)
    # Stub
  ;;
  pre-restore)
    # Stub
  ;;
  post-restore)
    if [ -e "$S/system_ext/priv-app/SetupWizard" ] || [ -e "$S/priv-app/SetupWizard" ] || [ -e "/system_ext/priv-app/SetupWizard" ]; then
      rm -rf "$S/system_ext/priv-app/Provision"
      rm -rf "$S/priv-app/Provision"
      rm -rf "/system_ext/priv-app/Provision"
    fi
    for i in $(list_files); do
      f=$(get_output_path "$S/$i")
      chown root:root $f
      chmod 644 $f
      chmod 755 $(dirname $f)
    done
  ;;
esac
"""
        with open(out_addond / "addond_tail", "w") as f:
            f.write(core_addond_tail)
    else:
        # Telephony edition retains stock app removal
        shutil.copy2(GAPPS_TOP / "addond_tail", out_addond)

    # 3. Copy META-INF and customize update-binary
    shutil.copytree(GAPPS_BUILD_META, out_metainf, dirs_exist_ok=True)
    update_binary_path = out_metainf / "com" / "google" / "android" / "update-binary"
    if update_binary_path.exists():
        with open(update_binary_path, "r") as f:
            ub_content = f.read()

        if variant == "core":
            # Remove stock app deletion block from update-binary in Core
            ub_content = re.sub(
                r'ui_print "Removing overridden stock apps"[\s\S]*?done',
                '# Stock apps kept in Core edition',
                ub_content
            )
            with open(update_binary_path, "w") as f:
                f.write(ub_content)

    # 4. Copy prebuilts
    proprietary_garch = GAPPS_TOP / garch / "proprietary"
    shutil.copytree(PROPRIETARY_COMMON, out_system, dirs_exist_ok=True)
    if proprietary_garch.exists():
        shutil.copytree(proprietary_garch, out_system, dirs_exist_ok=True)

    # 5. Velvet Removal Safeguard (ensure Velvet never makes it into either edition)
    for velvet_target in [
        out_system / "product" / "priv-app" / "Velvet",
        out_system / "product" / "priv-app" / "VelvetTitan",
    ]:
        if velvet_target.exists():
            shutil.rmtree(velvet_target)

    # 6. Apply variant differences
    if variant == "core":
        print("Configuring Core Edition (removing telephony packages: Dialer, Bugle, Contacts)...")
        telephony_items = [
            out_system / "product" / "priv-app" / "GoogleDialer",
            out_system / "product" / "priv-app" / "PrebuiltBugle",
            out_system / "product" / "app" / "GoogleContacts",
            out_system / "product" / "framework" / "com.google.android.dialer.support.jar",
            out_system / "product" / "etc" / "permissions" / "com.google.android.dialer.support.xml",
        ]
        for item in telephony_items:
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()
    else:
        print("Configuring Telephony Edition (includes Dialer, Bugle, and Contacts)...")

    # 7. Merge split prebuilts
    for first_chunk in glob.glob(
        "**/*.00", root_dir=out_system, recursive=True
    ):
        merged_path = Path(out_system / first_chunk).with_suffix("")
        with open(merged_path, "wb+") as f:
            for chunk in sorted(glob.glob(f"{merged_path}.*")):
                with open(chunk, "rb") as c:
                    shutil.copyfileobj(c, f)
                os.remove(chunk)

    # 8. Copy toybox
    toybox_src = GAPPS_TOP / f"toybox-{garch}"
    if toybox_src.exists():
        shutil.copy2(toybox_src, out_dir / "toybox")

    # 9. Create build.prop
    with open(out_dir / "build.prop", "wt+") as f:
        f.write(f"arch={cpuarch}\n")
        f.write(f"version={SDKV}\n")
        f.write(f"version_nice={ANDROIDV}\n")
        f.write(f"variant={variant}\n")

    # 10. Package archive
    GAPPS_OUT.mkdir(parents=True, exist_ok=True)
    shutil.make_archive(zip_basename_unsigned, "zip", out_dir)

    # 11. Sign archive
    run_command(
        [
            "java",
            "-Xmx2048m",
            "-jar",
            GAPPS_BUILD_SIGN_SIGNAPK,
            "-w",
            f"{GAPPS_BUILD_SIGN_TESTKEY}.x509.pem",
            f"{GAPPS_BUILD_SIGN_TESTKEY}.pk8",
            zip_filename_unsigned,
            zip_filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "LD_LIBRARY_PATH": str(GAPPS_BUILD_SIGN)},
        text=True,
    )
    if zip_filename_unsigned.exists():
        os.remove(zip_filename_unsigned)

    # 12. Generate sha256 checksum file
    sha256_path = GAPPS_OUT / f"{zip_filename.name}.sha256sum"
    with open(sha256_path, "wt+") as f:
        digest = hashlib.file_digest(open(zip_filename, "rb"), "sha256").hexdigest()
        f.write(f"{digest}  {zip_filename.name}\n")

    print(f"Generated: {zip_filename.name} (SHA-256: {digest[:16]}...)")

    # 13. Clean working build directory
    shutil.rmtree(out_dir)

    return zip_filename


def main():
    if len(sys.argv) < 2:
        print("Usage: gapps.py <arm|arm64> [cpuarch] [core|telephony|both]")
        sys.exit(1)

    garch = sys.argv[1]
    cpuarch = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] not in ("core", "telephony", "both", "all") else garch
    
    # Determine variant target
    variant = "both"
    if len(sys.argv) > 2 and sys.argv[2] in ("core", "telephony", "both", "all"):
        variant = sys.argv[2]
    elif len(sys.argv) > 3:
        variant = sys.argv[3]

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

    if variant in ("core", "both", "all"):
        build_package(garch, cpuarch, "core", timestamp)

    if variant in ("telephony", "both", "all"):
        build_package(garch, cpuarch, "telephony", timestamp)


if __name__ == "__main__":
    main()
