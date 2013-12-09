#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
from common import cli_fmwk
from provision import py_libvirt
from provision import vc_commision
from provision import ssh
import inspect
import string
import os
import json
import shutil
import time

log_file=None

class provisionError(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

def complete_dom(text, line, begidx, endidx):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    comp_type=cli_fmwk.autocomp(['domain'], text)

    args=line.split()
    if len(args) == 2 and line[-1] == ' ':
        #Second level.
        if args[1]=='domain':
            print("<domain name>")
            comp_type=['']
    return comp_type

def complete_network(text, line, begidx, endidx):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    comp_type=cli_fmwk.autocomp(['network'], text)

    args=line.split()
    if len(args) == 2 and line[-1] == ' ':
        #Second level.
        if args[1]=='network':
            print("<network name>")
            comp_type=['']
    return comp_type

def complete_nwk_dom(text, line, begidx, endidx):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    comp_type=cli_fmwk.autocomp(['domain', 'network'], text)

    args=line.split()
    if len(args) == 2 and line[-1] == ' ':
        #Second level.
        if args[1]=='domain':
            print("<domain name>")
            comp_type=['']
        if args[1]=='network':
            print("<network name>")
            comp_type=['']
    return comp_type

class provCLI(cli_fmwk.VCCli):
    def __init__(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="virtcluster provision cli")
        self.def_comp_lst=['domain', 'network']

    def postloop(self):
        py_libvirt.con_fin(self._con)
    def preloop(self):
        self._con = py_libvirt.con_init()

    def do_domain(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        dom_cli=provCLI_domain(self._con)
        dom_cli.cmdloop()

    def help_domain(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Domain subcommands    ")

    def do_network(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        nwk_cli=provCLI_network(self._con)
        nwk_cli.cmdloop()

    def help_network(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Network subcommands    ")

    def do_info(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_info()
            return

        comp_type=cli_fmwk.autocomp(['domain'], arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            s=py_libvirt.info_domain(dom)
            print(s)
        else:
            print("Enter domain")
            return

    def help_info(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Info domain <domain name>    ")

    def complete_info(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_list(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        s = py_libvirt.list_domains(self._con)
        print (s)
        #network
    def help_list(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     List domains    ")

    def do_dumpxml(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_dumpxml()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            s = py_libvirt.dumpxml_domain(dom)
            print(s)
        elif comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            s=py_libvirt.dumpxml_network(nwk)
            print(s)
        else:
            print("Enter either domain or network")
            return

    def help_dumpxml(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Dump XML of either:      ")
        print("      domain <domain name>    ")
        print("             or               ")
        print("      network <network name>  ")

    def complete_dumpxml(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

class provCLI_domain(cli_fmwk.VCCli):
    def __init__(self, con):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="Domain subcommands")
        self.prompt = self.prompt[:-1]+':Domain)'
        self.def_comp_lst=['domain']
        self._con = con

    def _dom_xml_comp(self, val):
        xml="\
            <domain type='kvm'>\
              <name>$domain</name>\
              <memory unit='KiB'>$memory</memory>\
              <currentMemory unit='KiB'>$memory</currentMemory>\
              <vcpu placement='static'>$vcpu</vcpu>\
              <os>\
                <type arch='$arch' machine='pc-1.1'>hvm</type>\
                <kernel>$kernel</kernel>\
                <cmdline>vga=0 root=/dev/hda</cmdline>\
                <boot dev='hd'/>\
              </os>\
              <clock offset='utc'/>\
              <on_poweroff>destroy</on_poweroff>\
              <on_reboot>restart</on_reboot>\
              <on_crash>destroy</on_crash>\
              <devices>\
                <emulator>/usr/bin/kvm</emulator>\
                <disk type='file' device='disk'>\
                  <driver name='qemu' type='raw'/>\
                  <source file='$rootfs'/>\
                  <target dev='hda' bus='ide'/>\
                </disk>\
                <interface type='network'>\
                  <mac address='$fab0_dom_mac'/>\
                  <source network='$fab0_net_name'/>\
                  <target dev='$fab0_net_dev'/>\
                  <model type='virtio'/>\
                </interface>\
                <graphics type='vnc' port='$vnc_port' autoport='yes'/>\
              </devices>\
              <seclabel type='none'/>\
            </domain>\
"
        xmlT=""
        try:
            xmlT=string.Template(xml).substitute(val)
        except Exception as e:
            raise provisionError("Domain define invalid arguments {0}".format(e))
        return xmlT

    def do_define(self, args):
        global log_file

        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        common.log([common.info, common.lfile, log_file],
                   "\nDomain define args {0}".format(args))

        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if dom:
                print("Domain already defined")
                return
        else:
            print("Enter domain ")
            return

        common.log([common.info, common.lfile, log_file],
                   "\nDomain name {0}".format(dom_name))

        #Get fabric network details and update arg_d
        j_dict={}

        net_fname="{0}.net".format(dom_name)
        net_file = os.path.join("net", net_fname)
        with open(net_file, 'r') as f:
            j_dict=json.load(f)

        arg_d['fab0_dom_mac']=j_dict['fab0_dom_mac']

        common.log([common.info, common.lfile, log_file],
                   "\nDomain mac {0}".format(arg_d['fab0_dom_mac']))

        j_dict={}

        fab_fname="fab0_host.net"
        fab_file = os.path.join("net", fab_fname)
        with open(fab_file, 'r') as f:
            j_dict=json.load(f)

        arg_d['fab0_net_name']=j_dict['fab0_net_name']
        arg_d['fab0_net_dev']=j_dict['fab0_net_dev']

        #Request for vnc port auto allocation
        arg_d['vnc_port']='-1'

        common.log([common.info, common.lfile, log_file],
                   "\nDomain net {0} dev {1} \n".format
                   (arg_d['fab0_net_name'], arg_d['fab0_net_dev']))

        img_name=arg_d['image']
        common.log([common.info, common.lfile, log_file],
                   "\nImage name {0} \n".format(img_name))

        if img_name:
            img_dir="provisioned_domain/{}/images".format(dom_name)
            common.log([common.info, common.lfile, log_file],
                       "\nImage dir {0} \n".format(img_dir))
            os.makedirs(img_dir)
            img_tgz=os.path.join("./images",
                                 "virtcluster-image-{}.tgz".format(img_name))
            op=common.exec_cmd_op(["tar", "zxvf", img_tgz, "-C", img_dir])
            common.log([common.info, common.lfile, log_file], op)
        else:
            print("Enter Image")
            return

        img_dir=os.path.join(os.getcwd(),
                  "provisioned_domain/{}/images/{}".format(dom_name, img_name))
        common.log([common.info, common.lfile, log_file],
                   "\nProvisioned domain Image dir {0} \n".format(img_dir))

        with open(os.path.join(img_dir,"manifest")) as infile:
            img_desc = json.load(infile)

        arg_d['kernel']=os.path.join(img_dir, img_desc['kernel'])
        arg_d['rootfs']=os.path.join(img_dir, img_desc['fs_raw'])
        common.log([common.info, common.lfile, log_file],
                   "\nkernel {0} rootfs {1}\n".format(arg_d['kernel'], arg_d['rootfs']))

        xml = self._dom_xml_comp(arg_d)
        common.log([common.info, common.lfile, log_file], xml)
        dom = py_libvirt.dom_defineXML(self._con, xml)

    def help_define(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Define domain <domain name>    ")

    def complete_define(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_commision(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))
        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            s=py_libvirt.info_domain(dom)
            if not "State: running" in s:
                print("Domain not running")
                return
        else:
            print("Enter domain ")
            return

        comi_dir=os.path.join(os.getcwd(), "commisioned_domain")
        net_dir=os.path.join(os.getcwd(), "net")
        common.log([common.info, common.lfile, log_file],
                   "\nCommision start\n")
        vc_commision.start(comi_dir, net_dir, arg_d, log_file)

    def help_commision(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Start domain <domain name>  ")

    def complete_commision(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_undefine(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        nopurge=False
        if 'nopurge' in args:
            nopurge=True
            args=args.replace('nopurge', '')

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            dom = py_libvirt.dom_undefine(dom)
            if not nopurge:
                common.log([common.info, common.lfile, log_file],
                           "\nPurge selected")
                shutil.rmtree(os.path.join("provisioned_domain", dom_name),
                              True)
                shutil.rmtree(os.path.join("commisioned_domain", dom_name),
                              True)
                comi_dir=os.path.join(os.getcwd(), "commisioned_domain")
                net_dir=os.path.join(os.getcwd(), "net")
                common.log([common.info, common.lfile, log_file],
                           "\nCommision cleanup")
                vc_commision.cleanup(dom_name, comi_dir, net_dir, log_file)
        else:
            print("Enter domain")
            return

    def help_undefine(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Undefine domain <domain name>    ")

    def complete_undefine(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

    def do_start(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nDomain {0} started at {1}".format(dom_name, time.asctime()))
            py_libvirt.dom_start(dom)
        else:
            print("Enter domain")
            return

    def help_start(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Start domain <domain name>    ")

    def complete_start(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

    def do_stop(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nDomain {0} stopped at {1}".format(dom_name, time.asctime()))
            py_libvirt.dom_stop(dom)
        else:
            print("Enter either domain or network")
            return

    def help_stop(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Stop domain <domain name>    ")

    def complete_stop(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

    def do_shut(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_shut()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nDomain {0} shut at {1}".format(dom_name, time.asctime()))
            py_libvirt.dom_shut(dom)
        else:
            print("Enter domain")
            return

    def help_shut(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Shut domain <domain name>    ")

    def complete_shut(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_pause(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_pause()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nDomain {0} paused at {1}".format(dom_name, time.asctime()))
            py_libvirt.dom_pause(dom)
        else:
            print("Enter domain")
            return

    def help_pause(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Pause domain <domain name>    ")

    def complete_pause(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_resume(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_resume()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nDomain {0} resumed at {1}".format(dom_name, time.asctime()))
            py_libvirt.dom_resume(dom)
        else:
            print("Enter domain")
            return

    def help_resume(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Resume domain <domain name>    ")

    def complete_resume(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

class provCLI_dhcp(cli_fmwk.VCCli):
    def __init__(self, arg_d):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        self.arg_d=arg_d
        cli_fmwk.VCCli.__init__(self, intro="DHCP subcommands")
        self.prompt = self.prompt[:-1]+':dhcp)'

    def do_range(self, args):
        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        self.arg_d['dhcp_start']=t_dict['start']
        self.arg_d['dhcp_end']=t_dict['end']
        common.log([common.info, common.lfile, log_file],
                   "\nDHCP range starting {0} end {1}".format(self.arg_d['dhcp_start'], self.arg_d['dhcp_end']))

    def help_range(self, args):
        pass
    def complete_range(self, args):
        pass

    def do_host(self, args):
        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        host_xml="<host mac='$mac' name='$name' ip='$ip'/>\ \n"
        hostT=string.Template(host_xml).substitute(t_dict)
        common.log([common.info, common.lfile, log_file],
                   "\nDHCP host entry {0}".format(hostT))

        if 'host' in self.arg_d:
            self.arg_d['host']=self.arg_d['host']+hostT
        else:
            self.arg_d['host']=hostT

        #Store domain net configs in net directory
        j_dict={}
        j_dict['fab0_dom_name']=t_dict['name']
        j_dict['fab0_dom_ip']=t_dict['ip']
        j_dict['fab0_dom_mac']=t_dict['mac']

        net_fname="{0}.net".format(t_dict['name'])
        net_file = os.path.join("net", net_fname)
        with open(net_file, 'w') as f:
            json.dump(j_dict, f)

    def help_host(self, args):
        pass
    def complete_host(self, args):
        pass

class provCLI_network_define(cli_fmwk.VCCli):
    def __init__(self, arg_d):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        self.arg_d=arg_d
        cli_fmwk.VCCli.__init__(self, intro="Network define subcommands")
        self.prompt = self.prompt[:-1]+':Network {0})'.format(arg_d['network'])
        if self.arg_d['network']=='fabric':
            self.is_fabric=True
            self.arg_d['network']='virtcluster_fabric0'
            common.log([common.info, common.lfile, log_file],
                       "\nFabric network define")

    def do_bridge(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        if self.is_fabric:
            self.arg_d['brname']='virfab0'
        else:
            self.arg_d['brname']=t_dict['name']
        self.arg_d['ip_addr']=t_dict['ip']
        self.arg_d['netmask']=t_dict['netmask']

        common.log([common.info, common.lfile, log_file],
                   "\nBridge name {0}, ip, netmask".format(
                self.arg_d['brname'], self.arg_d['ip_addr'], self.arg_d['netmask']))

        #Store host configs in net directory
        j_dict={}
        j_dict['fab0_net_name']=self.arg_d['network']
        j_dict['fab0_host_net_ip']=t_dict['ip']
        j_dict['fab0_net_dev']='vfab0'

        net_fname="fab0_host.net"
        net_file = os.path.join("net", net_fname)
        with open(net_file, 'w') as f:
            json.dump(j_dict, f)

    def help_bridge(self, args):
        pass
    def complete_bridge(self, args):
        pass
    def do_dhcp(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        dhcp_cli=provCLI_dhcp(self.arg_d)
        dhcp_cli.cmdloop()

    def help_dhcp(self, args):
        pass
    def complete_dhcp(self, args):
        pass

class provCLI_network(cli_fmwk.VCCli):
    def __init__(self, con):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="Network subcommands")
        self.prompt = self.prompt[:-1]+':Network)'
        self.def_comp_lst=['network']
        self._con = con

    def _nwk_xml_comp(self, val):
        xml="\
           <network>\
             <name>$network</name>\
             <bridge name='$brname' stp='on' delay='0' />\
             <ip address='$ip_addr' netmask='$netmask'>\
               <dhcp>\
                 <range start='$dhcp_start' end='$dhcp_end' />\
                 $host \
               </dhcp>\
             </ip>\
           </network>\
"
        xmlT=""
        try:
            xmlT=string.Template(xml).substitute(val)
        except Exception as e:
            raise provisionError("Network define invalid arguments {0}".format(e))
        return xmlT

    def do_define(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        nwk_name = arg_d['network']
        if nwk_name:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if nwk:
                print("Network already defined")
                return
        else:
            print("Enter network")
            return

        common.log([common.info, common.lfile, log_file],
                   "\nNetwork {0} define at {1}".format(nwk_name, time.asctime()))

        nwk_def_cli=provCLI_network_define(arg_d)
        nwk_def_cli.cmdloop()

        xml = self._nwk_xml_comp(arg_d)
        common.log([common.info, common.lfile, log_file], xml)
        nwk = py_libvirt.network_defineXML(self._con, xml)

    def help_define(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Define network <network name>  ")

    def complete_define(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        return complete_network(text, line, begidx, endidx)

    def do_undefine(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nNetwork undefine args {0}".format(nwk_name))
            nwk = py_libvirt.network_undefine(nwk)
        else:
            print("Enter network")
            return

    def help_undefine(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Undefine network <network name>  ")

    def complete_undefine(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_network(text, line, begidx, endidx)

    def do_start(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nNetwork {0} start at {1}".format(nwk_name, time.asctime()))
            py_libvirt.network_start(nwk)
        else:
            print("Enter network")
            return

    def help_start(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Start network <network name>  ")

    def complete_start(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_network(text, line, begidx, endidx)

    def do_stop(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            common.log([common.info, common.lfile, log_file],
                       "\nNetwork {0} stop at {1}".format(nwk_name, time.asctime()))
            py_libvirt.network_stop(nwk)
        else:
            print("Enter network")
            return

    def help_stop(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Stop network <network name>  ")

    def complete_stop(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return complete_network(text, line, begidx, endidx)

def prep_provision():
    global log_file
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    try:
        os.mkdir("logs")
    except OSError:
        pass

    log_file=open(os.path.join("logs", "provision.log"), 'a+')

    common.log([common.info, common.lfile, log_file],
               "\nProvision initiated on {0}".format(time.asctime()))

def cleanup_provision():
    global log_file
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    log_file.close()

def main():
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    #common.set_debug_lvl(common.debug)

    prep_provision()

    try:
        os.mkdir("provisioned_domain")
        common.log([common.info, common.lfile, log_file],
                   "\nprovisioned_domain directory created")
        os.mkdir("commisioned_domain")
        common.log([common.info, common.lfile, log_file],
                   "\ncommisioned_domain directory created")
        os.mkdir("net")
        common.log([common.info, common.lfile, log_file],
                   "\nnet directory created")
    except OSError:
        pass

    try:
        prov_cmd=provCLI()
        prov_cmd.cmdloop()
    except common.execCmdError as e:
        common.log([common.error, common.lfile, log_file],
                   "Error {0}".format(e))
    except provisionError as e:
        common.log([common.error, common.lfile, log_file],
                   "Error {0}".format(e))
    except vc_commision.commisionError as e:
        common.log([common.error, common.lfile, log_file],
                   "Error {0}".format(e))
    except ssh.sshError as e:
        common.log([common.error, common.lfile, log_file],
                   "Error {0}".format(e))
    except IOError as e:
        common.log([common.error, common.lfile, log_file],
                   "Error {0}".format(e))
    except OSError as e:
        common.log([common.error, common.lfile, log_file],
                   "Error {0}".format(e))

    cleanup_provision()

if __name__=='__main__':
    main()
