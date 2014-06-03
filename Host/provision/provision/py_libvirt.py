
import libvirt
from common import common

'''                              Internal functions'''

'''               Utility functions'''

def _debug(msg):
#    print (msg)
    pass

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

def _validate_nwk(nwk):
    if not nwk:
        _debug("Invalid network object")
        return False
    return True


'''               Connection info'''

def errorHandler(ctx, err):
    pass

def _estab_connection():
    conn = libvirt.open("")
    libvirt.registerErrorHandler(errorHandler, None)
    return conn

def _close_connection(conn):
    conn.close()

'''               Network'''

def _lookup_network(con, name):
    try:
        nwk = con.networkLookupByName(name)
    except libvirt.libvirtError as e:
        nwk = None
        _debug(e.get_error_message())
    return nwk

def _define_network(con, xml):
    nwk = con.networkDefineXML(xml)
    return nwk

def _undef_network(nwk):
    nwk.undefine()

def _start_network(nwk):
    nwk.create()

def _stop_network(nwk):
    if nwk.isActive():
        nwk.destroy()

'''               Domain information'''

def _lookup_domain(con, name):
    try:
        dom = con.lookupByName(name)
    except libvirt.libvirtError as e:
        dom = None
        _debug(e.get_error_message())
    return dom

def _create_domain_xml(name, kernel, mem, arch):
    def_xml="\
 <domain type='kvm'>\
   <name>{0}</name>\
   <memory unit='KiB'>{1}</memory>\
   <os>\
     <type arch='{2}'>hvm</type>\
     <kernel>{3}</kernel>\
     <cmdline>vga=0 root=/dev/hda</cmdline>\
     <boot dev='hd'/>\
   </os>\
   <devices>\
     <graphics type='vnc'/>\
   </devices>\
 </domain>\
 ".format(name, mem, arch, kernel)
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

def _start_resume_domain(dom):
    dom.create()

'''               Devices'''
#vcpu
#mem

def _set_dev(dom, xml, flags=0):
    dom.attachDeviceFlags(xml, flags)

def _hp_set_dev(dom, xml):
    dom.attachDevice(xml)

def _nhp_set_dev(dom, xml):
    _set_dev(dom, xml, 0)

def _hp_cdrom(dom, xml):
    dom.updateDeviceFlags(xml, 0)

'''               Interfaces'''

def _def_interface(dom, xml, flags=0):
    dom.attachDeviceFlags(xml, flags)


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

'''               Network'''

def network_lookup(con, name):
    nwk = None
    if _validate_con(con) or name:
        nwk = _lookup_network(con, name)
    return nwk

def network_defineXML(con, xml):
    nwk = _define_network(con, xml)
    return nwk

def network_define(con, nwk_name, br_name, br_mac, br_ip, d_start, d_end):
    xml="\
  <network>\
    <name>{0}</name>\
    <bridge name='{1}' stp='on' delay='0'/>\
    <mac address='{2}'/>\
    <ip address='{3}' netmask='255.255.255.0'>\
      <dhcp>\
        <range start='{4}' end='{5}'/>\
      </dhcp>\
    </ip>\
  </network>\
 ".format(nwk_name, br_name, br_mac, br_ip, d_start, d_end)
    nwk = network_defineXML(con, xml)
    return nwk

def network_undefine(nwk):
    if _validate_nwk(nwk):
        _undef_network(nwk)
        return True
    return False

def network_start(nwk):
    if _validate_nwk(nwk):
        _start_network(nwk)
        return True
    return False

def network_stop(nwk):
    if _validate_nwk(nwk):
        _stop_network(nwk)
        return True
    return False

'''     Network utils'''
def dumpxml_network(nwk):
    if not _validate_nwk(nwk):
        return ""
    return ("\nNetwork xml\n"+nwk.XMLDesc(0))

def list_network(con):
    if not _validate_con(con):
        return ""
    return ("\nRunning Network\n" + str(con.listNetworks()) +
            "\nDefined Network\n" + str(con.listDefinedNetworks()))

'''               Domain information'''

def dom_lookup(con, name):
    dom = None
    if _validate_con(con) or name:
        dom = _lookup_domain(con, name)
    return dom

def dom_define(con, name, kernel, mem=524288, arch='i686'):
    dom = None
    if _validate_con(con):
        def_xml = _create_domain_xml(name, kernel, mem, arch)
        if def_xml:
            dom = _def_domain(con, def_xml)
    return dom

