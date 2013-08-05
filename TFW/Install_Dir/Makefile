include $(CURR_DIR)/TFW/inc/make_inc.mk

TEST_BIN_RPM = $(RPM_DIR)/test_bin*.rpm

EXE_LIST=$(shell find . -iname "*.exe" |xargs)

$(TEST_BIN_RPM):$(EXE_LIST)

rpm:$(TEST_BIN_RPM)
