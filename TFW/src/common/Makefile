
include $(CURR_DIR)/TFW/inc/make_inc.mk

SRC_FILES := $(shell $(OF_CMD))
OBJS = $(addprefix $(OBJ_DIR)/, $(SRC_FILES:.c=.o))

-include $(OBJS:.o=.d)

rpm:common.o
