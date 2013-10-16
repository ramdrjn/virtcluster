#!/usr/bin/env python
# -*- coding: utf-8 -*-

import libvirt

'''                              Internal functions'''

'''               Utility functions'''

def _debug(msg):
    print msg

def _validate_dom(dom):
    if not dom:
        _debug("Invalid domain object")
        return False
    return True

def _validate_con(con):
    if not con:
        _debug("Invalid connection object")
        return False
    return True

'''               Connection info'''

def _estab_connection():
    conn = libvirt.open("")
    return conn

def _close_connection(conn):
    conn.close()

'''               Domain information'''

def _lookup_domain(con, name):
    try:
        dom = con.lookupByName(name)
    except libvirt.libvirtError as e:
        dom = None
        _debug(e.get_error_message())
    return dom

def _create_domain_xml(name, mem, arch, dev):
    def_xml="\
 <domain type='kvm'>\
   <name>%s</name>\
   <memory unit='KiB'>%d</memory>\
   <os>\
     <type arch='%s'>hvm</type>\
     <boot dev='%s'/>\
   </os>\
   <devices>\
     <graphics type='sdl' display=':0'/>\
   </devices>\
 </domain>\
 " %(name, mem, arch, dev)
    return def_xml

def _def_domain(conn, dom_xml):
    dom = conn.defineXML(dom_xml)
    return dom

def _undef_domain(dom):
    dom.undefine()

def _start_domain(dom):
    dom.createWithFlags(libvirt.VIR_DOMAIN_START_PAUSED)

def _shut_domain(dom):
    dom.shutdown()

def _stop_domain(dom):
    dom.destroy()

def _stop_domain_graceful(dom):
    dom.destroyFlags(libvirt.VIR_DOMAIN_DESTROY_GRACEFUL)

def _resume_domain(dom):
    dom.resume()

def _pause_domain(dom):
    None

'''               Devices'''
#vcpu
#mem

def _set_dev(dom, xml, flags=0):
    dom.attachDeviceFlags(xml, flags)

def _hp_set_dev(dom, xml):
    dom.attachDevice(xml)

def _nhp_set_dev(dom, xml):
    _set_dev(dom, xml, 0)

'''               Events & Features'''
#events
#power management flags.
#hypervisor features.

'''                              Public Interfaces'''

'''               Connection info'''

def con_init():
    con = _estab_connection()
    return con

def con_fin(con):
    if _validate_con(con):
        _close_connection(con)
        return True
    return False

'''               Domain information'''

def dom_lookup(con, name):
    dom = None
    if _validate_con(con) or name:
        dom = _lookup_domain(con, name)
    return dom

def dom_define(con, name, mem=524288, arch='i686', dev='hd'):
    dom = None
    if _validate_con(con):
        def_xml = _create_domain_xml(name, mem, arch, dev)
        if def_xml:
            dom = _def_domain(con, def_xml)
    return dom

def dom_undefine(dom):
    if _validate_dom(dom):
        _undef_domain(dom)
        return True
    return False

def dom_start(dom):
    #Start domain but in paused mode
    if _validate_dom(dom):
        _start_domain(dom)
        return True
    return False

def dom_shut(dom):
    if _validate_dom(dom):
        _shut_domain(dom)
        return True
    return False

def dom_stop(dom):
    if _validate_dom(dom):
        _stop_domain(dom)
        return True
    return False

def dom_stop_graceful(dom):
    if _validate_dom(dom):
        _stop_domain_graceful(dom)
        return True
    return False

def dom_resume(dom):
    if _validate_dom(dom):
        _resume_domain(dom)
        return True
    return False

def dom_pause(dom):
    if _validate_dom(dom):
        _pause_domain(dom)
        return True
    return False

'''     Domains utils'''
def list_domains(con):
    if not _validate_con(con):
        return False
    _debug("\nRunning domains")
    _debug(con.listDomainsID())
    _debug("\nDefined domains")
    _debug(con.listDefinedDomains())
    return True

state_names = { libvirt.VIR_DOMAIN_RUNNING  : "running",
                libvirt.VIR_DOMAIN_BLOCKED  : "idle",
                libvirt.VIR_DOMAIN_PAUSED   : "paused",
                libvirt.VIR_DOMAIN_SHUTDOWN : "in shutdown",
                libvirt.VIR_DOMAIN_SHUTOFF  : "shut off",
                libvirt.VIR_DOMAIN_CRASHED  : "crashed",
                libvirt.VIR_DOMAIN_NOSTATE  : "no state" }

def info_domain(dom):
    if not _validate_dom(dom):
        return False
    try:
        info = dom.info()
        _debug("\nDomain info")
        _debug("State: %s"%state_names[info[0]])
        _debug("Max Memory: %s"%info[1])
        _debug("Current Memory: %s"%info[2])
        _debug("Num of Current Vcpu: %s"%info[3])
        _debug("CPU time: %s"%info[4])
    except libvirt.libvirtError as e:
        _debug(e.get_error_message())
        return False
    return True


def dumpxml_domain(dom):
    if not _validate_dom(dom):
        return False
    _debug("\nActive domain xml")
    _debug(dom.XMLDesc(0))
    _debug("\nInactive domain xml")
    _debug(dom.XMLDesc(libvirt.VIR_DOMAIN_XML_INACTIVE))
    return True

'''               Devices'''

'''          vcpu'''
def set_maxVcpu(dom, vcpus):
    dom.setVcpusFlags(vcpus, libvirt.VIR_DOMAIN_VCPU_MAXIMUM)

def set_vcpu(dom, vcpus, flags=0):
    if flags:
        dom.setVcpusFlags(vcpus, flags)
    else:
        dom.setVcpusFlags(vcpus, libvirt.VIR_DOMAIN_AFFECT_CONFIG)
        dom.setVcpusFlags(vcpus, libvirt.VIR_DOMAIN_AFFECT_CURRENT)

'''          memory'''
def set_maxMem(dom, mem):
    dom.setMaxMemory(mem)

def set_mem(dom, mem, flags=0):
    if flags:
        dom.setMemoryFlags(mem, flags)
    else:
        dom.setMemoryFlags(mem, libvirt.VIR_DOMAIN_AFFECT_CONFIG)
        dom.setMemoryFlags(mem, libvirt.VIR_DOMAIN_AFFECT_CURRENT)

'''          graphics'''
def set_graphics_sdl(dom):
    xml="\
  <graphics type='sdl' display=':0.0'/>\
 "
    _nhp_set_dev(dom, xml)

