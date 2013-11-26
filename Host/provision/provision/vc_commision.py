#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
import inspect

def _prep_commision(comi_dir):
    print comi_dir

def _check_commision_prep(comi_dir):
    
    _prep_commision(comi_dir)

def start(comi_dir, arg_d):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    _check_commision_prep(comi_dir)
    print arg_d
