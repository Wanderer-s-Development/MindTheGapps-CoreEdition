# build paths
TOPDIR := .
BUILD_SYSTEM := $(TOPDIR)/build
BUILD_GAPPS := $(BUILD_SYSTEM)/gapps.py
OUTDIR := $(TOPDIR)/out
LOG_BUILD := /tmp/gapps_log

distclean:
	@rm -fr $(OUTDIR)
	@echo "Output removed! Ready for a clean build"

gapps_arm_core:
	@echo "Compiling MindTheGapps Core for arm..."
	@$(BUILD_GAPPS) arm arm core 2>&1

gapps_arm_telephony:
	@echo "Compiling MindTheGapps Telephony for arm..."
	@$(BUILD_GAPPS) arm arm telephony 2>&1

gapps_arm:
	@echo "Compiling MindTheGapps Core and Telephony for arm..."
	@$(BUILD_GAPPS) arm arm both 2>&1

gapps_arm64_core:
	@echo "Compiling MindTheGapps Core for arm64..."
	@$(BUILD_GAPPS) arm64 arm64 core 2>&1

gapps_arm64_telephony:
	@echo "Compiling MindTheGapps Telephony for arm64..."
	@$(BUILD_GAPPS) arm64 arm64 telephony 2>&1

gapps_arm64:
	@echo "Compiling MindTheGapps Core and Telephony for arm64..."
	@$(BUILD_GAPPS) arm64 arm64 both 2>&1

all: gapps_arm64
