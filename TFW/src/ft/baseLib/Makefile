include $(CURR_DIR)/TFW/inc/make_inc.mk

EXE := $(INSTALL_DIR)/baseLib-FT.exe

SRC_FILES := $(shell $(OF_CMD))
OBJS = $(addprefix $(OBJ_DIR)/, $(SRC_FILES:.c=.o))

-include $(OBJS:.o=.d)

$(EXE):$(OBJS) $(COMMON_OBJ)
rpm:$(EXE)
