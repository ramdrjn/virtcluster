
from common import common
from common import cli_fmwk
from utils import grc
from utils import pkt
import cmd
import inspect

class genPkt_cli(cli_fmwk.VCCli):
    def __init__(self, d):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Generator packet definitions cli",
                                prompt="(cpackgen:Generator:Packet)")
        self.param_dict=d

    def do_l2(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=pkt.l2_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l2']=l_dict

    def help_l2(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 2 packet definition subcommands         ")

    def do_l3(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=pkt.l3_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l3']=l_dict

    def help_l3(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 3 packet definition subcommands         ")

    def do_l4(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=pkt.l4_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l4']=l_dict

    def help_l4(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 4 packet definition subcommands         ")

    def do_l7(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=pkt.l7_cli(l_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['l7']=l_dict

    def help_l7(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Layer 7 packet definition subcommands         ")

    def do_custom(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        l_dict={}

        p_cli=pkt.customPkt_cli(l_dict)
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

        if len(r_list) < 2:
            self.help_rate()
            return

        if r_list[0]=='pps':
            if not r_list[1]:
                self.help_rate()
                return
            self.param_dict['rate_pps']=int(r_list[1])
        elif r_list[0]=='bps':
            if not r_list[1]:
                self.help_rate()
                return
            bps=int(r_list[1])
            if r_list[2]:
                if r_list[2]=='KBps':
                    bps=bps*1024*8
                if r_list[2]=='MBps':
                    bps=bps*1024*1024*8
                if r_list[2]=='GBps':
                    bps=bps*1024*1024*1024*8
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

        if len(r_list) < 2:
            self.help_count()
            return

        if r_list[0]=='max':
            if not r_list[1]:
                self.help_count()
                return
            self.param_dict['max_count']=int(r_list[1])
        else:
            self.help_count()
            return

    def help_count(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Packet count     ")
        print ("          count max <val> ")

    def do_duration(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        r_list=args.split()

        if len(r_list) < 2:
            self.help_duration()
            return

        if r_list[0]=='max':
            if not r_list[1]:
                self.help_duration()
                return
            self.param_dict['duration_max']=int(r_list[1])
        else:
            self.help_duration()
            return

    def help_duration(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Packet generation duration     ")
        print ("          duration <val>            ")

class generator_cli(grc.comCls):
    def __init__(self):
        grc.debug("Initialized {0} class".format(self.__class__))
        grc.comCls.__init__(self, "Generator subcommands",
                            'cpackgen:Generator)', 'generator')

    def __del__(self):
        grc.debug("Finalized {0} class".format(self.__class__))
        grc.comCls.__del__(self)

    def do_parameter(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        param_dict={}

        p_cli=genParams_cli(param_dict)
        p_cli.cmdloop()

        j_dict={}
        j_dict['generator_parameter']=param_dict
        #Send the parameters to generator process
        grc.jdump(j_dict, self.p_ref.stdin)
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            grc.error("Generator process terminated")
        else:
            grc.debug("Generator process still active")

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
        grc.jdump(j_dict, self.p_ref.stdin)
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            grc.error("Generator process terminated")
        else:
            grc.debug("Generator process still active")

    def help_packet(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Generator Packet definitions     ")
