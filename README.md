# MindTheGapps Minimal (Android 17)

> [!IMPORTANT]
> **Personal Project**: This repository is an independent, customized personal project. It is not affiliated with, maintained by, or endorsed by Google LLC or the official MindTheGapps organization.

A lightweight, de-bloated Google Apps (GApps) package for modern **Android 17 (API 37)** systems. It strips unnecessary telemetry, background surveillance, and heavy bloatware while integrating official Google Pixel telephony apps (**Phone**, **Messages with native RCS**, and **Contacts**) extracted directly from official Google Pixel OTAs.

---

## What Apps Are Included

| Component / Module | Package Name | Partition | Purpose / Details |
| :--- | :--- | :--- | :--- |
| **`PrebuiltGmsCoreVic`** | `com.google.android.gms` | `product/apex` | **Google Play Services** (modern APEX mainline module). Core runtime for authentication, Push (FCM), location, and integrity. |
| **`Phonesky`** | `com.android.vending` | `product/priv-app` | **Google Play Store**. Application management, updates, and licensing. |
| **`GoogleServicesFramework`** | `com.google.android.gsf` | `system_ext/priv-app` | **Google Services Framework (GSF)**. Device check-in and cloud messaging ID. |
| **`GoogleDialer`** | `com.google.android.dialer` | `product/priv-app` | **Google Phone**. Official Pixel dialer with spam caller ID, in-call UI, and satellite telephony hooks. *(Overrides AOSP `Dialer`)*. |
| **`PrebuiltBugle`** | `com.google.android.apps.messaging` | `product/priv-app` | **Google Messages**. Official Pixel SMS/MMS client with **built-in Jibe RCS support**. *(Overrides AOSP `Mms`, `messaging`)*. |
| **`GoogleContacts`** | `com.google.android.contacts` | `product/app` | **Google Contacts**. Full modern contact manager with native account sync. *(Overrides AOSP `Contacts`)*. |
| **`SetupWizard`** | `com.google.android.setupwizard` | `system_ext/priv-app` | **Google Setup Wizard**. First-boot account provisioning and biometric setup. *(Overrides AOSP `Provision`)*. |
| **`GoogleRestore`** | `com.google.android.apps.restore` | `product/priv-app` | **Cloud Backup & Restore**. Device-to-device migration and cloud state restoration. |
| **`GooglePartnerSetup`** | `com.google.android.partnersetup` | `product/priv-app` | **Partner Setup**. Carrier network and partner configuration. |
| **`GoogleCalendarSyncAdapter`** | `com.google.android.syncadapters.calendar` | `product/app` | Sync adapter for AOSP Calendar. |

### Supporting Overlays & Libraries
* **`com.google.android.dialer.support.jar`**: Telephony support framework required for Google Dialer compatibility on custom ROMs.
* **`libjni_latinimegoogle.so`**: Native library providing gesture/swype typing for AOSP Latin keyboard.
* **Runtime Resource Overlays (RROs)**:
  * `GmsOverlay`: Sets framework default roles (Assistant, Credential Manager, Speech).
  * `GmsSettingsOverlay`: Integrates Nearby and Bluetooth settings slices.
  * `GmsSettingsProviderOverlay`: Configures Google Backup Transport as default.
  * `GmsSetupWizardOverlay`: Enables Material You dynamic theming in Setup Wizard.

---

## What Was Removed (De-bloating & Privacy)

The following components from standard GApps packages were purged to save storage, battery, and memory:

* ❌ **`VelvetTitan` (~396 MB)**: Google Pixel Tablet app (unneeded on mobile devices).
* ❌ **`SpeechServicesByGoogle` (~72 MB)**: Text-to-speech engine (can be downloaded from Play Store if needed).
* ❌ **`talkback` (~42 MB)**: Android Accessibility Suite screen reader (downloadable from Play Store).
* ❌ **`FamilyLinkParentalControls` (~30 MB)**: Parental monitoring and child account supervision.
* ❌ **`Wellbeing` (~25 MB)**: Digital Wellbeing screen time tracking.
* ❌ **`AndroidAutoStub` (~4 MB)**: Auto projection handshake (downloads dynamically when connected to a car).
* ❌ **`GoogleFeedback` (~0.5 MB)**: System crash and ANR bug telemetry reporter.
* ❌ **`PrebuiltExchange3Google` (~0.5 MB)**: Obsolete Exchange adapter from Android 6.0.
* ❌ **`GoogleContactsSyncAdapter` (~1.5 MB)**: Redundant (native sync handled by Google Contacts).

---

## How to Build Flashable Packages

### 1. In the Cloud (GitHub Actions)
1. Fork or push this repository to GitHub.
2. Go to **Actions** → **Build GApps** → click **Run workflow**.
3. Download the signed flashable recovery zips from the Actions Artifacts page.

### 2. Locally
Ensure `python3`, `make`, and `openjdk-17` (or newer) are in your `PATH`:
```bash
# Clean previous builds
make distclean

# Build signed flashable recovery package for ARM64
make gapps_arm64

# Output zip will be generated in:
out/MindTheGapps-17.0.0-arm64-*.zip
```

### 3. Inline AOSP ROM Compilation
To bundle this package directly inside an AOSP / LineageOS ROM source tree:
1. Clone this repository into your ROM source:
   ```bash
   git clone https://github.com/nithishlabs08/mind_gapps_minimal.git vendor/gapps
   ```
2. In your device's `device.mk` or ROM configuration, include:
   ```make
   $(call inherit-product, vendor/gapps/arm64/arm64-vendor.mk)
   ```

---

## Credits & Acknowledgments
* Based on the [MindTheGapps](https://gitlab.com/MindTheGapps/vendor_gapps) architecture and build tools.
* Official Pixel 8 Vanilla Ice Cream telephony blobs sourced directly from Google OTA images (`dl.google.com`).
