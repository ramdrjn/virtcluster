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
import logging
import logging.handlers
import urlparse

logger=None

class provisionError(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

def complete_dom(text, line, begidx, endidx):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    comp_type=cli_fmwk.autocomp(['domain'], text)

    args=line.split()
    if len(args) == 2 and line[-1] == ' ':
        #Second level.
        if args[1]=='domain':
            print("<domain name>")
            comp_type=['']
    return comp_type

def complete_network(text, line, begidx, endidx):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    comp_type=cli_fmwk.autocomp(['network'], text)

    args=line.split()
    if len(args) == 2 and line[-1] == ' ':
        #Second level.
        if args[1]=='network':
            print("<network name>")
            comp_type=['']
    return comp_type

def complete_nwk_dom(text, line, begidx, endidx):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

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

def complete_nwk_dom_ifc(text, line, begidx, endidx):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    comp_type=cli_fmwk.autocomp(['domain', 'network', 'interface'], text)

    args=line.split()
    if len(args) == 2 and line[-1] == ' ':
        #Second level.
        if args[1]=='domain':
            print("<domain name>")
            comp_type=['']
        if args[1]=='network':
            print("<network name>")
            comp_type=['']
        if args[1]=='interface':
            print("<interface name>")
            comp_type=['']
    return comp_type

def error_log_print(msg):
    logger.error(msg)
    print(msg)

def _iso_prep(dom, pm_group):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))
    logger.info("Packgage group file {0}".format(pm_group))

    d={}
    with open(pm_group) as f:
        d=json.load(f)
    if not 'main' in d:
        raise provisionError("'main' repository not defined in package group")
    main_d=d['main']
    if 'iso' in main_d:
        logger.info("Attaching iso to dom")
        py_libvirt.attach_cdrom_hp(dom, main_d['iso'])
    elif 'dev' in main_d:
        logger.info("Attaching cdrom device to dom")
        py_libvirt.attach_cdrom_dev_hp(dom, main_d['dev'])

def _cdrom_eject(dom):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))
    py_libvirt.detach_cdrom_dev_hp(dom)

def _host_network_store(name, ip, mac):
    #Store domain net configs in net directory
    j_dict={}
    j_dict['fab0_dom_name']=name
    j_dict['fab0_dom_ip']=ip
    j_dict['fab0_dom_mac']=mac

    net_fname="{0}.net".format(name)
    net_file = os.path.join("net", net_fname)
    logger.info("Generating domain networking file {0}".format(net_file))
    with open(net_file, 'w') as f:
        json.dump(j_dict, f)

