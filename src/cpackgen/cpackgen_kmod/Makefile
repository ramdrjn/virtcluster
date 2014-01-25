#############################################################################
# Makefile                                                                  #
#############################################################################

#Specify this as a kernel makefile
KERNEL_MAKEFILE=yes

target:rpm

include $(CURR_DIR)/src/com_inc/make_inc.mk

CPACKGEN_KMOD_RPM = $(RPM_DIR)/cpackgen_kmod*.rpm

$(CPACKGEN_KMOD_RPM):kmod

rpm:$(CPACKGEN_KMOD_RPM)

#############################################################################
