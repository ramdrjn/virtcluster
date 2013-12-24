#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/opt/x86vm/')

from common import common
from common import cli_fmwk
import gen-rcv-com as grc
import json
import cmd
import inspect

class l2_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 2 packet definitions",
                                prompt="(cpackgen:L2)")
        self.param_dict=d

class l3_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 3 packet definitions",
                                prompt="(cpackgen:L3)")
        self.param_dict=d

class l4_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 4 packet definitions",
                                prompt="(cpackgen:L4)")
        self.param_dict=d

class l7_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Layer 7 packet definitions",
                                prompt="(cpackgen:L7)")
        self.param_dict=d

class customPkt_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Custom packet definitions",
                                prompt="(cpackgen:Custom Packet)")
        self.param_dict=d

class genPkt_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Generator packet definitions cli",
                                prompt="(cpackgen:Generator:Packet)")
        self.param_dict=d

    def do_l2(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=l2_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l2']=l_dict

    def help_l2(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 2 packet definition subcommands         ")

    def do_l3(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=l3_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l3']=l_dict

    def help_l3(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 3 packet definition subcommands         ")

    def do_l4(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=l4_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l4']=l_dict

    def help_l4(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 4 packet definition subcommands         ")

    def do_l7(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=l7_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l7']=l_dict

    def help_l7(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 7 packet definition subcommands         ")

    def do_custom(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=customPkt_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['custom']=l_dict

    def help_custom(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Custom packet definition subcommands         ")

class genParams_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Generator parameters cli",
                                prompt="(cpackgen:Generator:Parameter)")
        self.param_dict=d

    def do_rate(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        r_list=args.split()
        if r_list[1]=='pps':
            if not r_list[2]:
                self.help_rate()
                return
            self.param_dict['rate_pps']=r_list[2]
        elif r_list[1]=='bps':
            if not r_list[2]:
                self.help_rate()
                return
            bps=r_list[2]
            if r_list[3]:
                if r_list[3]=='KBPS':
                    bps=bps*1024
                if r_list[3]=='MBPS':
                    bps=bps*1024*1024
                if r_list[3]=='GBPS':
                    bps=bps*1024*1024*1024
            self.param_dict['rate_bps']=bps
        else:
            self.help_rate()
            return

    def help_rate(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Generator rate parameter subcommands         ")
        print ("          Rate pps (packet per second) <val>      ")
        print ("          Rate bps (bits per second) <val>        ")
        print ("               Rate bps in bps, KBps, MBps, GBps  ")

    def do_count(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        r_list=args.split()
        if r_list[1]=='count':
            if not r_list[2]:
                self.help_count()
                return
            self.param_dict['count']=r_list[2]
        else:
            self.help_count()
            return

    def help_count(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Packet count     ")
        print ("          count <val> ")

    def do_duration(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        r_list=args.split()
        if r_list[1]=='duration':
            if not r_list[2]:
                self.help_duration()
                return
            self.param_dict['duration']=r_list[2]
        else:
            self.help_duration()
            return

    def help_duration(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Packet generation duration     ")
        print ("          duration <val>            ")

class generator_cli(cli_fmwk.VCCli):
    def __init__(self):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Generator subcommands")
        self.prompt='cpackgen:Generator)'

    def postloop(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.terminate()
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.kill()

    def preloop(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref=grc.start_proc('generator')

    def do_start(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('start', self.p_ref.stdin)

    def help_start(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Start Generator     ")

    def do_stop(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stop', self.p_ref.stdin)
        return True

    def help_stop(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Stop Generator     ")

    def do_stats(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stats', self.p_ref.stdin)
        grc.process_stats(self.p_ref.stdout)

    def help_stats(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Display stats    ")

    def do_pause(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('pause', self.p_ref.stdin)

    def help_pause(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Pause Generator     ")

    def do_resume(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('resume', self.p_ref.stdin)

    def help_resume(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Resume Generator     ")

    def do_parameter(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        param_dict={}

        p_cli=genParams_cli(param_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['generator_parameter']=param_dict
        #Send the parameters to generator process
        json.dump(j_dict, self.p_ref.stdin)

    def help_parameter(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Generator Parameters     ")

    def do_packet(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        pkt_dict={}

        p_cli=genPkt_cli(pkt_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['generator_packet']=pkt_dict
        #Send the packet definitions to generator process
        json.dump(j_dict, self.p_ref.stdin)

    def help_packet(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Generator Packet definitions     ")
