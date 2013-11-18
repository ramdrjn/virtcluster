DESCRIPTION = "virtcluster image"

IMAGE_FEATURES += "package-management ssh-server-openssh"

IMAGE_INSTALL = "\
               packagegroup-virtcluster-os \
               packagegroup-virtcluster-connectivity \
               packagegroup-virtcluster-tools \
               packagegroup-virtcluster-apps \
               "

IMAGE_LINGUAS = "en-us"

LICENSE = "MIT"

inherit core-image

IMAGE_ROOTFS_SIZE = "8192"

# remove not needed ipkg informations
ROOTFS_POSTPROCESS_COMMAND += "remove_packaging_data_files ; "
