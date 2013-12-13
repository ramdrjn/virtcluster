#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
import os
import argparse
import time
import shutil
import inspect
import json

currdir=""
log_file=""
conf_dir=""

class configCls:
      def __init__(self, filename):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
            self.__f = open(filename, "a")
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
            self.__f.close()
      def sendConf(self, conf):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            self.__f.write(conf)

class confighCls(configCls):
      pass

class configmkCls(configCls):
      pass

class configbldCls(configCls):
      pass

class initEnvCls():
      def __init__(self, filename):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
            self.__f = open(filename, "w+")
            self.__f.write("#!/bin/sh\n")
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
            self.__f.write("\necho \"Starting dev shell. 'exit' to quit\"")
            self.__f.write("\nbash")
            self.__f.write("\necho \"Existing dev shell\"")
            self.__f.close()
      def sendData(self, conf):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            self.__f.write(conf)

def args_actions(args):
      global conf_dir
      global currdir

      if args.verbosity:
            common.set_debug_lvl(args.verbosity)
      if args.quiet:
            common.set_debug_lvl(common.error)

      configh = confighCls(os.path.join(conf_dir, "config.h"))
      configmk = configmkCls(os.path.join(conf_dir, "config.mk"))
      configbld = configbldCls(os.path.join(conf_dir, "config.bld"))
      initenv = initEnvCls(os.path.join(currdir, "init_env.sh"))

      if args.sa:
            configmk.sendConf("\nSA={0}".format(args.sa))
            common.log([common.info, common.screen_file, log_file],
                       "\nSA flag set as SA={0}".format(args.sa))
      if args.debug:
            configmk.sendConf("\nDEBUG_FLAG=-g")
            common.log([common.info, common.screen_file, log_file],
                       "\nDEBUG flag (-g) set.")
      if args.production:
            configmk.sendConf("\nPROD_FLAG=-O{0}".format(args.production))
            common.log([common.info, common.screen_file, log_file],
                       "\nOptimization -O{0} set".format(args.production))
      if not args.static:
            configmk.sendConf("\nLIBTYPE=shared")
            common.log([common.info, common.screen_file, log_file],
                       "\nUsing shared library")
      else:
            configmk.sendConf("\nLIBTYPE=static")
            common.log([common.info, common.screen_file, log_file],
                       "\nUsing static library")
      if args.gprof:
            configmk.sendConf("\nGPROF_FLAGS=-pg")
            common.log([common.info, common.screen_file, log_file],
                       "\nGPROF_FLAGS = -pg")
      if args.gcov:
            configmk.sendConf("\nGCOV_FLAGS=-ftest-coverage -fprofile-arcs")
            common.log([common.info, common.screen_file, log_file],
                       "\nGCOV_FLAGS= -ftest-coverage -fprofile-arcs")
      if args.host:
            tdir=os.path.join(conf_dir, "host")
            host_dir=os.path.join(tdir, args.host)
            filename=os.path.join(host_dir, "host.desc")
            with open(filename) as infile:
                  host_desc = json.load(infile)
            common.log([common.info, common.screen_file, log_file],
                       "\nSelecting host as {0}".format(args.host))
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
            common.log([common.info, common.screen_file, log_file],
                       "\nSelecting target as {0}".format(args.target))
            if target_desc["environment_setup_script"]:
                  sdk=target_desc["environment_setup_script"]
                  initenv.sendData("\n . "+sdk)
            if target_desc["extra_environment_setup_script"]:
                  sdk=target_desc["extra_environment_setup_script"]
                  initenv.sendData("\n . "+sdk)
            initenv.sendData("\nexport TARGET_TYPE="+args.target)

def process_cmd_args():
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

def prep(logf):
      global currdir
      global log_file
      global conf_dir
      currdir = os.getcwd()
      conf_dir = os.path.join(currdir, "conf")
      log_file = open(os.path.join(currdir, logf), 'w')

      common.log([common.info, common.lfile, log_file],
                 "\nConfiguration Started at {0}\n".format(time.asctime()))
      shutil.copy(os.path.join(conf_dir, "def_configs/config.h.def"),\
                        os.path.join(conf_dir, "config.h"))
      common.log([common.info, common.lfile, log_file],
                 "Copied default configs {0}\n".format("config.h"))
      shutil.copy(os.path.join(conf_dir, "def_configs/config.mk.def"),\
                        os.path.join(conf_dir, "config.mk"))
      common.log([common.info, common.lfile, log_file],
                 "Copied default configs {0}\n".format("config.mk"))
      shutil.copy(os.path.join(conf_dir, "def_configs/config.bld.def"),\
                        os.path.join(conf_dir, "config.bld"))
      common.log([common.info, common.lfile, log_file],
                 "Copied default configs {0}\n".format("config.bld"))

def cleanup():
      global currdir
      global log_file
      common.log([common.info, common.lfile, log_file],
                 "\nEnded at {0}\n".format(time.asctime()))
      log_file.close()

def exec_new_dev_shell():
      global currdir
      exec_file=os.path.join(currdir, "init_env.sh")
      common.exec_cmd(["chmod", "+x", exec_file])
      common.exec_cmd(exec_file)

def main():
      prep("output/logs/config.log")
      process_cmd_args()
      cleanup()
      exec_new_dev_shell()

if __name__=='__main__':
      main()
