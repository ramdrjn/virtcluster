
.PHONY:rpm
rpm:
	$(MAKE) -C common/ 			$(TARGET)
	$(MAKE) -C ft/baseLib/ 	$(TARGET)
	$(MAKE) -C ft/dsLib/ 		$(TARGET)
	$(MAKE) -C st/baseLib/ 	$(TARGET)
	$(MAKE) -C st/dsLib/ 		$(TARGET)
	$(MAKE) -C st/msgLib/ 	$(TARGET)

.PHONY:cleanall
cleanall:
	$(MAKE) -C ft/dsLib/ 		tfclean
	$(MAKE) -C st/baseLib/ 	tfclean
	$(MAKE) -C st/dsLib/ 		tfclean
	$(MAKE) -C st/msgLib/ 	tfclean
	$(MAKE) -C common/ 			$(TARGET)
	$(MAKE) -C ft/baseLib/ 	$(TARGET)
	$(MAKE) -C ft/dsLib/ 		$(TARGET)
	$(MAKE) -C st/baseLib/ 	$(TARGET)
	$(MAKE) -C st/dsLib/ 		$(TARGET)
	$(MAKE) -C st/msgLib/ 	$(TARGET)
