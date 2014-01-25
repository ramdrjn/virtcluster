#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
import os
import argparse
import shutil
import inspect
import json
import logging

currdir=""
logger=""
conf_dir=""

class configCls:
      def __init__(self, filename):
            logger.debug("Initialized {0} class".format(self.__class__))
            self.__f = open(filename, "a")
      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))
            self.__f.close()
      def sendConf(self, conf):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))
            self.__f.write(conf)

class confighCls(configCls):
      pass

class configmkCls(configCls):
      pass

class configbldCls(configCls):
      pass

class initEnvCls():
      def __init__(self, filename):
            logger.debug("Initialized {0} class".format(self.__class__))
            self.__f = open(filename, "w+")
            self.__f.write("#!/bin/sh\n")
      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))
            self.__f.write("\necho \"Starting dev shell. 'exit' to quit\"")
            self.__f.write("\nbash")
            self.__f.write("\necho \"Existing dev shell\"")
            self.__f.close()
      def sendData(self, conf):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))
            self.__f.write(conf)

def args_actions(args):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      if args.verbosity:
            logger.setLevel(logging.DEBUG)
      if args.quiet:
            logger.setLevel(logging.ERROR)

      configh = confighCls(os.path.join(conf_dir, "config.h"))
      configmk = configmkCls(os.path.join(conf_dir, "config.mk"))
      configbld = configbldCls(os.path.join(conf_dir, "config.bld"))
      initenv = initEnvCls(os.path.join(currdir, "init_env.sh"))

      if args.sa:
            configmk.sendConf("\nSA={0}".format(args.sa))
            logger.info("SA flag set as SA={0}".format(args.sa))
      if args.debug:
            configmk.sendConf("\nDEBUG_FLAG=-g")
            logger.info("DEBUG flag (-g) set.")
      if args.production:
            configmk.sendConf("\nPROD_FLAG=-O{0}".format(args.production))
            logger.info("Optimization -O{0} set".format(args.production))
      if not args.static:
            configmk.sendConf("\nLIBTYPE=shared")
            logger.info("Using shared library")
      else:
            configmk.sendConf("\nLIBTYPE=static")
            logger.info("Using static library")
      if args.gprof:
            configmk.sendConf("\nGPROF_FLAGS=-pg")
            logger.info("GPROF_FLAGS = -pg")
      if args.gcov:
            configmk.sendConf("\nGCOV_FLAGS=-ftest-coverage -fprofile-arcs")
            logger.info("GCOV_FLAGS= -ftest-coverage -fprofile-arcs")
      if args.host:
            tdir=os.path.join(conf_dir, "host")
            host_dir=os.path.join(tdir, args.host)
            filename=os.path.join(host_dir, "host.desc")
            with open(filename) as infile:
                  host_desc = json.load(infile)
            logger.info("Selecting host as {0}".format(args.host))
            if host_desc["environment_setup_script"]:
                  sdk=host_desc["environment_setup_script"]
                  initenv.sendData("\n . "+sdk)
            if host_desc["extra_environment_setup_script"]:
                  sdk=host_desc["extra_environment_setup_script"]
                  initenv.sendData("\n . "+sdk)
            initenv.sendData("\nexport HOST_TYPE="+args.host)
      if args.target:
            tdir=os.path.join(conf_dir, "target")
            target_dir=os.path.join(tdir, args.target)
            filename=os.path.join(target_dir, "target.desc")
            with open(filename) as infile:
                  target_desc = json.load(infile)
            logger.info("Selecting target as {0}".format(args.target))
            if target_desc["environment_setup_script"]:
                  sdk=target_desc["environment_setup_script"]
                  initenv.sendData("\n . "+sdk)
            if target_desc["extra_environment_setup_script"]:
                  sdk=target_desc["extra_environment_setup_script"]
                  initenv.sendData("\n . "+sdk)
            if target_desc["kernel_src"]:
                  src=target_desc["kernel_src"]
                  initenv.sendData("\nexport K_SRC_DIR="+src)
            initenv.sendData("\nexport TARGET_TYPE="+args.target)

def process_cmd_args():
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      parser = argparse.ArgumentParser(description="Configuration script")

      ################## - SA - ##################
      parser.add_argument("--sa",\
                                help="Enable Static Analysis on code",\
                                action="store_true")

      ################## - Verbosity level - ##################
      group_verbosity = parser.add_mutually_exclusive_group()
      group_verbosity.add_argument("-v", "--verbosity", type=int)
      group_verbosity.add_argument("-q", "--quiet", action="store_true")

      ################## - debug/production level - ##################
      parser.add_argument("-d", "--debug", action="store_true",\
                                help="Enable debugging mode")
      parser.add_argument("-p", "--production", type=int, metavar="'O Level'",\
                                help="Enter optimization 'O' level for production mode")

      ################## - library type - ##################
      group_lib = parser.add_argument_group("Static Library",\
                                                  "Debugging tools with static library")
      group_lib.add_argument("--static", action="store_true",\
                                   help="Enable static library")
      group_lib.add_argument("--gprof", action="store_true",\
                                   help="Enable gprof")
      group_lib.add_argument("--gcov", action="store_true",\
                                   help="Enable gcov")

      ################## - host type - ##################
      parser.add_argument("--host", default="native-x86_64", nargs='?',\
                                help="Host type else native-x86_64")

      ################## - target type - ##################
      parser.add_argument("--target", default="yocto-x86", nargs='?',\
                                help="Target type else yocto-x86")

      ################## - End of options - ##################
      args = parser.parse_args()
      if args:
            args_actions(args)

def prep():
      global currdir
      global logger
      global conf_dir

      currdir = os.getcwd()
      conf_dir = os.path.join(currdir, "conf")

      # create logger
      logger = logging.getLogger('config')
      logger.setLevel(logging.INFO)

      # create file handler and set level to debug
      fh = logging.FileHandler("output/logs/config.log")

      fh.setLevel(logging.DEBUG)

      # create formatter
      formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')

      # add formatter to ch
      fh.setFormatter(formatter)

      # add fh to logger
      logger.addHandler(fh)

      logger.info('Configuration started')

      shutil.copy(os.path.join(conf_dir, "def_configs/config.h.def"),\
                        os.path.join(conf_dir, "config.h"))
      logger.info("Copied default configs {0}".format("config.h"))
      shutil.copy(os.path.join(conf_dir, "def_configs/config.mk.def"),\
                        os.path.join(conf_dir, "config.mk"))
      logger.info("Copied default configs {0}".format("config.mk"))
      shutil.copy(os.path.join(conf_dir, "def_configs/config.bld.def"),\
                        os.path.join(conf_dir, "config.bld"))
      logger.info("Copied default configs {0}".format("config.bld"))

def cleanup():
      logger.info("Configuration Ended")

def exec_new_dev_shell():
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      exec_file=os.path.join(currdir, "init_env.sh")
      common.exec_cmd(["chmod", "+x", exec_file])
      common.exec_cmd(exec_file)

def main():
      prep()
      process_cmd_args()
      cleanup()
      exec_new_dev_shell()

if __name__=='__main__':
      try:
            main()
      except:
            logger.exception("Error during configuration")
