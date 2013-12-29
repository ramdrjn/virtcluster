#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/opt/x86vm/')

from common import common
from common import cli_fmwk
from utils import gen
from utils import rcv
from utils import grc
import cmd
import inspect

class cpackgen_cli(cli_fmwk.VCCli):
    def __init__(self):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="cpackgen cli",
                                prompt="(cpackgen)")

    def do_generator(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        gen_cli=gen.generator_cli()
        gen_cli.cmdloop()

    def help_generator(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Generator subcommands     ")

    def do_receiver(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))

        rcv_cli=rcv.receiver_cli()
        rcv_cli.cmdloop()

    def help_receiver(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Receiver subcommands     ")

def start():
    grc.debug("In Function {0}".format(inspect.stack()[0][3]))

    cpg_cli=cpackgen_cli()
    cpg_cli.cmdloop()

def prep():
    grc.debug("In Function {0}".format(inspect.stack()[0][3]))

def cleanup():
    grc.debug("In Function {0}".format(inspect.stack()[0][3]))

def main():
    grc.debug("In Function {0}".format(inspect.stack()[0][3]))

    prep()

    start()

    cleanup()

if __name__=='__main__':
    main()
