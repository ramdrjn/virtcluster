#
# Copyright (C) 2007 OpenedHand Ltd.
#

SUMMARY = "virtcluster package group"
DESCRIPTION = "The minimal set of packages required to boot the system"
LICENSE = "MIT"
DEPENDS = "virtual/kernel"
PR = "r01"

inherit packagegroup

PACKAGE_ARCH = "${MACHINE_ARCH}"

#
# Set by the machine configuration with packages essential for device bootup
#
MACHINE_ESSENTIAL_EXTRA_RDEPENDS ?= ""
MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS ?= ""

PACKAGES = "\
    packagegroup-virtcluster-os \
    packagegroup-virtcluster-connectivity \
    packagegroup-virtcluster-tools \
    packagegroup-virtcluster-apps \
    "

# Distro can override the following VIRTUAL-RUNTIME providers:
VIRTUAL-RUNTIME_dev_manager ?= "udev"
VIRTUAL-RUNTIME_login_manager ?= "tinylogin"
VIRTUAL-RUNTIME_init_manager ?= "sysvinit"
VIRTUAL-RUNTIME_initscripts ?= "initscripts"
VIRTUAL-RUNTIME_keymaps ?= "keymaps"

RDEPENDS_packagegroup-virtcluster-os = "\
    base-files \
    base-passwd \
    eglibc \
    busybox \
    ${@base_contains("MACHINE_FEATURES", "rtc", "busybox-hwclock", "", d)} \
    ${@base_contains("MACHINE_FEATURES", "keyboard", "${VIRTUAL-RUNTIME_keymaps}", "", d)} \
    modutils-initscripts \
    ${VIRTUAL-RUNTIME_login_manager} \
    ${VIRTUAL-RUNTIME_init_manager} \
    ${VIRTUAL-RUNTIME_initscripts} \
    ${VIRTUAL-RUNTIME_dev_manager} \
    ${VIRTUAL-RUNTIME_update-alternatives} \
    ${MACHINE_ESSENTIAL_EXTRA_RDEPENDS}"

RDEPENDS_packagegroup-virtcluster-connectivity = "\
    netbase \
    init-ifupdown \
    openssl \
    openssh \
    iputils \
    "

RDEPENDS_packagegroup-virtcluster-tools = "\
    bash \
    python \
    rpm \
    sqlite3 \
    "

RDEPENDS_packagegroup-virtcluster-apps = ""

RRECOMMENDS_packagegroup-virtcluster-apps = ""

RRECOMMENDS_packagegroup-virtcluster-os = "\
    ${MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS}"
