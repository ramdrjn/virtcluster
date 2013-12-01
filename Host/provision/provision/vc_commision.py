#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
from provision import py_libvirt

import inspect
import os

def _prep_commision(dat_dir, fname):
    with open(fname, "w") as f:
        f.write("Initiated")
    key_fname = os.path.join(dat_dir, "host_key")
    common.exec_cmd(["ssh-keygen", "-P", "", "-f", key_fname])
    with open(fname, "w") as f:
        f.write("Done")
    return ((0, "success"))

def _check_commision_prep(dat_dir):
    prep_status=(0, "success")
    try:
        os.mkdir(dat_dir)
    except OSError:
        pass

    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        prep_status=_prep_commision(dat_dir, fname)

    if prep_status[0] != 0:
        return prep_status

    state="Done"
    with open(fname) as f:
        state=f.readline()

    if state != "Initiated":
        if state != "Done":
            return ((-1, "commision.dat state not valid"))

    return ((0, "success"))

def _do_ssh_config(domain_dir, ip_host):
    print ip_host


def _do_ssh_linkup(known_host_fname, id_fname, ip_host):
    ip=ip_host[0]
    common.exec_cmd(["ssh",
                     "-o", "UserKnownHostsFile={0}".format(known_host_fname),
                     "-o", "StrictHostKeyChecking=no",
                     "-i", id_fname,
                     ip])

def start(comi_dir, arg_d):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    dat_dir = os.path.join(comi_dir, "dat")

    ck_status = _check_commision_prep(dat_dir)
    if ck_status[0] != 0:
        return ck_status

    known_host_fname = os.path.join(dat_dir, "known_hosts")
    id_fname = os.path.join(dat_dir, "host_key.pub")

    #Proceed with domain specific commision processing.
    ip_host=py_libvirt.get_fabric_ip(arg_d['domain'])

    lk_status=_do_ssh_linkup(known_host_fname, id_fname, ip_host)
    if lk_status[0] != 0:
        return lk_status

    domain_dir = os.path.join(comi_dir, arg_d['domain'])
    try:
        os.mkdir(domain_dir)
    except OSError:
        return ((-1, "Unable to create domain directory"))

    _do_ssh_config(domain_dir, ip_host)

    print arg_d
    print ck_status
    return ((0, "success"))
