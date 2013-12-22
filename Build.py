#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
from scripts import virtcluster_iso
from scripts import virtcluster_image
import argparse
import os
import inspect
import glob
import sys
import logging

currdir=""
logger=""

class tagsCls:
      def __init__(self):
            logger.debug("Initialized {0} class".format(self.__class__))

      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))

      def gen_listof_files(self):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            common.exec_cmd(["find", "./src/", "-name", "*.[ch]", "-fprint", "cscope.files"])
            logger.info("Generated list of files")
      def gen_tags(self):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            common.exec_cmd(["ctags", "-e", "-L", "cscope.files"])
            logger.info("Generated TAGS")
      def gen_cscope(self):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            common.exec_cmd(["cscope", "-bq"])
            logger.info("Generated cscope db")
      def gen(self):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            self.gen_listof_files()
            self.gen_tags()
            self.gen_cscope()

class cleanCls:
      def __init__(self):
            logger.debug("Initialized {0} class".format(self.__class__))

            self.pat_lst=[\
                  "tags",\
                        "TAGS",\
                        "cscope*",\
                        "output/*iso",\
                        "output/logs/*log*",\
                        "init_env.sh"\
                        ]
      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))
      def dist_clean(self):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            logger.info("Removing iso images")
            [[os.remove(f) for f in glob.glob(pat)] for pat in self.pat_lst]
            [os.remove(f) for f in ["./conf/config.h", "./conf/config.mk",\
                                           "./conf/config.bld"]]

class buildCls:
      def __init__(self):
            logger.debug("Initialized {0} class".format(self.__class__))
      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))
      def _make(self, direc, mod, target):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            cmd_lst=["make", "-C", direc,\
                           "MODULE={0}".format(mod),\
                           "TARGET={0}".format(target)\
                           ]
            with open("output/logs/build.log", 'a') as f:
                  common.exec_cmd(cmd_lst, f)
      def build(self, testbin, host, image, mod, target):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))

            if testbin:
                  self._make("TFW", mod, target)
            elif host:
                  self._make("Host", mod, target)
            elif image:
                  if target != "cleanall":
                        logger.info("Preparing image")
                        image=imageCls()
                        image.prep_image(currdir)
                  self._make("Image", mod, target)
            else:
                  self._make("src", mod, target)

class isoCls:
      def __init__(self):
            logger.debug("Initialized {0} class".format(self.__class__))
      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))
      def create_iso(self, currdir):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))
            virtcluster_iso.gen_iso(currdir)

class imageCls:
      def __init__(self):
            logger.debug("Initialized {0} class".format(self.__class__))
      def __del__(self):
            logger.debug("Finalized {0} class".format(self.__class__))
      def prep_image(self, currdir):
            logger.debug("In Function {0}".format(inspect.stack()[0][3]))
            virtcluster_image.package_image(currdir)

def args_actions(args):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      if args.verbosity:
            logger.setLevel(logging.DEBUG)
      if args.quiet:
            logger.setLevel(logging.ERROR)

      if args.distclean:
            clean=cleanCls()
            clean.dist_clean()
            return (1)

      if args.tags:
            tags=tagsCls()
            tags.gen()

      build=buildCls()
      build.build(args.testbin, args.host, args.image,
                  args.module, args.target)
      if args.iso:
            iso=isoCls()
            iso.create_iso(currdir)

def process_cmd_args():
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

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

def build_prep():
      global currdir
      global logger

      currdir = os.getcwd()
      os.environ ['CURR_DIR'] = currdir

      # create logger
      logger = logging.getLogger('build')
      logger.setLevel(logging.INFO)

      # create file handler and set level to debug
      fh = logging.FileHandler("output/logs/build.log")

      fh.setLevel(logging.DEBUG)

      # create formatter
      formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')

      # add formatter to ch
      fh.setFormatter(formatter)

      # add fh to logger
      logger.addHandler(fh)

      logger.info("Building from {0}".format(currdir))

def cleanup():
      logger.info("Build done")

def main():
      build_prep()
      process_cmd_args()
      cleanup()

if __name__=='__main__':
      try:
            main()
      except:
            logger.exception("Build failed")
