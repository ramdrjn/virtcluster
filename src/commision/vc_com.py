#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common

def parse_json(fname):
    d={}
    buf=""
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
    l=[]
    with open(fname) as f:
        rpm=f.readline()
        while rpm:
            l.append(rpm.strip("\n"))
            rpm=f.readline()
    return (l)

def smart_install(l):
    out=""
    err=""
    for rpm in l:
        cmd = "smart install {0} -y".format(rpm)
        status=common.exec_command(cmd, out, err)
        if status != 0:
            print (err)

def main():
    d=parse_json("/opt/x86vm/commision.conf")
    pkg_mgmt=d['pkg-mgmt']
    l=get_rpms("/opt/x86vm/conf/rpm.install")
    if pkg_mgmt == "smart":
        smart_install(l)

if __name__=='__main__':
    main()
