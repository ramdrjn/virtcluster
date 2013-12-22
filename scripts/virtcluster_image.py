#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inc.scripts.py import common
import shutil
import os
import inspect
import json
import glob
import logging

logger=None

def prep(image_prep_dir, images_dir):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      [os.remove(f) for f in glob.glob(os.path.join(images_dir, "*.tgz"))]
      try:
            os.remove(os.path.join(images_dir, "manifest"))
      except OSError:
            pass
      shutil.rmtree(image_prep_dir, True)
      os.mkdir(image_prep_dir)

def prep_dir(image_prep_dir, cwd):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      t_dir=os.environ['TARGET_TYPE']
      filename="{0}/conf/target/{1}/target.desc".format(cwd,t_dir)
      with open(filename) as infile:
            target_desc = json.load(infile)
      manifest=os.path.join(image_prep_dir, "manifest")
      f=open(manifest, 'w')
      f.write("{\n")
      for t in ["device_file", "fs_raw", "fs_tar", "initramfs", "initrd", "modules", "bootloader", "kernel"]:
            t_file=target_desc[t]
            if t_file:
                  try:
                        shutil.copy(t_file, image_prep_dir)
                        f.write("\"{0}\":\"{1}\"".format(t,
                                                 t_file[t_file.rfind("/")+1:]))
                        if t=="kernel":
                              f.write("\n")
                        else:
                              f.write(",\n")
                  except IOError:
                        logger.error("Skipping file: {0}".format(t_file))
      f.write("}")
      f.close()

def pack_image(image_prep_dir, image_dir, tar_name):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))

      cmd=["tar", "-C", "{0}".format(image_dir), "-zcvf", "{0}".format(tar_name), "{0}".format(os.path.basename(image_prep_dir))]

      op = common.exec_cmd_op(cmd)
      logger.info(op)
      shutil.copy(os.path.join(image_prep_dir, "manifest"),\
                        os.path.join(image_dir, "manifest"))
      logger.info("Finished packaging images")

def cleanup(image_prep_dir):
      logger.debug("In Function {0}".format(inspect.stack()[0][3]))
      shutil.rmtree(image_prep_dir, True)

def _package_image_prep(currdir):
      global logger

      log_f="{0}/output/logs/image.log".format(currdir)

      # create logger
      logger = logging.getLogger('image')
      logger.setLevel(logging.INFO)

      # create file handler and set level to debug
      fh = logging.FileHandler(log_f)

      fh.setLevel(logging.DEBUG)

      # create formatter
      formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s')

      # add formatter to ch
      fh.setFormatter(formatter)

      # add fh to logger
      logger.addHandler(fh)

      logger.info('Image preparation started')

def _package_image(currdir):

      _package_image_prep(currdir)

      logger.info("CWD: {0}".format(currdir))

      ARCH=os.environ['ARCH']
      logger.info("ARCH: {0}".format(ARCH))

      image_dir=os.path.join(currdir, "Image/pre_built_images/images")
      target_dir=os.environ['TARGET_TYPE']
      image_prep_dir=os.path.join(image_dir, target_dir)
      tar_name=os.path.join(image_dir,
                            "virtcluster-image-{0}.tgz".format(target_dir))
      logger.info("Image preparation directory: {0}".format(image_prep_dir))
      logger.info("Image output: {0}".format(tar_name))

      prep(image_prep_dir, image_dir)
      prep_dir(image_prep_dir, currdir)
      pack_image(image_prep_dir, image_dir, tar_name)
      cleanup(image_prep_dir)

def package_image(currdir):
      try:
            _package_image(currdir)
      except:
            logger.exception("Image preparation failed")
