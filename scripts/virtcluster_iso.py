#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
import shutil
import os
import time
import inspect
import json


def prep(iso_dir):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      shutil.rmtree(iso_dir, True)
      os.mkdir(iso_dir)

def prep_dir(iso_dir, arch, rpm_lst, cwd):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      arch_dir=os.path.join(iso_dir, arch)
      common.log(common.debug, "arch dir: {0}".format(arch_dir))
      os.mkdir(arch_dir)
      with open(rpm_lst, 'r') as f:
            for rpm in f:
                  rpmf=(os.path.join(cwd,rpm)).strip("\n")
                  common.log(common.debug, "rpm file: {0}".format(rpmf))
                  try:
                        shutil.copy(rpmf, arch_dir)
                  except IOError:
                        common.log(common.error, "Skipping file: {0}".format(rpmf))

def prep_host_dir(iso_dir, arch, rpm_lst, cwd):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      host_dir=os.path.join(iso_dir, "host/")
      os.mkdir(host_dir)
      arch_dir=os.path.join(host_dir, arch)
      common.log(common.debug, "arch dir: {0}".format(arch_dir))
      os.mkdir(arch_dir)
      with open(rpm_lst, 'r') as f:
            for rpm in f:
                  rpmf=(os.path.join(cwd,rpm)).strip("\n")
                  common.log(common.debug, "rpm file: {0}".format(rpmf))
                  try:
                        shutil.copy(rpmf, arch_dir)
                  except IOError:
                        common.log(common.error, "Skipping file: {0}".format(rpmf))

def prep_host_scripts(iso_dir, cwd):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      for f in ["inc/scripts/py/common.py", "Host/iso_scripts/install_iso.py"]:
            scriptf=os.path.join(cwd, f)
            common.log(common.debug, "script file: {0}".format(scriptf))
            try:
                  shutil.copy(scriptf, iso_dir)
            except IOError:
                  common.log(common.error,"Skipping file: {0}".format(scriptf))
      common.log(common.debug, "Install scripts copied to ISO dir")

def make_iso(iso_dir, iso_name, op_log):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      cmd=["genisoimage", "-l", "-debug", "-v", "-o", "{0}".format(iso_name), "{0}".format(iso_dir),]
      with open(op_log, 'w') as f:
            op = common.exec_cmd(cmd, f)
      common.log(common.info, "Finishes generating ISO")

def cleanup(iso_dir):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      shutil.rmtree(iso_dir, True)

def gen_iso(cwd):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      currdir=cwd
      common.log(common.debug, "CWD: {0}".format(currdir))

      ISO_GEN_DIR="/tmp/virtcluster-iso/"
      common.log(common.debug, "ISO_GEN_DIR: {0}".format(ISO_GEN_DIR))
      RES_OP="{0}/output/logs/iso.log".format(currdir)
      common.log(common.debug, "RES_OP: {0}".format(RES_OP))
      ARCH=os.environ['ARCH']
      common.log(common.debug, "ARCH: {0}".format(ARCH))
      ISO_NAME="{0}/output/virtcluster-{1}.iso".format(currdir,ARCH)
      common.log(common.debug, "ISO_NAME: {0}".format(ISO_NAME))

      t_dir=os.environ['TARGET_TYPE']
      filename="{0}/conf/target/{1}/target.desc".format(currdir,t_dir)
      with open(filename) as infile:
            target_desc = json.load(infile)
      RPM_LST=target_desc["rpm_list"]
      common.log(common.debug, "RPM_LST: {0}".format(RPM_LST))

      host_arch=os.environ['HOST_ARCH']
      common.log(common.debug, "HOST_ARCH: {0}".format(host_arch))
      t_dir=os.environ['HOST_TYPE']
      filename="{0}/conf/host/{1}/host.desc".format(currdir,t_dir)
      with open(filename) as infile:
            host_desc = json.load(infile)
      host_rpm_lst=host_desc["rpm_list"]
      common.log(common.debug, "HOST_RPM_LST: {0}".format(host_rpm_lst))

      prep(ISO_GEN_DIR)
      prep_dir(ISO_GEN_DIR, ARCH, RPM_LST, currdir)
      prep_host_dir(ISO_GEN_DIR, host_arch, host_rpm_lst, currdir)
      prep_host_scripts(ISO_GEN_DIR, currdir)
      make_iso(ISO_GEN_DIR, ISO_NAME, RES_OP)
      cleanup(ISO_GEN_DIR)