class provCLI(cli_fmwk.VCCli):
    def __init__(self):
        logger.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="virtcluster provision cli")
        self.def_comp_lst=['domain', 'network']

    def postloop(self):
        py_libvirt.con_fin(self._con)
    def preloop(self):
        self._con = py_libvirt.con_init()

    def do_domain(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        dom_cli=provCLI_domain(self._con)
        dom_cli.cmdloop()

    def help_domain(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Domain subcommands    ")

    def do_network(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        nwk_cli=provCLI_network(self._con)
        nwk_cli.cmdloop()

    def help_network(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Network subcommands    ")

    def do_commision(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        com_cli=provCLI_commision(self._con)
        com_cli.cmdloop()

    def help_commision(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Commision subcommands    ")

    def do_info(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_info()
            return

        comp_type=cli_fmwk.autocomp(['domain'], arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            s=py_libvirt.info_domain(dom)
            print(s)
            s=py_libvirt.get_vncport(dom_name)
            print(s)
        else:
            print("Enter domain")
            return

    def help_info(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Info domain <domain name>    ")

    def complete_info(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_list(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("\nDomain:")
        print ("-------")
        s = py_libvirt.list_domains(self._con)
        print (s)
        print ("\nNetwork:")
        print ("--------")
        s = py_libvirt.list_network(self._con)
        new_s=s.replace('virtcluster_fabric0', 'fabric')
        print (new_s)
        print ("\nInterfaces:")
        print ("-----------")
        s = py_libvirt.list_interfaces(self._con)
        print (s)
        print ("\nStorage Volume:")
        print ("---------------")
        s = py_libvirt.list_storage_vol(self._con)
        print (s)
    def help_list(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     List domains    ")

    def do_dumpxml(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_dumpxml()
            return

        comp_lst=['domain', 'network', 'interface']
        comp_type=cli_fmwk.autocomp(comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            s = py_libvirt.dumpxml_domain(dom)
            print(s)
        elif comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                error_log_print("Network not defined")
                return
            s=py_libvirt.dumpxml_network(nwk)
            print(s)
        elif comp_type==['interface']:
            ifc_name=arg_lst[1]
            ifc = py_libvirt.host_interfaces_lookup(self._con, ifc_name)
            if not ifc:
                error_log_print("Interface not defined")
                return
            s=py_libvirt.dumpxml_network(ifc)
            print(s)
        else:
            print("Enter domain, network or interface")
            return

    def help_dumpxml(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Dump XML of either:          ")
        print("      domain <domain name>        ")
        print("             or                   ")
        print("      network <network name>      ")
        print("             or                   ")
        print("      interface <interface name>  ")

    def complete_dumpxml(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom_ifc(text, line, begidx, endidx)

class provCLI_domain(cli_fmwk.VCCli):
    def __init__(self, con):
        logger.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Domain subcommands")
        self.prompt = self.prompt[:-1]+':Domain)'
        self.def_comp_lst=['domain']
        self._con = con

    def _dom_xml_comp(self, val):
        '''
        <interface type='network'>\
        <mac address='$fab0_dom_mac'/>\
        <source network='$fab0_net_name'/>\
        <model type='virtio'/>\
        </interface>\
        '''
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
                <disk type='block' device='cdrom'>\
                  <target dev='hdc' bus='ide' tray='open'/>\
                  <readonly/>\
                </disk>\
                <graphics type='vnc' port='$vnc_port' autoport='yes'/>\
              </devices>\
              <seclabel type='none'/>\
            </domain>\
"
        xmlT=string.Template(xml).substitute(val)
        return xmlT

    def do_define(self, args):
        global logger

        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        logger.debug("Domain define args {0}".format(args))

        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if dom:
                error_log_print("Domain already defined")
                return
        else:
            print("Enter domain ")
            return

        logger.info("Domain name {0}".format(dom_name))

        #Request for vnc port auto allocation
        arg_d['vnc_port']='-1'

        img_name=arg_d['image']
        logger.info("Image name {0} ".format(img_name))

        if img_name:
            img_dir="provisioned_domain/{}/images".format(dom_name)
            logger.info("Image dir {0}".format(img_dir))
            os.makedirs(img_dir)
            logger.debug("Extracting image tar")
            img_tgz=os.path.join("./images",
                                 "virtcluster-image-{}.tgz".format(img_name))
            op=common.exec_cmd_op(["tar", "zxvf", img_tgz, "-C", img_dir])
            logger.info(op)
        else:
            print("Enter Image")
            return

        img_dir=os.path.join(os.getcwd(),
                  "provisioned_domain/{}/images/{}".format(dom_name, img_name))
        logger.info("Provisioned domain Image dir {0}".format(img_dir))

        logger.debug("Accessing manifest file")
        with open(os.path.join(img_dir, "manifest")) as infile:
            img_desc = json.load(infile)

        arg_d['kernel']=os.path.join(img_dir, img_desc['kernel'])
        arg_d['rootfs']=os.path.join(img_dir, img_desc['fs_raw'])
        logger.info("kernel {0} rootfs {1}".format(arg_d['kernel'],
                                                   arg_d['rootfs']))

        logger.debug("Forming domain xml from template")
        xml = self._dom_xml_comp(arg_d)
        logger.info(xml)
        logger.debug("Defining domain")
        dom = py_libvirt.dom_defineXML(self._con, xml)

    def help_define(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Define domain <domain name>    ")

    def complete_define(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_undefine(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain undefine args {0}".format(args))

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
                error_log_print("Domain not defined")
                return
            dom = py_libvirt.dom_undefine(dom)
            if not nopurge:
                logger.info("Purge selected")
                shutil.rmtree(os.path.join("provisioned_domain", dom_name),
                              True)
                shutil.rmtree(os.path.join("commisioned_domain", dom_name),
                              True)
                comi_dir=os.path.join(os.getcwd(), "commisioned_domain")
                net_dir=os.path.join(os.getcwd(), "net")
                logger.debug("Commision cleanup")
                vc_commision.cleanup(dom_name, comi_dir, net_dir)
        else:
            print("Enter domain")
            return

    def help_undefine(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Undefine domain <domain name>    ")

    def complete_undefine(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

    def do_start(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain start args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            logger.info("Domain {0} started".format(dom_name))
            py_libvirt.dom_start(dom)
        else:
            print("Enter domain")
            return

    def help_start(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Start domain <domain name>    ")

    def complete_start(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

    def do_stop(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain stop args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            logger.info("Domain {0} stopped".format(dom_name))
            py_libvirt.dom_stop(dom)
        else:
            print("Enter domain")
            return

    def help_stop(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Stop domain <domain name>    ")

    def complete_stop(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_nwk_dom(text, line, begidx, endidx)

    def do_shut(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain shut args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_shut()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            logger.info("Domain {0} shut".format(dom_name))
            py_libvirt.dom_shut(dom)
        else:
            print("Enter domain")
            return

    def help_shut(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Shut domain <domain name>    ")

    def complete_shut(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_pause(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain pause args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_pause()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            logger.info("Domain {0} paused".format(dom_name))
            py_libvirt.dom_pause(dom)
        else:
            print("Enter domain")
            return

    def help_pause(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Pause domain <domain name>    ")

    def complete_pause(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_resume(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain resume args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_resume()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            logger.info("Domain {0} resumed".format(dom_name))
            py_libvirt.dom_resume(dom)
        else:
            print("Enter domain")
            return

    def help_resume(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Resume domain <domain name>    ")

    def complete_resume(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_host(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Host args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 8:
            self.help_interface()
            return

        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        dom = None
        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
        else:
            print("Enter domain")
            return

        #Get fabric network details and update arg_d
        j_dict={}

        fab_fname="fab0_host.net"
        fab_file = os.path.join("net", fab_fname)
        logger.info("Fabric network file name {0}".format(fab_file))
        with open(fab_file, 'r') as f:
            j_dict=json.load(f)

        arg_d['br']=j_dict['fab0_br_name']

        _host_network_store(arg_d['name'], arg_d['ip'], arg_d['mac'])
        py_libvirt.attach_vs_interface(dom, arg_d['mac'], arg_d['br'])

    def help_host(self, args):
        pass
    def complete_host(self, args):
        pass

    def do_interface(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain add interface args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 6:
            self.help_interface()
            return

        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            py_libvirt.attach_interface(dom, arg_d['mac'], arg_d['dev'])
        else:
            print("Enter domain")
            return

    def help_interface(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Interface add to domain <domain name>    ")

    def complete_interface(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_migrate(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Domain migrate args {0}".format(args))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_d['domain']
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            logger.info("Domain {0} started".format(dom_name))
            py_libvirt.migrate(dom, arg_d['duri'], False, False, False)
        else:
            print("Enter domain")
            return

    def help_migrate(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Migrate domain <domain name>    ")

    def complete_migrate(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

class provCLI_dhcp(cli_fmwk.VCCli):
    def __init__(self, arg_d):
        logger.debug("Initialized {0} class".format(self.__class__))
        self.arg_d=arg_d
        cli_fmwk.VCCli.__init__(self, intro="DHCP subcommands")
        self.prompt = self.prompt[:-1]+':dhcp)'

    def do_range(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Dhcp range args {0}".format(args))

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        self.arg_d['dhcp_start']=t_dict['start']
        self.arg_d['dhcp_end']=t_dict['end']
        logger.info("DHCP range starting {0} end {1}".format(
                self.arg_d['dhcp_start'], self.arg_d['dhcp_end']))

    def help_range(self, args):
        pass
    def complete_range(self, args):
        pass

    def do_host(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Dhcp host args {0}".format(args))

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        host_xml="<host mac='$mac' name='$name' ip='$ip'/>\ \n"
        logger.debug("Generating host xml")
        hostT=string.Template(host_xml).substitute(t_dict)
        logger.info("DHCP host entry {0}".format(hostT))

        if 'host' in self.arg_d:
            self.arg_d['host']=self.arg_d['host']+hostT
        else:
            self.arg_d['host']=hostT
        logger.debug("Full host enteries {0}".format(self.arg_d['host']))
        _host_network_store(t_dict['name'], t_dict['ip'], t_dict['mac'])

    def help_host(self, args):
        pass
    def complete_host(self, args):
        pass

class provCLI_network_define(cli_fmwk.VCCli):
    def __init__(self, arg_d, con):
        logger.debug("Initialized {0} class".format(self.__class__))
        self.arg_d=arg_d
        cli_fmwk.VCCli.__init__(self, intro="Network define subcommands")
        self.prompt = self.prompt[:-1]+':Network {0})'.format(arg_d['network'])
        if self.arg_d['network']=='fabric':
            self.is_fabric=True
            self.arg_d['network']='virtcluster_fabric0'
            logger.info("Fabric network define")
        self._con=con

    def do_bridge(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Bridge args {0}".format(args))

        self.arg_d['vs']=False
        if 'vs' in args:
            args=args.replace('vs', '')
            self.arg_d['vs']=True

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        if self.is_fabric:
            if self.arg_d['vs']:
                self.arg_d['brname']=t_dict['name']
            else:
                self.arg_d['brname']='virfab0'
        else:
            self.arg_d['brname']=t_dict['name']
        self.arg_d['ip_addr']=t_dict['ip']
        self.arg_d['netmask']=t_dict['netmask']

        logger.info("Bridge name {0}, ip {1}, netmask {2}".format(
                self.arg_d['brname'], self.arg_d['ip_addr'],
                self.arg_d['netmask']))

        #Configure the host interface.
        py_libvirt.host_interface_up(self._con,
                                     self.arg_d['brname'],
                                     self.arg_d['ip_addr'],
                                     self.arg_d['netmask'])

        #Store host configs in net directory
        j_dict={}
        j_dict['fab0_net_name']=self.arg_d['network']
        j_dict['fab0_host_net_ip']=t_dict['ip']
        j_dict['fab0_br_name']=self.arg_d['brname']

        if self.is_fabric:
            net_fname="fab0_host.net"
        else:
            net_fname=self.arg_d['network']

        net_file = os.path.join("net", net_fname)
        logger.debug("Accessing network file {0}".format(net_file))
        with open(net_file, 'w') as f:
            json.dump(j_dict, f)

    def help_bridge(self, args):
        pass
    def complete_bridge(self, args):
        pass
    def do_dhcp(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        dhcp_cli=provCLI_dhcp(self.arg_d)
        dhcp_cli.cmdloop()

    def help_dhcp(self, args):
        pass
    def complete_dhcp(self, args):
        pass
    def do_host(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Host args {0}".format(args))

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))
        _host_network_store(t_dict['name'], t_dict['ip'], t_dict['mac'])

    def help_host(self, args):
        pass
    def complete_host(self, args):
        pass

class provCLI_network(cli_fmwk.VCCli):
    def __init__(self, con):
        logger.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Network subcommands")
        self.prompt = self.prompt[:-1]+':Network)'
        self.def_comp_lst=['network']
        self._con = con

    def _nwk_xml_comp(self, val):
        if val['vs']:
            xml="\
             <network>\
               <name>$network</name>\
               <forward mode='bridge'/>\
               <bridge name='$brname' />\
               <virtualport type='openvswitch'/>\
             </network>\
"
        else:
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
        xmlT=string.Template(xml).substitute(val)
        return xmlT

    def do_define(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Network args {0}".format(args))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        nwk_name = arg_d['network']
        if nwk_name:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if nwk:
                error_log_print("Network already defined")
                return
        else:
            print("Enter network")
            return

        logger.info("Network {0} define".format(nwk_name))

        nwk_def_cli=provCLI_network_define(arg_d, self._con)
        nwk_def_cli.cmdloop()

        '''
        logger.debug("Generating network xml".format(nwk_name))
        xml = self._nwk_xml_comp(arg_d)
        logger.info(xml)
        nwk = py_libvirt.network_defineXML(self._con, xml)
        '''

    def help_define(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Define network <network name>  ")

    def complete_define(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        return complete_network(text, line, begidx, endidx)

    def do_undefine(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Network undefine args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            if nwk_name=='fabric':
                nwk_name='virtcluster_fabric0'
                logger.debug("Fabric network")
            '''
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                error_log_print("Network not defined")
                return
            logger.info("Network {0} undefine".format(nwk_name))
            nwk = py_libvirt.network_undefine(nwk)
            '''
        else:
            print("Enter network")
            return

    def help_undefine(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Undefine network <network name>  ")

    def complete_undefine(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_network(text, line, begidx, endidx)

    def do_start(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Network start args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            if nwk_name=='fabric':
                nwk_name='virtcluster_fabric0'
                logger.debug("Fabric network")
            '''
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                error_log_print("Network not defined")
                return
            logger.info("Network {0} start".format(nwk_name))
            py_libvirt.network_start(nwk)
            '''
        else:
            print("Enter network")
            return

    def help_start(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Start network <network name>  ")

    def complete_start(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_network(text, line, begidx, endidx)

    def do_stop(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Network stop args {0}".format(args))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.autocomp(self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            if nwk_name=='fabric':
                nwk_name='virtcluster_fabric0'
                logger.debug("Fabric network")
            '''
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                error_log_print("Network not defined")
                return
            logger.info("Network {0} stop".format(nwk_name))
            py_libvirt.network_stop(nwk)
            '''
        else:
            print("Enter network")
            return

    def help_stop(self):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Stop network <network name>  ")

    def complete_stop(self, text, line, begidx, endidx):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_network(text, line, begidx, endidx)

class provCLI_package(cli_fmwk.VCCli):
    def __init__(self, arg_d):
        logger.debug("Initialized {0} class".format(self.__class__))

        self.arg_d=arg_d
        cli_fmwk.VCCli.__init__(self, intro="Package group subcommands")
        self.prompt = self.prompt[:-1]+':pkg-grp {0})'.format(arg_d['group'])

    def __del__(self):
        logger.debug("Finalized {0} class".format(self.__class__))

    def do_manager(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Manager args {0}".format(args))

        self.arg_d['manager']=args.strip()
        logger.info("Package Manager {0}".format(self.arg_d['manager']))

    def help_manager(self, args):
        pass
    def complete_manager(self, args):
        pass

    def do_main(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Package main args {0}".format(args))

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))

        main_dict={}

        url=urlparse.urlparse(t_dict['url'])
        if url.scheme == 'file':
            main_dict['url']=url.path

            if 'iso' in t_dict:
                iso_url=urlparse.urlparse(t_dict['iso'])
                if iso_url.scheme == 'file':
                    main_dict['iso']=iso_url.path
                else:
                    main_dict['iso']=t_dict['iso']
                logger.info("ISO url {0}".format(main_dict['iso']))

            if 'dev' in t_dict:
                main_dict['dev']=t_dict['dev']
                logger.info("Dev {0}".format(main_dict['dev']))
        else:
            main_dict['url']=t_dict['url']

        self.arg_d['main']=main_dict

        logger.info("Main url {0}".format(main_dict['url']))

    def help_main(self, args):
        pass
    def complete_main(self, args):
        pass

    def do_update(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        logger.debug("Package update args {0}".format(args))

        t_dict=args.split()
        t_dict = dict(zip(t_dict[::2], [t_dict[i]
                                        for i in range(1, len(t_dict), 2)]))

        update_dict={}

        url=urlparse.urlparse(t_dict['url'])
        if url.scheme == 'file':
            update_dict['url']=url.path

            if 'iso' in t_dict:
                iso_url=urlparse.urlparse(t_dict['iso'])
                if iso_url.scheme == 'file':
                    update_dict['iso']=iso_url.path
                else:
                    update_dict['iso']=t_dict['iso']
                logger.info("ISO url {0}".format(update_dict['iso']))

            if 'dev' in t_dict:
                update_dict['dev']=t_dict['dev']
                logger.info("Dev {0}".format(update_dict['dev']))
        else:
            update_dict['url']=t_dict['url']

        self.arg_d['update']=update_dict

        logger.info("Update url {0}".format(update_dict['url']))

    def help_update(self, args):
        pass
    def complete_update(self, args):
        pass

class provCLI_commision(cli_fmwk.VCCli):
    def __init__(self, con):
        logger.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Commisioning")
        self.prompt = self.prompt[:-1]+':Commision)'
        self._con=con

    def do_initialize(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        logger.debug("Initialize args {0}".format(args))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))
        dom=None
        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                error_log_print("Domain not defined")
                return
            s=py_libvirt.info_domain(dom)
            if not "State: running" in s:
                error_log_print("Domain not running")
                return
        else:
            print("Enter domain ")
            return

        comi_dir=os.path.join(os.getcwd(), "commisioned_domain")
        dat_dir = os.path.join(comi_dir, "dat")
        net_dir=os.path.join(os.getcwd(), "net")

        pm_group_fname="{0}.pg".format(arg_d['pkg-group'])
        pm_group=os.path.join(dat_dir, pm_group_fname)
        if not os.path.isfile(pm_group):
            error_log_print("Package group not defined")
            return
        _iso_prep(dom, pm_group)

        logger.debug("Commision start")

        vc_commision.start(comi_dir, net_dir, arg_d)

        logger.info("Ejecting cdrom")
        _cdrom_eject(dom)

        logger.debug("Exiting Commision")

    def help_initialize(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        print("     Initialize domain <domain name>  ")

    def complete_initialize(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))
        return complete_dom(text, line, begidx, endidx)

    def do_package(self, args):
        logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        pkg_cli=provCLI_package(arg_d)
        pkg_cli.cmdloop()

        comi_dir=os.path.join(os.getcwd(), "commisioned_domain")
        vc_commision.pkg_config_add(comi_dir, arg_d)

    def help_package(self, args):
        pass
    def complete_package(self, args):
        pass

def prep_provision():
    global logger

    try:
        os.mkdir("logs")
    except OSError:
        pass

    # create logger
    logger = logging.getLogger('provision')
    logger.setLevel(logging.DEBUG)

    # create file handler and set level to debug
    fh = logging.handlers.RotatingFileHandler("logs/provision.log",
                                              maxBytes=50*1024*1024,
                                              backupCount=5)
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    fh.setFormatter(formatter)

    # add fh to logger
    logger.addHandler(fh)

    logger.info('Provisioning initiated')

def cleanup_provision():
    global logger
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

def main():

    prep_provision()

    try:
        os.mkdir("provisioned_domain")
        logger.info("provisioned_domain directory created")
        os.mkdir("commisioned_domain")
        logger.info("commisioned_domain directory created")
        os.mkdir("commisioned_domain/dat")
        logger.info("commisioned_domain/dat directory created")
        os.mkdir("net")
        logger.info("net directory created")
    except OSError:
        logger.info("Skipping directory creations")
        pass

    try:
        prov_cmd=provCLI()
        prov_cmd.cmdloop()
    except (common.execCmdError,
            provisionError,
            vc_commision.commisionError,
            ssh.sshError,
            IOError,
            OSError) as e:
        logger.exception("Error {0}".format(str(e)))
    except:
        logger.exception("Error")

    cleanup_provision()

if __name__=='__main__':
    main()
