#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
import inspect

def _prep_commision(fname):
    with open(fname, "w") as f:
        f.write("Initiated")

def _check_commision_prep(comi_dir):
    dat_dir = os.path.join(comi_dir, "dat")
    try:
        os.mkdir(dat_dir)
    except OSError:
        return (-1, "dat directory not found")

    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        _prep_commision(fname)

    with open(fname) as f:
        state=f.readline()

    if state != "Initiated" or state != "Done":
        return (-1, "commision.dat state not valid")

    return (0, "success")

def start(comi_dir, arg_d):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))
    ck_status = _check_commision_prep(comi_dir)
    print arg_d
    print ck_status
