#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py.common import *

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

def prep_host_dir(iso_dir, arch, rpm_lst, cwd):
      log(debug, "In Function", inspect.stack()[0][3])
      host_dir=iso_dir+"host/"
      os.mkdir(host_dir)
      arch_dir=host_dir+arch
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

      t_dir=os.environ['TARGET_TYPE']
      filename="{0}/conf/target/{1}/target.desc".format(currdir,t_dir)
      with open(filename) as infile:
            target_desc = json.load(infile)
      RPM_LST=target_desc["rpm_list"]
      log(debug, "RPM_LST: {0}".format(RPM_LST))

      host_arch=os.environ['HOST_ARCH']
      log(debug, "HOST_ARCH: {0}".format(host_arch))
      t_dir=os.environ['HOST_TYPE']
      filename="{0}/conf/host/{1}/host.desc".format(currdir,t_dir)
      with open(filename) as infile:
            host_desc = json.load(infile)
      host_rpm_lst=host_desc["rpm_list"]
      log(debug, "HOST_RPM_LST: {0}".format(host_rpm_lst))

      prep(ISO_GEN_DIR)
      prep_dir(ISO_GEN_DIR, ARCH, RPM_LST, currdir)
      prep_host_dir(ISO_GEN_DIR, host_arch, host_rpm_lst, currdir)
      make_iso(ISO_GEN_DIR, ISO_NAME, RES_OP)
      cleanup(ISO_GEN_DIR)
