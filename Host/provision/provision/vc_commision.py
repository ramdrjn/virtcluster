#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
import inspect
import os

def _prep_commision(dat_dir, fname):
    with open(fname, "w") as f:
        f.write("Initiated")
    key_fname = os.path.join(dat_dir, "host_key")
    common.exec_cmd(["ssh-keygen", "-P", "", "-f", key_fname])
    return (0, "success")

def _check_commision_prep(comi_dir):
    dat_dir = os.path.join(comi_dir, "dat")
    try:
        os.mkdir(dat_dir)
    except OSError:
        pass

    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        prep_status=_prep_commision(dat_dir, fname)

    state="Done"
    with open(fname) as f:
        state=f.readline()

    if state != "Initiated":
        if state != "Done":
            return (-1, "commision.dat state not valid")

    return (0, "success")

def _do_ssh_config(domain_dir):
    pass
def start(comi_dir, arg_d):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))
    ck_status = _check_commision_prep(comi_dir)

    #Proceed with domain specific commision processing.

    domain_dir = os.path.join(comi_dir, arg_d['domain'])
    try:
        os.mkdir(domain_dir)
    except OSError:
        return (-1, "Unable to create domain directory")

    _do_ssh_config(domain_dir)

    print arg_d
    print ck_status
