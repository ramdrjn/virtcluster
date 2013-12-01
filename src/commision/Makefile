#############################################################################
# Makefile                                                                  #
#############################################################################

target:rpm

include $(CURR_DIR)/src/com_inc/make_inc.mk

vpath %.c $(SRC_DIR)

COMMISION_RPM = $(RPM_DIR)/commision*.rpm

.PHONY:commision
commision:../../inc/scripts/py/cli_fmwk.py ../../inc/scripts/py/common.py
	cp ../../inc/scripts/py/cli_fmwk.py ./common/cli_fmwk.py
	cp ../../inc/scripts/py/common.py ./common/common.py
	rm -vrf ./build
	/usr/bin/python3 com_setup.py bdist
	rm -v ./common/cli_fmwk.py
	rm -v ./common/common.py
	rm -vrf ./build
	/usr/bin/python3 commision_setup.py bdist
	rm -vrf ./build

$(COMMISION_RPM):commision

rpm:$(COMMISION_RPM)

#############################################################################
