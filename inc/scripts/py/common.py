#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import inspect
import os
import shutil
import glob
import time
import sys
import json

debug=1
info=3
error=5

debug_lvl=info

def set_debug_lvl(lvl):
      global debug_lvl
      debug_lvl = lvl

def log(lvl, arg, *args):
      if lvl >= debug_lvl:
            print(arg, (lambda: args and args or "")())
            return lvl

def exec_cmd(cmd, out=None, err=None):
      log(debug, "In Function", inspect.stack()[0][3])
      if out:
            err = subprocess.STDOUT
      try:
            log(debug, "Executing command {0}".format(cmd))
            subprocess.check_call(cmd, stdout=out, stderr=err)
      except subprocess.CalledProcessError as e:
            log(error, "Cmd: {0} returned {1}\n".format(e.cmd, e.returncode))
