#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
import json
import logging
import logging.handlers
import inspect

logger=None

def get_rpms(fname):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    l=[]
    logger.info("Parsing rpm list file {0}".format(fname))
    with open(fname) as f:
        rpm=f.readline()
        while rpm:
            l.append(rpm.strip("\n"))
            rpm=f.readline()
    return (l)

def smart_install(l):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    for rpm in l:
        logger.info("Installing rpm file {0}".format(rpm))
        cmd = ["smart", "install", "{0}".format(rpm), "-y"]
        out=common.exec_cmd_op(cmd)
        logger.info(out)
    logger.debug("Installation of packages done")

def prep():
    global logger

    # create logger
    logger = logging.getLogger('commision')
    logger.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fh = logging.handlers.RotatingFileHandler("/opt/x86vm/logs/stage2-commision.log",
                                              maxBytes=50*1024*1024,
                                              backupCount=2)
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    fh.setFormatter(formatter)

    # add fh to logger
    logger.addHandler(fh)

    logger.info('Commisioning stage 2 initiated')

def cleanup():
    logger.debug('Commisioning stage 2 cleanup')

    logger.info("Unmounting the cdrom after commision")
    out=common.exec_cmd_op(["umount", "/media/cdrom0"])
    if out:
        logger.info(out)

def main():

    prep()

    try:
        d={}
        with open("/opt/x86vm/conf/commision.conf") as f:
            d=json.load(f)
        pkg_grp_file=d['pm-group-file']
        with open(pkg_grp_file) as f:
            j=json.load(f)
        pkg_mgmt=j['manager']
        rpm_install_file=d['rpm_install']
        l=get_rpms(rpm_install_file)
        if pkg_mgmt == "smart":
            smart_install(l)
    except (OSError, common.execCmdError) as e:
        logger.exception("Error {0}".format(str(e)))

    cleanup()

if __name__=='__main__':
    main()
