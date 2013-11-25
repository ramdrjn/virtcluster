#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import common
import shutil
import os
import time
import inspect
import glob

def prep():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))

def install_host_rpm():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      common.exec_cmd(["rpm", "-ivh", "host/x86_64/provision*.rpm"])
      common.exec_cmd(["rpm", "-ivh", "host/x86_64/py*.rpm"])

def install_images():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      common.exec_cmd(["rpm", "-ivh", "x86/virtcluster_image*.rpm"])

def repo_setup():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      repo_p=os.path.join(os.path.join("/opt", "x86vm"), "repo-vc")
      os.mkdir(repo_p)
      main_p=os.path.join(repo_p, "main")
      os.mkdir(main_p)
      os.mkdir(os.path.join(repo_p, "updates"))
      for f in glob.glob("x86/*"):
            if "virtcluster_image" in f:
                  continue
            shutil.copy(f, main_p)
      common.exec_cmd(["createrepo", "-v", main_p])

def cleanup():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))

def uninstall():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      common.exec_cmd(["rpm", "-evh", "virtcluster-image"])
      common.exec_cmd(["rpm", "-evh", "provision"])
      common.exec_cmd(["rpm", "-evh", "py-scripts-common"])
      shutil.rmtree("/opt/x86vm", True)

def main():
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      prep()
      install_host_rpm()
      install_images()
      repo_setup()
      cleanup()

if __name__=='__main__':
      main()
