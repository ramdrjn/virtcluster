#
# Copyright (C) 2007 OpenedHand Ltd.
#

SUMMARY = "virtcluster minimal package group"
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
    packagegroup-virtcluster-os-min \
    packagegroup-virtcluster-connectivity-min \
    packagegroup-virtcluster-tools-min \
    packagegroup-virtcluster-apps-min \
    "

RDEPENDS_packagegroup-virtcluster-os-min = "\
    base-files \
    base-passwd \
    eglibc \
    busybox \
    initscripts \
    modutils-initscripts \
    tinylogin \
    ${MACHINE_ESSENTIAL_EXTRA_RDEPENDS}"

RDEPENDS_packagegroup-virtcluster-connectivity-min = "\
    netbase \
    init-ifupdown \
    openssl \
    openssh \
    iputils \
    "

RDEPENDS_packagegroup-virtcluster-tools-min = "\
    bash \
    python \
    rpm \
    sqlite3 \
    "

RDEPENDS_packagegroup-virtcluster-apps-min = ""

RRECOMMENDS_packagegroup-virtcluster-apps-min = ""

RRECOMMENDS_packagegroup-virtcluster-os-min = "\
    ${MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS}"
