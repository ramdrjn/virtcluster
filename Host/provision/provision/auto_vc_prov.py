#!/usr/bin/env python
# -*- coding: utf-8 -*-

import common
import py_libvirt
import argparse
import os
import time
import inspect

def network_define(con, xml, logf):
      nwk=py_libvirt.network_defineXML(con, xml)
      return nwk

def network_start(nwk, logf):
      py_libvirt.network_start(nwk)
      common.log([common.info, common.file, logf], "\nNetwork started")

def processNetXML(con, netxml, logf):
      common.log([common.info, common.file, logf],
                 "\nPicking up netxml file as {0}".format(netxml))

      with open(netxml, 'r') as f:
            net_xml = f.read()
      nwk = network_define(con, net_xml, logf)
      network_start(nwk, logf)

def domain_define(con, xml, logf):
      dom=py_libvirt.dom_defineXML(con, xml)
      return dom

def domain_start(dom, logf):
      py_libvirt.dom_start_resume(dom)
      common.log([common.info, common.file, logf], "\Domain started")

def processDomXML(con, domxml, logf):
      common.log([common.info, common.file, logf],
                 "\nPicking up domxml file as {0}".format(domxml))

      with open(domxml, 'r') as f:
            dom_xml = f.read()
      dom = domain_define(con, dom_xml, logf)
      domain_start(dom, logf)

def args_actions(currdir, logf, args):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      if args.verbosity:
            common.set_debug_lvl(args.verbosity)
      if args.quiet:
            common.set_debug_lvl(common.error)

      con = py_libvirt.con_init()

      if args.netxml:
            processNetXML(con, args.netxml, logf)
      else:
            common.log([common.info, common.file, logf], "\nnetxml not specified");
      if args.domxml:
            processDomXML(con, args.domxml, logf)
      else:
            common.log([common.info, common.file, logf], "\ndomxml not specified");
      py_libvirt.con_fin(con)

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
