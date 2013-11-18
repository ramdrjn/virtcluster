DESCRIPTION = "virtcluster image"

IMAGE_FEATURES = "package-management"

IMAGE_INSTALL = "\
               packagegroup-virtcluster-os-min \
               packagegroup-virtcluster-connectivity-min \
               packagegroup-virtcluster-tools-min \
               packagegroup-virtcluster-apps-min \
               "

IMAGE_LINGUAS = "en-us"

LICENSE = "MIT"

inherit core-image

IMAGE_ROOTFS_SIZE = "8192"

# remove not needed ipkg informations
ROOTFS_POSTPROCESS_COMMAND += "remove_packaging_data_files ; "
