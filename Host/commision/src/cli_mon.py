#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymon

def dom_lookup(con, name):
    dom = pymon.dom_lookup(con, name)
    return dom

def dom_define(con, name):
    dom = pymon.dom_define(con, name)
    return dom

def dom_undefine(dom):
    pymon.dom_undefine(dom)

def dom_start(dom):
    pymon.dom_start(dom)

def dom_stop(dom):
    pymon.dom_stop(dom)

def dom_shut(dom):
    pymon.dom_shut(dom)

def dom_pause(dom):
    pymon.dom_pause(dom)

def dom_resume(dom):
    pymon.dom_resume(dom)

def dom_list(con):
    pymon.list_domains(con)

def dom_info(dom):
    pymon.info_domain(dom)

def dom_dumpxml(dom):
    pymon.dumpxml_domain(dom)

def dom_br_mod(dom, maxvcpu):
    pymon.set_maxVcpu(dom, maxvcpu)
    pymon.set_vcpu(dom, maxvcpu)

def dom_ar_mod(dom):
    None

def dom_br_dev_mod(dom):
    None

def dom_ar_dev_mod(dom):
    None

def dom_as_mod(dom):
    None

def dom_as_dev_mod(dom):
    #pymon.set_graphics_sdl(dom)
    None

if __name__=='__main__':
    con = pymon.con_init()

    name = 'x86vm'

    dom = dom_lookup(con, name)

    while True:
        opt = raw_input("Enter option:\n\
 d>efine u>ndefine\
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
            dom_dumpxml(dom)
        else:
            break;

    pymon.con_fin(con)
