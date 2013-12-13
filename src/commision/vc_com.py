#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
import logging
import logging.handlers
import inspect

logger=None

def parse_json(fname):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    d={}
    buf=""
    logger.info("Parsing json commisioning config file {0}".format(fname))
    with open(fname) as f:
        line=f.readline()
        while line:
            buf=buf+line.strip("\n")
            line=f.readline()
    buf=buf.replace("{", "")
    buf=buf.replace("}", "")
    buf=buf.replace('"', "")
    buf=buf.replace(" ", "")
    llist=buf.split(",")
    for ele in llist:
        tlist=ele.split(":")
        d[tlist[0]]=tlist[1]
    return (d)

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
        cmd = "smart install {0} -y".format(rpm)
        out=common.exec_command(cmd)
        logger.info(out)

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

def main():

    prep()

    try:
        d=parse_json("/opt/x86vm/conf/commision.conf")
        pkg_mgmt=d['pkg-mgmt']
        l=get_rpms("/opt/x86vm/conf/rpm.install")
        if pkg_mgmt == "smart":
            smart_install(l)
    except (OSError, common.execCmdError) as e:
        logger.exception("Error {0}".format(str(e)))

    cleanup()

if __name__=='__main__':
    main()
