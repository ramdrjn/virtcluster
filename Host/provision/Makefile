#############################################################################
# Makefile                                                                  #
#############################################################################

target:rpm

include $(CURR_DIR)/Host/com_inc/make_inc.mk

vpath %.c $(SRC_DIR)

PROVISION_RPM = $(RPM_DIR)/provision*.rpm

provision:../../inc/scripts/py/cli_fmwk.py ../../inc/scripts/py/common.py
	cp ../../inc/scripts/py/cli_fmwk.py ./common/cli_fmwk.py
	cp ../../inc/scripts/py/common.py ./common/common.py
	/usr/bin/python3 com_setup.py bdist
	rm -v ./common/cli_fmwk.py
	rm -v ./common/common.py
	rm -vrf ./build
	/usr/bin/python3 prov_setup.py bdist
	rm -vrf ./build

$(PROVISION_RPM):provision

rpm:$(PROVISION_RPM)

#############################################################################
