#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
import shutil
import os
import time
import inspect
import json
import logging

logger=None

def prep(iso_dir):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      shutil.rmtree(iso_dir, True)
      os.mkdir(iso_dir)

def prep_dir(iso_dir, arch, rpm_lst, cwd):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      arch_dir=os.path.join(iso_dir, arch)
      logger.info( "arch dir: {0}".format(arch_dir))
      os.mkdir(arch_dir)
      with open(rpm_lst, 'r') as f:
            for rpm in f:
                  rpmf=(os.path.join(cwd,rpm)).strip("\n")
                  logger.info( "rpm file: {0}".format(rpmf))
                  shutil.copy(rpmf, arch_dir)

def prep_host_dir(iso_dir, arch, rpm_lst, cwd):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      host_dir=os.path.join(iso_dir, "host/")
      os.mkdir(host_dir)
      arch_dir=os.path.join(host_dir, arch)
      logger.info( "arch dir: {0}".format(arch_dir))
      os.mkdir(arch_dir)
      with open(rpm_lst, 'r') as f:
            for rpm in f:
                  rpmf=(os.path.join(cwd,rpm)).strip("\n")
                  logger.info( "rpm file: {0}".format(rpmf))
                  shutil.copy(rpmf, arch_dir)

def prep_host_scripts(iso_dir, cwd):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      for f in ["inc/scripts/py/common.py", "Host/iso_scripts/install_iso.py"]:
            scriptf=os.path.join(cwd, f)
            logger.info( "script file: {0}".format(scriptf))
            shutil.copy(scriptf, iso_dir)
      logger.info( "Install scripts copied to ISO dir")

def make_iso(iso_dir, iso_name):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      cmd=["genisoimage", "-l", "-debug", "-v", "-o", "{0}".format(iso_name),
           "{0}".format(iso_dir)]
      op = common.exec_cmd_op(cmd)
      logger.info(op)
      logger.info("Finishes generating ISO")

def cleanup(iso_dir):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      shutil.rmtree(iso_dir, True)

def _gen_iso_prep(cwd):
      global logger

      log_f="{0}/output/logs/iso.log".format(cwd)

      # create logger
      logger = logging.getLogger('iso')
      logger.setLevel(logging.INFO)

      # create file handler and set level to debug
      fh = logging.FileHandler(log_f)

      fh.setLevel(logging.DEBUG)

      # create formatter
      formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')

      # add formatter to ch
      fh.setFormatter(formatter)

      # add fh to logger
      logger.addHandler(fh)

      logger.info('ISO preparation started')

def _gen_iso(cwd):

      _gen_iso_prep(cwd)

      currdir=cwd
      logger.info("CWD: {0}".format(currdir))

      ISO_GEN_DIR="/tmp/virtcluster-iso/"
      logger.info( "ISO_GEN_DIR: {0}".format(ISO_GEN_DIR))
      ARCH=os.environ['ARCH']
      logger.info("ARCH: {0}".format(ARCH))
      ISO_NAME="{0}/output/virtcluster-{1}.iso".format(currdir,ARCH)
      logger.info("ISO_NAME: {0}".format(ISO_NAME))

      t_dir=os.environ['TARGET_TYPE']
      filename="{0}/conf/target/{1}/target.desc".format(currdir, t_dir)
      with open(filename) as infile:
            target_desc = json.load(infile)
      RPM_LST=target_desc["rpm_list"]
      logger.info("RPM_LST: {0}".format(RPM_LST))

      host_arch=os.environ['HOST_ARCH']
      logger.info("HOST_ARCH: {0}".format(host_arch))
      t_dir=os.environ['HOST_TYPE']
      filename="{0}/conf/host/{1}/host.desc".format(currdir,t_dir)
      with open(filename) as infile:
            host_desc = json.load(infile)
      host_rpm_lst=host_desc["rpm_list"]
      logger.info("HOST_RPM_LST: {0}".format(host_rpm_lst))

      prep(ISO_GEN_DIR)
      prep_dir(ISO_GEN_DIR, ARCH, RPM_LST, currdir)
      prep_host_dir(ISO_GEN_DIR, host_arch, host_rpm_lst, currdir)
      prep_host_scripts(ISO_GEN_DIR, currdir)
      make_iso(ISO_GEN_DIR, ISO_NAME)
      cleanup(ISO_GEN_DIR)

def gen_iso(cwd):
      try:
            _gen_iso(cwd)
      except:
            logger.exception("ISO preparation failed")
