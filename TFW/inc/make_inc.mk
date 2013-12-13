#############################################################################
# Makefile                                                                  #
#############################################################################

include $(CURR_DIR)/inc/make_inc.mk

LIBS += -lutLib -lpthread -lrt

OBJ_DIR := ./
SRC_DIR := ./
BIN_DIR := ./
MAIN_SRC_DIR := $(CURR_DIR)/src
COMMON_OBJ := $(CURR_DIR)/TFW/src/common/common.o
INSTALL_DIR := $(CURR_DIR)/TFW/Install_Dir
INCLUDE += -I$(CURR_DIR)/TFW/inc/ -I$(MAIN_SRC_DIR)
DEFINES =

ifeq ($(LIBTYPE),static)
	LFLAGS += -L$(MAIN_SRC_DIR)/com_lib/static/
	ifeq ($(STATIC_LIB_GCOV),yes)
		LIBS += -lgcov
	endif
else
	LFLAGS += -L$(MAIN_SRC_DIR)/com_lib/
endif

%.o: %.c
	$(COMPILE.o) $(filter-out %.h, $^) $(OUTPUT.o)

.PHONY:tfclean
tfclean:
	rm -vf $(TFILES)

#############################################################################
