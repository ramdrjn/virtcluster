#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scripts.common import *

def prep(iso_dir):
      log(debug, "In Function", inspect.stack()[0][3])
      shutil.rmtree(iso_dir, True)
      os.mkdir(iso_dir)

def prep_dir(iso_dir, arch, rpm_lst, cwd):
      log(debug, "In Function", inspect.stack()[0][3])
      arch_dir=iso_dir+arch
      log(debug, "arch dir: {0}".format(arch_dir))
      os.mkdir(arch_dir)
      with open(rpm_lst, 'r') as f:
            for rpm in f:
                  rpmf=(os.path.join(cwd,rpm)).strip("\n")
                  log(debug, "rpm file: {0}".format(rpmf))
                  try:
                        shutil.copy(rpmf, arch_dir)
                  except IOError:
                        log(error, "Skipping file: {0}".format(rpmf))

def make_iso(iso_dir, iso_name, op_log):
      log(debug, "In Function", inspect.stack()[0][3])
      cmd=["genisoimage", "-l", "-debug", "-v", "-o", "{0}".format(iso_name), "{0}".format(iso_dir),]
      with open(op_log, 'w') as f:
            op = exec_cmd(cmd, f)
      log(info, "Finishes generating ISO")

def cleanup(iso_dir):
      log(debug, "In Function", inspect.stack()[0][3])
      shutil.rmtree(iso_dir, True)

def gen_iso(cwd):
      log(debug, "In Function", inspect.stack()[0][3])
      currdir=cwd
      log(debug, "CWD: {0}".format(currdir))

      ISO_GEN_DIR="/tmp/virtcluster-iso/"
      log(debug, "ISO_GEN_DIR: {0}".format(ISO_GEN_DIR))
      RES_OP="{0}/output/logs/iso.log".format(currdir)
      log(debug, "RES_OP: {0}".format(RES_OP))
      ARCH=os.environ['ARCH']
      log(debug, "ARCH: {0}".format(ARCH))
      ISO_NAME="{0}/output/virtcluster-{1}.iso".format(currdir,ARCH)
      log(debug, "ISO_NAME: {0}".format(ISO_NAME))
      RPM_LST="{0}/inc/rpm.list.{1}".format(currdir,ARCH)
      log(debug, "RPM_LST: {0}".format(RPM_LST))

      prep(ISO_GEN_DIR)
      prep_dir(ISO_GEN_DIR, ARCH, RPM_LST, currdir)
      make_iso(ISO_GEN_DIR, ISO_NAME, RES_OP)
      cleanup(ISO_GEN_DIR)
