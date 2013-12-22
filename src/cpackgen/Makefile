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

all:cpackgen cpackgen-cli

##############################################################################
