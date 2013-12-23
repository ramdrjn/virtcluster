#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('/opt/x86vm/')

from common import common
from common import cli_fmwk
import json
import cmd
import inspect
import subprocess

def _debug(msg):
    print(msg)
    pass

def start_proc(mod):
    p_ref=None
    if mod == 'generator':
        p_ref=subprocess.Popen(["./cpackgen.exe", "generator"],
                               stdin=subprocess.PIPE)
    elif mod == 'receiver':
        p_ref=subprocess.Popen(["./cpackgen.exe", "receiver"],
                               stdin=subprocess.PIPE)
    return (p_ref)

def _process_stats(fd):
    pass

class generator_cli(cli_fmwk.VCCli):
    def __init__(self):
        _debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Generator subcommands")
        self.prompt='cpackgen:Generator)'

    def postloop(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.terminate()
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.kill()

    def preloop(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref=start_proc('generator')

    def do_start(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('start', self.p_ref.stdin)

    def help_start(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Start Generator     ")

    def do_stop(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stop', self.p_ref.stdin)
        return True

    def help_stop(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Stop Generator     ")

    def do_stats(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stats', self.p_ref.stdin)
        _process_stats(self.p_ref.stdout)

    def help_stats(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Display stats    ")

    def do_pause(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('pause', self.p_ref.stdin)

    def help_pause(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Pause Generator     ")

    def do_resume(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('resume', self.p_ref.stdin)

    def help_resume(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Resume Generator     ")

class receiver_cli(cli_fmwk.VCCli):
    def __init__(self):
        _debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Receiver subcommands")
        self.prompt='cpackgen:Receiver)'

    def postloop(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.terminate()
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.kill()

    def preloop(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref=start_proc('receiver')

    def do_start(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('start', self.p_ref.stdin)

    def help_start(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Start Receiver     ")

    def do_stop(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stop', self.p_ref.stdin)
        return True

    def help_stop(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Stop Receiver     ")

    def do_stats(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stats', self.p_ref.stdin)
        _process_stats(self.p_ref.stdout)

    def help_stats(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Display stats    ")

    def do_pause(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('pause', self.p_ref.stdin)

    def help_pause(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Pause Receiver     ")

    def do_resume(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('resume', self.p_ref.stdin)

    def help_resume(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Resume Receiver     ")

class cpackgen_cli(cli_fmwk.VCCli):
    def __init__(self):
        _debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="cpackgen cli",
                                prompt="(cpackgen)")

    def do_generator(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        gen_cli=generator_cli()
        gen_cli.cmdloop()

    def help_generator(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Generator subcommands     ")

    def do_receiver(self, args):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        rcv_cli=generator_cli()
        rcv_cli.cmdloop()

    def help_receiver(self):
        _debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Receiver subcommands     ")

def start():
    _debug("In Function {0}".format(inspect.stack()[0][3]))

    cpg_cli=cpackgen_cli()
    cpg_cli.cmdloop()

def prep():
    _debug("In Function {0}".format(inspect.stack()[0][3]))

def cleanup():
    _debug("In Function {0}".format(inspect.stack()[0][3]))

def main():
    _debug("In Function {0}".format(inspect.stack()[0][3]))

    prep()

    start()

    cleanup()

if __name__=='__main__':
    main()
