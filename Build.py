#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
from scripts import virtcluster_iso
from scripts import virtcluster_image
import argparse
import os
import inspect
import time
import glob
import sys

currdir=""
log_file=""

class tagsCls:
      def __init__(self):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
      def gen_listof_files(self):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            common.exec_cmd(["find", "./src/", "-name", "*.[ch]", "-fprint", "cscope.files"])
            common.log(common.info, "Generated list of files")
      def gen_tags(self):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            common.exec_cmd(["ctags", "-e", "-L", "cscope.files"])
            common.log(common.info, "Generated TAGS")
      def gen_cscope(self):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            common.exec_cmd(["cscope", "-bq"])
            common.log(common.info, "Generated cscope db")
      def gen(self):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            self.gen_listof_files()
            self.gen_tags()
            self.gen_cscope()

class cleanCls:
      def __init__(self):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
            self.pat_lst=[\
                  "tags",\
                        "TAGS",\
                        "cscope*",\
                        "output/*iso",\
                        "output/logs/*log*",\
                        "init_env.sh"\
                        ]
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
      def dist_clean(self):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            common.log(common.debug, "Removing iso images")
            [[os.remove(f) for f in glob.glob(pat)] for pat in self.pat_lst]
            [os.remove(f) for f in ["./conf/config.h", "./conf/config.mk",\
                                           "./conf/config.bld"]]

class buildCls:
      def __init__(self):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
      def _make(self, direc, mod, target):
            global log_file
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            cmd_lst=["make", "-C", direc,\
                           "MODULE={0}".format(mod),\
                           "TARGET={0}".format(target)\
                           ]
            global log_file
            with open(log_file, 'a') as f:
                  common.exec_cmd(cmd_lst, f)
      def build(self, testbin, host, mod, target):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            if testbin:
                  self._make("TFW", mod, target)
            elif host:
                  self._make("Host", mod, target)
            else:
                  self._make("src", mod, target)
      def build_image_rpm(self, mod, target):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            self._make("Image", mod, target)

class isoCls:
      def __init__(self):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
      def create_iso(self, currdir):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            virtcluster_iso.gen_iso(currdir)

class imageCls:
      def __init__(self):
            common.log(common.debug,
                       "Initialized {0} class".format(self.__class__))
      def __del__(self):
            common.log(common.debug,
                       "Finalized {0} class".format(self.__class__))
      def prep_image(self, currdir):
            common.log(common.debug,
                       "In Function {0}".format(inspect.stack()[0][3]))
            virtcluster_image.package_image(currdir)

def build_prep(logf):
      global currdir
      global log_file
      currdir = os.getcwd()
      os.environ ['CURR_DIR'] = currdir
      log_file = os.path.join(currdir, logf)
      with open(log_file, 'w') as f:
            common.log([common.info, common.screen_file, f],
                       "\nBuilding from {0}".format(currdir))
            common.log([common.info, common.file, f],
                       "\nStarted at {0}\n".format(time.asctime()))

def args_actions(args):
      global currdir
      if args.verbosity:
            common.set_debug_lvl(args.verbosity)
      if args.quiet:
            common.set_debug_lvl(common.error)
      if args.distclean:
            clean=cleanCls()
            clean.dist_clean()
            sys.exit(0)
      if args.tags:
            tags=tagsCls()
            tags.gen()
      build=buildCls()
      if args.image:
            if args.target != "cleanall":
                  image=imageCls()
                  image.prep_image(currdir)
            build.build_image_rpm(args.module, args.target)
      build.build(args.testbin, args.host, args.module, args.target)
      if args.iso:
            iso=isoCls()
            iso.create_iso(currdir)

def process_cmd_args():
      parser = argparse.ArgumentParser(description="Build script")
      parser.add_argument("--testbin", help="Compile test binaries",\
                                action="store_true")
      parser.add_argument("--host", help="Build host packages",\
                                action="store_true")
      parser.add_argument("--tags", help="Generate ctags and cscope files",\
                                action="store_true")
      parser.add_argument("--iso", help="Create final ISO of rpms",\
                                action="store_true")
      parser.add_argument("--image", help="Create virtcluster images",\
                                action="store_true")
      parser.add_argument("--distclean", help="Super clean",\
                                action="store_true")
      parser.add_argument("module", default="all", nargs='?',\
                                help="Specify the module else 'all'")
      parser.add_argument("target", default="rpm", nargs='?',\
                                help="Specify the target. Either of rpm, clean or cleanall")
      group = parser.add_mutually_exclusive_group()
      group.add_argument("-v", "--verbosity", type=int,\
                               help="Specify verbosity level")
      group.add_argument("-q", "--quiet", action="store_true")
      args = parser.parse_args()
      if args:
            args_actions(args)

def cleanup():
      global currdir
      global log_file
      with open(log_file, 'a') as f:
            common.log([common.info, common.file, f],
                       "\nEnding at {0}\n".format(time.asctime()))

def main():
      build_prep("output/logs/build.log")
      process_cmd_args()
      cleanup()

if __name__=='__main__':
      main()
