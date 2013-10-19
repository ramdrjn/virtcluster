#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
import shutil
import os
import inspect
import json
import glob

def prep(image_prep_dir, images_dir):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      [os.remove(f) for f in glob.glob(os.path.join(images_dir, "*.tgz"))]
      try:
            os.remove(os.path.join(images_dir, "manifest"))
      except OSError:
            pass
      shutil.rmtree(image_prep_dir, True)
      os.mkdir(image_prep_dir)

def prep_dir(image_prep_dir, cwd, log_f):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      t_dir=os.environ['TARGET_TYPE']
      filename="{0}/conf/target/{1}/target.desc".format(cwd,t_dir)
      with open(filename) as infile:
            target_desc = json.load(infile)
      manifest=os.path.join(image_prep_dir, "manifest")
      f=open(manifest, 'w')
      for t in ["device_file", "fs_raw", "fs_tar", "initramfs", "initrd", "modules", "bootloader", "kernel"]:
            t_file=target_desc[t]
            if t_file:
                  try:
                        shutil.copy(t_file, image_prep_dir)
                        f.write("{0}:{1}\n".format(t,t_file))
                  except IOError:
                        common.log(common.error, "Skipping file: {0}".format(t_file))
      f.close()

def pack_image(image_prep_dir, image_dir, tar_name, log_f):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      cmd=["tar", "-C", "{0}".format(image_dir), "-zcvf", "{0}".format(tar_name), "{0}".format(os.path.basename(image_prep_dir))]
      with open(log_f, 'w') as f:
            op = common.exec_cmd(cmd, f)
      shutil.copy(os.path.join(image_prep_dir, "manifest"),\
                        os.path.join(image_dir, "manifest"))
      common.log(common.info, "Finished packaging images")

def cleanup(image_prep_dir):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      shutil.rmtree(image_prep_dir, True)

def package_image(currdir):
      common.log(common.debug,
                 "In Function {0}".format(inspect.stack()[0][3]))
      common.log(common.debug, "CWD: {0}".format(currdir))

      log_f="{0}/output/logs/image.log".format(currdir)
      common.log(common.debug, "Log file: {0}".format(log_f))
      ARCH=os.environ['ARCH']
      common.log(common.debug, "ARCH: {0}".format(ARCH))

      image_dir=os.path.join(currdir, "Image/pre_built_images/images")
      target_dir=os.environ['TARGET_TYPE']
      image_prep_dir=os.path.join(image_dir, target_dir)
      tar_name=os.path.join(image_dir, "virtcluster-image-{0}.tgz".format(target_dir))
      common.log(common.debug, "Image preparation directory: {0}".format(image_prep_dir))
      common.log(common.debug, "Image output: {0}".format(tar_name))

      prep(image_prep_dir, image_dir)
      prep_dir(image_prep_dir, currdir, log_f)
      pack_image(image_prep_dir, image_dir, tar_name, log_f)
      cleanup(image_prep_dir)
