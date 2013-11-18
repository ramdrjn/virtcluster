FILESEXTRAPATHS_prepend_x86vm := "${THISDIR}/files:"

PR := "${PR}.1"

COMPATIBLE_MACHINE_x86vm = "x86vm"

KBRANCH_x86vm  = "standard/common-pc/base"

KERNEL_FEATURES_append_x86vm += " cfg/smp.scc"

SRC_URI += "file://x86vm-standard.scc \
            file://x86vm-user-config.cfg \
            file://x86vm-user-patches.scc \
            file://x86vm-user-features.scc \
           "


# uncomment and replace these SRCREVs with the real commit ids once you've had
# the appropriate changes committed to the upstream linux-yocto repo
#SRCREV_machine_pn-linux-yocto_x86vm ?= "b170394a475b96ecc92cbc9e4b002bed0a9f69c5"
#SRCREV_meta_pn-linux-yocto_x86vm ?= "c2ed0f16fdec628242a682897d5d86df4547cf24"
#LINUX_VERSION = "3.8"
