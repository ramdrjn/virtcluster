#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scripts.common import *
import argparse

currdir=""
log_file=""
inc_dir=""

class configCls:
      def __init__(self, filename):
            log(debug, "Initialized %s class", self.__class__)
            self.__f = open(filename, "a")
      def __del__(self):
            log(debug, "Finalized %s class", self.__class__)
            self.__f.close()
      def sendConf(self, conf):
            log(debug, "In Function", inspect.stack()[0][3])
            self.__f.write(conf)

class confighCls(configCls):
      pass

class configmkCls(configCls):
      pass

class configbldCls(configCls):
      pass

def args_actions(args):
      global inc_dir

      if args.verbosity:
            set_debug_lvl(args.verbosity)
      if args.quiet:
            global error
            set_debug_lvl(error)

      configh = confighCls(os.path.join(inc_dir, "config.h"))
      configmk = configmkCls(os.path.join(inc_dir, "config.mk"))
      configbld = configbldCls(os.path.join(inc_dir, "config.bld"))

      if args.sa:
            configmk.sendConf("\nSA={0}".format(args.sa))
            log_file.write("\nSA flag set as {0}".format(args.sa))
            log(info, "\nSA flag set as {0}".format(args.sa))
      if args.debug:
            configmk.sendConf("\nDEBUG_FLAG=-g")
            log_file.write("\nDEBUG flag (-g) set.")
            log(info, "\nDEBUG flag set")
      if args.production:
            configmk.sendConf("\nPROD_FLAG=-O{0}".format(args.production))
            log_file.write("\nOptimization -O{0} set".format(args.production))
            log(info, "\nOptimization -O{0} set".format(args.production))
      if not args.static:
            configmk.sendConf("\nLIBTYPE=shared")
            log_file.write("\nUsing shared library")
            log(info, "\nUsing shared library")
      else:
            configmk.sendConf("\nLIBTYPE=static")
            log_file.write("\nUsing static library")
            log(info, "\nUsing static library")
      if args.gprof:
            configmk.sendConf("\nGPROF_FLAGS=-pg")
            log_file.write("\nGPROF_FLAGS = -pg")
            log(info, "\nGPROF={0}".format(args.gprof))
      if args.gcov:
            configmk.sendConf("\nGCOV_FLAGS=-ftest-coverage -fprofile-arcs")
            log_file.write("\nGCOV_FLAGS= -ftest-coverage -fprofile-arcs")
            log(info, "\nGCOV={0}".format(args.gcov))

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

      ################## - End of options - ##################
      args = parser.parse_args()
      if args:
            args_actions(args)

def prep(logf):
      global currdir
      global log_file
      global inc_dir
      currdir = os.getcwd()
      inc_dir = os.path.join(currdir, "./inc")
      log_file = open(os.path.join(currdir, logf), 'w')

      log_file.write("\nConfiguration Started at {0}\n".format(time.asctime()))
      shutil.copy(os.path.join(inc_dir, "config.h.def"),\
                                     os.path.join(inc_dir, "config.h"))
      log_file.write("Copied default configs {0}\n".format("config.h"))
      shutil.copy(os.path.join(inc_dir, "config.mk.def"),\
                                     os.path.join(inc_dir, "config.mk"))
      log_file.write("Copied default configs {0}\n".format("config.mk"))
      shutil.copy(os.path.join(inc_dir, "config.bld.def"),\
                                     os.path.join(inc_dir, "config.bld"))
      log_file.write("Copied default configs {0}\n".format("config.bld"))

def cleanup():
      global currdir
      global log_file
      log_file.write("\nEnded at {0}\n".format(time.asctime()))
      log_file.close()

def main():
      prep("output/logs/config.log")
      process_cmd_args()
      cleanup()

if __name__=='__main__':
      main()
