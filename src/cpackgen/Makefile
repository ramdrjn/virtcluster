#############################################################################
# Makefile                                                                  #
#############################################################################

target:all

.PHONY:cpackgen-cli
cpackgen-cli:
	$(MAKE) -C ./cpackgen-cli/ $(TARGET)

.PHONY:cpackgen
cpackgen:
	$(MAKE) -C ./cpackgen/ $(TARGET)

.PHONY:cpackgen_kmod
cpackgen_kmod:
	$(MAKE) -C ./cpackgen_kmod/ $(TARGET)

all:cpackgen cpackgen_kmod cpackgen-cli

##############################################################################
