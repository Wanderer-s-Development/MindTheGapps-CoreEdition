# Removed Applications List

This list documents all proprietary applications and telemetry components removed from upstream **MindTheGapps** to maintain the minimal, lightweight footprint of **MindTheGapps-CoreEdition**.

If upstream reintroduces these components in a future pull/merge, refer to this list to remove them:

---

## 1. Application Directories to Remove

### Google App (Velvet)
- `arm/proprietary/product/priv-app/Velvet`
- `arm64/proprietary/product/priv-app/Velvet`
- `arm64/proprietary/product/priv-app/VelvetTitan`

### Speech Services (TTS)
- `arm/proprietary/product/app/SpeechServicesByGoogle`
- `arm64/proprietary/product/app/SpeechServicesByGoogle`

### Accessibility Suite
- `arm/proprietary/product/app/talkback`
- `arm64/proprietary/product/app/talkback`

### Parental Controls
- `arm/proprietary/product/priv-app/FamilyLinkParentalControls`
- `arm64/proprietary/product/priv-app/FamilyLinkParentalControls`

### Telemetry & Digital Wellbeing
- `common/proprietary/product/priv-app/Wellbeing`
- `common/proprietary/product/etc/sysconfig/wellbeing.xml`
- `common/proprietary/system_ext/priv-app/GoogleFeedback`

### Stubs & Legacy Protocols
- `common/proprietary/product/priv-app/AndroidAutoStub`
- `common/proprietary/product/app/PrebuiltExchange3Google`

---

## 2. Proprietary File List Entries to Remove

When upstream updates, check the following files and remove any lines referencing the apps above:
- `proprietary-files-arm.txt`
- `proprietary-files-arm64.txt`
- `proprietary-files-common.txt`
- `proprietary-files-arm-nongrouper.txt` (if present)
- `proprietary-files-arm64-nongrouper.txt` (if present)
- `proprietary-files-common-nongrouper.txt` (if present)

*(After editing the txt files, run `python3 setup-makefiles.py` to regenerate `Android.bp` and `*-vendor.mk`)*.
