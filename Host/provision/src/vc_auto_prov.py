#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
import py_libvirt
import argparse
import os
import time
import inspect

def args_actions(currdir, logf, args):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      if args.verbosity:
            common.set_debug_lvl(args.verbosity)
      if args.quiet:
            common.set_debug_lvl(common.error)
      if args.domxml:
            domxml=args.domxml
            common.log([common.info, common.file, logf],
                       "\nPicking up domxml file as {0}".format(domxml))
      if args.netxml:
            netxml=args.netxml
            common.log([common.info, common.file, logf],
                       "\nPicking up netxml file as {0}".format(netxml))

def process_cmd_args(currdir, logf):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      parser = argparse.ArgumentParser(description="Guest Provision Script")
      parser.add_argument("-d", "--domxml",\
                               help="Specify domain(guest) xml file")
      parser.add_argument("-n", "--netxml",\
                               help="Specify network xml file")
      group = parser.add_mutually_exclusive_group()
      group.add_argument("-v", "--verbosity", type=int,\
                               help="Specify verbosity level")
      group.add_argument("-q", "--quiet", action="store_true")
      args = parser.parse_args()
      if args:
            args_actions(currdir, logf, args)

def prep(currdir):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      log_dir=os.path.join(currdir, "logs")
      try:
            os.makedirs(log_dir)
      except:
            common.log(common.debug, "Logs directory already exist.")
      ts=time.strftime("%A_%d_%B_%H_%M_%S")
      logfname="prov_{0}.log".format(ts)
      log_file = os.path.join(log_dir, logfname)
      logf=open(log_file, 'w')
      common.log([common.info, common.file, logf],
          "\nProvision started on {0} from {1}".format(time.asctime(),currdir))
      return (logf)

def cleanup(currdir, logf):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      common.log([common.info, common.file, logf],
                 "\nEnding at {0}\n".format(time.asctime()))
      logf.close()

def main():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      currdir = os.getcwd()
      logf=prep(currdir)
      process_cmd_args(currdir, logf)
      cleanup(currdir, logf)

if __name__=='__main__':
      main()
