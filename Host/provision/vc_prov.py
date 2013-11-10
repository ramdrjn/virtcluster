#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import common
from common import cli_fmwk
from provision import py_libvirt
import inspect
import string
import os
import json
import shutil

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

    def _complete_nwk_dom(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

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

    def _complete_dom(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, ['domain'], text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='domain':
                print("<domain name>")
                comp_type=['']
        return comp_type

    def _complete_network(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, ['network'], text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='network':
                print("<network name>")
                comp_type=['']
        return comp_type

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

        comp_type=cli_fmwk.VCCli._autocomp(self, ['domain'], arg_lst[0])

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
        return self._complete_dom(text, line, begidx, endidx)

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

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

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
        return self._complete_nwk_dom(text, line, begidx, endidx)

class provCLI_domain(cli_fmwk.VCCli):
    def __init__(self, con):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="Domain subcommands")
        self.prompt = self.prompt[:-1]+':Domain)'
        self.def_comp_lst=['domain']
        self._con = con

    def _complete_dom(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='domain':
                print("<domain name>")
                comp_type=['']
        return comp_type

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
                  <mac address='$fab0_nic_mac'/>\
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
        except Exception as E:
            print("Invalid arguments")
        return xmlT

    def do_define(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        arg_d = dict(zip(arg_lst[::2], [arg_lst[i]
                                        for i in range(1, len(arg_lst), 2)]))

        dom_name=arg_d['domain']
        if dom_name:
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if dom:
                print("Domain already defined")
                return
        else:
            print("Enter domain ")
            return

        img_name=arg_d['image']
        if img_name:
            img_dir="provisioned_domain/{}/images".format(dom_name)
            os.makedirs(img_dir)
            img_tgz=os.path.join("./images",
                                 "virtcluster-image-{}.tgz".format(img_name))
            common.exec_cmd(["tar", "zxvf", img_tgz, "-C", img_dir])
        else:
            print("Enter Image")
            return

        img_dir=os.path.join(os.getcwd(),
                  "provisioned_domain/{}/images/{}".format(dom_name, img_name))

        with open(os.path.join(img_dir,"manifest")) as infile:
            img_desc = json.load(infile)

        arg_d['kernel']=os.path.join(img_dir, img_desc['kernel'])
        arg_d['rootfs']=os.path.join(img_dir, img_desc['fs_raw'])

        xml = self._dom_xml_comp(arg_d)
        dom = py_libvirt.dom_defineXML(self._con, xml)

    def help_define(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Define domain <domain name>    ")

    def complete_define(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

    def do_undefine(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            dom = py_libvirt.dom_undefine(dom)
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
        return self._complete_nwk_dom(text, line, begidx, endidx)

    def do_purge(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_purge()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                shutil.rmtree(os.path.join("provisioned_domain", dom_name),
                              True)
            else:
                print("Domain still defined")
                return
        else:
            print("Enter network")
            return

    def help_purge(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Purge domain <domain name>    ")

    def complete_purge(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

    def do_start(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
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
        return self._complete_nwk_dom(text, line, begidx, endidx)

    def do_stop(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
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
        return self._complete_nwk_dom(text, line, begidx, endidx)

    def do_shut(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_shut()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
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
        return self._complete_dom(text, line, begidx, endidx)

    def do_pause(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_pause()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
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
        return self._complete_dom(text, line, begidx, endidx)

    def do_resume(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_resume()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
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
        return self._complete_dom(text, line, begidx, endidx)

class provCLI_network(cli_fmwk.VCCli):
    def __init__(self, con):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="Network subcommands")
        self.prompt = self.prompt[:-1]+':Network)'
        self.def_comp_lst=['network']
        self._con = con

    def _complete_network(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='network':
                print("<network name>")
                comp_type=['']
        return comp_type

    def _nwk_xml_comp(self, val):
        xml="\
           <network>\
             <name>$network</name>\
             <bridge name='$brname' stp='on' delay='0' />\
             <mac address='52:54:00:3E:31:C9'/>\
             <ip address='192.168.100.1' netmask='255.255.255.0'>\
               <dhcp>\
                 <range start='192.168.100.128' end='192.168.100.254' />\
               </dhcp>\
             </ip>\
           </network>\
"
        xmlT=""
        try:
            xmlT=string.Template(xml).substitute(val)
        except Exception as E:
            print("Invalid arguments")
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
        xml = self._nwk_xml_comp(arg_d)
        nwk = py_libvirt.network_defineXML(self._con, xml)

    def help_define(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Define network <network name>  ")

    def complete_define(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        return self._complete_network(text, line, begidx, endidx)

    def do_undefine(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
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
        return self._complete_network(text, line, begidx, endidx)

    def do_start(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
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
        return self._complete_network(text, line, begidx, endidx)

    def do_stop(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
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
        return self._complete_network(text, line, begidx, endidx)

if __name__=='__main__':
#    common.set_debug_lvl(common.debug)

    try:
        os.mkdir("provisioned_domain")
    except OSError:
        pass

    prov_cmd=provCLI()
    prov_cmd.cmdloop()
