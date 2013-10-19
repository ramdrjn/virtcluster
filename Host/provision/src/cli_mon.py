#!/usr/bin/env python
# -*- coding: utf-8 -*-

import py_libvirt

def dom_lookup(con, name):
    dom = py_libvirt.dom_lookup(con, name)
    return dom

def dom_define(con, name):
    dom = py_libvirt.dom_define(con, name, kernel="/Work/Contents/opt/x86vm/provisioned_domains/x86vm-0/images/yocto-x86/bzImage")
    return dom

def dom_undefine(dom):
    py_libvirt.dom_undefine(dom)

def dom_start(dom):
    py_libvirt.dom_start(dom)

def dom_stop(dom):
    py_libvirt.dom_stop(dom)

def dom_shut(dom):
    py_libvirt.dom_shut(dom)

def dom_pause(dom):
    py_libvirt.dom_pause(dom)

def dom_resume(dom):
    py_libvirt.dom_resume(dom)

def dom_list(con):
    py_libvirt.list_domains(con)

def dom_info(dom):
    py_libvirt.info_domain(dom)

def dom_dumpxml(dom, nwk):
    py_libvirt.dumpxml_domain(dom)
    py_libvirt.dumpxml_network(nwk)

def dom_br_mod(dom, maxvcpu):
    py_libvirt.set_maxVcpu(dom, maxvcpu)
    py_libvirt.set_vcpu(dom, maxvcpu)

def dom_ar_mod(dom):
    None

def dom_br_dev_mod(dom):
    py_libvirt.attach_raw_disk_nhp(dom, "/Work/Contents/opt/x86vm/provisioned_domains/x86vm-0/images/yocto-x86/virtcluster-x86vm.ext3")
    py_libvirt.attach_interface(dom, "52:54:00:d7:2a:31",
                                "virtcluster_fabric0", "vfab0")

def dom_ar_dev_mod(dom):
    None

def dom_as_mod(dom):
    None

def dom_as_dev_mod(dom):
    #py_libvirt.set_graphics_sdl(dom)
    None

def nwk_lookup(con, name):
    nwk = py_libvirt.network_lookup(con, name)
    return nwk

def network_start(nwk):
    py_libvirt.network_start(nwk)

def network_stop(nwk):
    py_libvirt.network_stop(nwk)

def nwk_def(con, nwk_name):
    nwk=py_libvirt.network_define(con, nwk_name, "virfab0",
                                  "52:54:00:3E:31:C9", "192.168.100.1",
                                  "192.168.100.128", "192.168.100.254")
    network_start(nwk)
    return nwk

def nwk_undef(nwk):
    network_stop(nwk)
    py_libvirt.network_undefine(nwk)

if __name__=='__main__':
    con = py_libvirt.con_init()

    name = 'x86vm'
    nwk_name = 'virtcluster_fabric0'

    dom = dom_lookup(con, name)

    nwk= nwk_lookup(con, nwk_name)

    while True:
        opt = raw_input("Enter option:\n\
 d>efine u>ndefine\
 nd>efine nu>ndefine\
 brm>od brd>ev\
 s>tart sh>ut st>op\
 p>ause r>esume\
 arm>od ard>ev\
 asm>od asd>ev\
 l>ist i>nfo x>ml\
 e>xit :\
 ")
        if opt == 'e':
            break;
        elif opt == 'd':
            dom = dom_define(con, name)
        elif opt == 'u':
            dom = dom_undefine(dom)
            dom=None
        elif opt == 'brm':
            dom_br_mod(dom, 2)
        elif opt == 'brd':
            dom_br_dev_mod(dom)
        elif opt == 's':
            dom_start(dom)
        elif opt == 'sh':
            dom_shut(dom)
        elif opt == 'st':
            dom_stop(dom)
        elif opt == 'p':
            dom_pause(dom)
        elif opt == 'r':
            dom_resume(dom)
        elif opt == 'arm':
            dom_ar_mod(dom)
        elif opt == 'ard':
            dom_ar_dev_mod(dom)
        elif opt == 'asm':
            dom_as_mod(dom)
        elif opt == 'asd':
            dom_as_dev_mod(dom)
        elif opt == 'l' or opt == '\n':
            dom_list(con)
        elif opt == 'i':
            dom_info(dom)
        elif opt == 'x':
            dom_dumpxml(dom, nwk)
        elif opt == 'nd':
            nwk=nwk_def(con, nwk_name)
        elif opt == 'nu':
            nwk_undef(nwk)
            nwk=None
        else:
            break;

    py_libvirt.con_fin(con)
