# Automatically generated file. DO NOT MODIFY
#

PRODUCT_SOONG_NAMESPACES += \
    vendor/gapps/common

PRODUCT_PACKAGES += \
    GoogleCalendarSyncAdapter \
    GoogleContactsSyncAdapter \
    GooglePartnerSetup \
    GoogleServicesFramework \
    allowed_apex_com.google.android.gmssystem.xml \
    d2d_cable_migration_feature.xml \
    default-permissions-google.xml \
    gms_fsverity_cert.der \
    google-hiddenapi-package-allowlist.xml \
    google.xml \
    privapp-permissions-google-product.xml \
    privapp-permissions-google-system_ext.xml

PRODUCT_PACKAGES += \
    default-permissions-mtg.xml \
    gapps.rc \
    privapp-permissions-mtg.xml \
    sysconfig-mtg.xml

ifeq ($(TARGET_IS_GROUPER),)
PRODUCT_PACKAGES += \
    GoogleRestore
endif

PRODUCT_SOONG_NAMESPACES += \
    vendor/gapps/overlay

PRODUCT_PACKAGES += \
    GmsOverlay \
    GmsSettingsOverlay \
    GmsSettingsProviderOverlay \
    GmsSetupWizardOverlay
