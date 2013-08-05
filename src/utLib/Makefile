#############################################################################
# Makefile                                                                  #
#############################################################################

target:rpm

include $(CURR_DIR)/src/com_inc/make_inc.mk

vpath %.c $(SRC_DIR)

UTLIB_RPM = $(RPM_DIR)/utLib*.rpm

ifeq ($(LIBTYPE),static)
	UTLIB = $(STATIC_LIB_DIR)/libutLib.a
else
	UTLIB = $(LIB_DIR)/libutLib.so
	CFLAGS += $(SH_LIB_CFLAGS)
endif

SRC_FILES := $(shell $(OF_CMD))
OBJS = $(addprefix $(OBJ_DIR)/, $(SRC_FILES:.c=.o))

-include $(OBJS:.o=.d)

$(UTLIB):$(OBJS)
$(UTLIB_RPM): $(UTLIB)

rpm:$(UTLIB_RPM)

#############################################################################
