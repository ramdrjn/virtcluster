#############################################################################
# Makefile                                                                  #
#############################################################################

target:rpm

include $(CURR_DIR)/src/com_inc/make_inc.mk

CPACKGEN-CLI_RPM = $(RPM_DIR)/cpackgen-cli*.rpm

.PHONY:cpackgen-cli
cpackgen-cli:
	rm -vrf ./build
	/usr/bin/python3 setup.py bdist
	rm -vrf ./build

$(CPACKGEN-CLI_RPM):cpackgen-cli

rpm:$(CPACKGEN-CLI_RPM)

#############################################################################
