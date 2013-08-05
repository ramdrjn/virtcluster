#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scripts.common import *
from scripts import virtcluster_iso
import argparse

currdir=""
log_file=""

class tagsCls:
      def __init__(self):
            log(debug, "Initialized %s class", self.__class__)
      def __del__(self):
            log(debug, "Finalized %s class", self.__class__)
      def gen_listof_files(self):
            log(debug, "In Function", inspect.stack()[0][3])
            exec_cmd(["find", "./src/", "-name", "*.[ch]", "-fprint", "cscope.files"])
            log(info, "Generated list of files")
      def gen_tags(self):
            log(debug, "In Function", inspect.stack()[0][3])
            exec_cmd(["ctags", "-e", "-L", "cscope.files"])
            log(info, "Generated TAGS")
      def gen_cscope(self):
            log(debug, "In Function", inspect.stack()[0][3])
            exec_cmd(["cscope", "-bq"])
            log(info, "Generated cscope db")
      def gen(self):
            log(debug, "In Function", inspect.stack()[0][3])
            self.gen_listof_files()
            self.gen_tags()
            self.gen_cscope()

class cleanCls:
      def __init__(self):
            log(debug, "Initialized %s class", self.__class__)
            self.pat_lst=[\
                  "tags",\
                        "TAGS",\
                        "cscope*",\
                        "output/*iso",\
                        "output/logs/*log*"\
                        ]
      def __del__(self):
            log(debug, "Finalized %s class", self.__class__)
      def dist_clean(self):
            log(debug, "In Function", inspect.stack()[0][3])
            log(debug, "Removing iso images")
            [[os.remove(f) for f in glob.glob(pat)] for pat in self.pat_lst]
            [os.remove(f) for f in ["./inc/config.h", "./inc/config.mk",\
                                           "./inc/config.bld"]]

class buildCls:
      def __init__(self):
            log(debug, "Initialized %s class", self.__class__)
      def __del__(self):
            log(debug, "Finalized %s class", self.__class__)
      def _make(self, direc, mod, target):
            global log_file
            log(debug, "In Function", inspect.stack()[0][3])
            cmd_lst=["make", "-C", direc,\
                           "MODULE={0}".format(mod),\
                           "TARGET={0}".format(target)\
                           ]
            global log_file
            with open(log_file, 'a') as f:
                  exec_cmd(cmd_lst, f)
      def build(self, testbin, mod, target):
            log(debug, "In Function", inspect.stack()[0][3])
            if testbin:
                  self._make("TFW", mod, target)
            else:
                  self._make("src", mod, target)

class isoCls:
      def __init__(self):
            log(debug, "Initialized %s class", self.__class__)
      def __del__(self):
            log(debug, "Finalized %s class", self.__class__)
      def create_iso(self, currdir):
            log(debug, "In Function", inspect.stack()[0][3])
            virtcluster_iso.gen_iso(currdir)

def build_prep(logf):
      global currdir
      global log_file
      currdir = os.getcwd()
      os.environ ['CURR_DIR'] = currdir
      log(info, "\nBuilding from {0}".format(currdir))
      log_file = os.path.join(currdir, logf)
      with open(log_file, 'w') as f:
            f.write("\nBuilding from {0}".format(currdir))
            f.write("\nStarted at {0}\n".format(time.asctime()))

def build_action(testbin, mod, target):
      log(debug, "In Function", inspect.stack()[0][3])
      build=buildCls()
      build.build(testbin, mod, target)

def args_actions(args):
      if args.verbosity:
            set_debug_lvl(args.verbosity)
      if args.quiet:
            global error
            set_debug_lvl(error)
      if args.distclean:
            clean=cleanCls()
            clean.dist_clean()
            sys.exit(0)
      if args.tags:
            tags=tagsCls()
            tags.gen()
      build_action(args.testbin, args.module, args.target)
      if args.iso:
            global currdir
            iso=isoCls()
            iso.create_iso(currdir)

def process_cmd_args():
      parser = argparse.ArgumentParser(description="Build script")
      parser.add_argument("--testbin", help="Compile test binaries",\
                                action="store_true")
      parser.add_argument("--tags", help="Generate ctags and cscope files",\
                                action="store_true")
      parser.add_argument("--iso", help="Create final ISO of rpms",\
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
            f.write("\nEnding at {0}\n".format(time.asctime()))

def main():
      build_prep("output/logs/build.log")
      process_cmd_args()
      cleanup()

if __name__=='__main__':
      main()
