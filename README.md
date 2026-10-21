# MindTheGapps (Core & Telephony Editions)

A lightweight MindTheGapps package for **Android 17 (API 37)** featuring two custom builds created automatically on every build:

1. **`MindTheGapps-17.0.0-<arch>-Core-<timestamp>.zip`**:
   Minimal Google Play Services, Play Store, Google Services Framework, and Sync Adapters (`GoogleCalendarSyncAdapter` + `GoogleContactsSyncAdapter`). Leaves stock AOSP Dialer, Messaging, and Contacts untouched!
2. **`MindTheGapps-17.0.0-<arch>-Telephony-<timestamp>.zip`**:
   Core package + official Google Pixel Dialer (call recording/caller ID), Google Messages (native RCS), and Google Contacts app, automatically overriding and purging stock AOSP communication apps.

---

## 📦 Edition Comparison

| Component | Core Package | Telephony Package |
| :--- | :---: | :---: |
| **Google Play Services (APEX)** | ✅ | ✅ |
| **Google Play Store (`Phonesky`)** | ✅ | ✅ |
| **Google Services Framework (`GSF`)** | ✅ | ✅ |
| **Google Setup Wizard** | ✅ | ✅ |
| **Google Calendar Sync Adapter** | ✅ | ✅ |
| **Google Contacts Sync Adapter** | ✅ | ✅ |
| **Google Restore & Partner Setup** | ✅ | ✅ |
| **Google Dialer (`GoogleDialer`)** | ❌ (Keeps Stock) | ✅ (Overrides Stock) |
| **Google Messages (`PrebuiltBugle`)** | ❌ (Keeps Stock) | ✅ (Overrides Stock) |
| **Google Contacts App (`GoogleContacts`)** | ❌ (Keeps Stock) | ✅ (Overrides Stock) |

---

## 🚫 Completely Removed / De-bloated
* ❌ **`Velvet` / `VelvetTitan`**: Google Search app completely removed.
* ❌ **`SpeechServicesByGoogle`** (TTS)
* ❌ **`GoogleFeedback`**
* ❌ **`TalkBack`**
* ❌ **`FamilyLinkParentalControls`**
* ❌ **`Wellbeing`**
* ❌ **`AndroidAutoStub`**
* ❌ **`PrebuiltExchange3Google`**

---

## 🛠️ Building Locally

```bash
# Build both Core and Telephony packages for arm64:
make gapps_arm64

# Build only Core for arm64:
make gapps_arm64_core

# Build only Telephony for arm64:
make gapps_arm64_telephony
```
Output packages and their SHA-256 checksums will be placed in `out/`.