def dom_defineXML(con, xml):
    dom = None
    if _validate_con(con):
        dom = _def_domain(con, xml)
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

def dom_start_resume(dom):
    #Start domain but in paused mode
    if _validate_dom(dom):
        _start_resume_domain(dom)
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
        return ""
    id_list=con.listDomainsID()
    dom_list=[con.lookupByID(id_val).name() for id_val in id_list]
    return ("\nRunning domains\n" + str(dom_list) +
            "\nDefined domains\n" + str(con.listDefinedDomains()))

state_names = { libvirt.VIR_DOMAIN_RUNNING  : "running",
                libvirt.VIR_DOMAIN_BLOCKED  : "idle",
                libvirt.VIR_DOMAIN_PAUSED   : "paused",
                libvirt.VIR_DOMAIN_SHUTDOWN : "in shutdown",
                libvirt.VIR_DOMAIN_SHUTOFF  : "shut off",
                libvirt.VIR_DOMAIN_CRASHED  : "crashed",
                libvirt.VIR_DOMAIN_NOSTATE  : "no state" }

def info_domain(dom):
    if not _validate_dom(dom):
        return ""
    try:
        info = dom.info()
        return ("\nDomain info\n" +
                "State: {}\n".format(state_names[info[0]]) +
                "Max Memory: {}\n".format(info[1]) +
                "Current Memory: {}\n".format(info[2]) +
                "Num of Current Vcpu: {}\n".format(info[3]) +
                "CPU time: {}\n".format(info[4]))
    except libvirt.libvirtError as e:
        _debug(e.get_error_message())
        return ""

def dumpxml_domain(dom):
    if not _validate_dom(dom):
        return ""
    return ("\nActive domain xml\n" + dom.XMLDesc(0) +
            "\nInactive domain xml\n" + dom.XMLDesc(libvirt.VIR_DOMAIN_XML_INACTIVE))

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

'''          raw disk'''
def attach_raw_disk_nhp(dom, path):
    xml="\
 <disk type='file' device='disk'>\
   <driver name='qemu' type='raw'/>\
   <source file='{0}'/>\
   <target dev='hda'/>\
 </disk>\
 ".format(path)
    _nhp_set_dev(dom, xml)

def attach_cdrom_hp(dom, path):
    xml="\
 <disk type='file' device='cdrom'>\
   <source file='{0}'/>\
   <target dev='hdc'/>\
   <readonly/>\
 </disk>\
 ".format(path)
    _hp_cdrom(dom, xml)

def attach_cdrom_dev_hp(dom, dev):
    xml="\
 <disk type='block' device='cdrom'>\
   <source dev='{0}'/>\
   <target dev='hdc'/>\
   <readonly/>\
 </disk>\
 ".format(path)
    _hp_cdrom(dom, xml)

def detach_cdrom_dev_hp(dom):
    xml="\
 <disk type='block' device='cdrom'>\
 <target dev='hdc' bus='ide' tray='open'/>\
 <readonly/>\
 </disk>\
 "
    _hp_cdrom(dom, xml)

def list_storage_vol(con):
    if not _validate_con(con):
        return ""
    return ("\nRunning Storage Volume\n" + str(con.listStoragePools()) +
            "\nDefined Storage Volume\n" + str(con.listDefinedStoragePools()))

'''          nwk interface'''
def attach_interface(dom, mac, dev_name):
    xml="\
  <interface type='direct'>\
    <mac address='{0}'/>\
    <source dev='{1}' mode='bridge'/>\
    <model type='virtio'/>\
  </interface>\
 ".format(mac, dev_name)
    _def_interface(dom, xml)

def attach_vs_interface(dom, mac, br_name):
    xml="\
  <interface type='bridge'>\
    <mac address='{0}'/>\
    <source bridge='{1}' />\
    <virtualport type='openvswitch' />\
    <model type='virtio'/>\
  </interface>\
 ".format(mac, br_name)
    _def_interface(dom, xml)

def list_interfaces(con):
    if not _validate_con(con):
        return ""
    return ("\nRunning Interfaces\n" + str(con.listInterfaces()) +
            "\nDefined Interfaces\n" + str(con.listDefinedInterfaces()))

'''               Other interfaces'''
def get_vncport(dom_name):
    op=common.exec_cmd_op(["virsh", "vncdisplay", dom_name])
    return ("VNC port number: {0}".format(op))
