#############################################################################
# Makefile                                                                  #
#############################################################################

target:rpm

include $(CURR_DIR)/src/com_inc/make_inc.mk

LIBS += -lutLib -lpthread -lrt

LFLAGS += -L$(COM_LIB_DIR)

vpath %.c $(SRC_DIR)

CPACKGEN_RPM = $(RPM_DIR)/cpackgen*.rpm
CPACKGEN=$(BIN_DIR)/cpackgen.exe

SRC_FILES := $(shell $(OF_CMD))
OBJS = $(addprefix $(OBJ_DIR)/, $(SRC_FILES:.c=.o))

-include $(OBJS:.o=.d)

$(CPACKGEN):$(OBJS)
$(CPACKGEN_RPM): $(CPACKGEN)

rpm:$(CPACKGEN_RPM)

#############################################################################
