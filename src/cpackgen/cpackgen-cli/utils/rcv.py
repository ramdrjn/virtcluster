
import sys
sys.path.append('/opt/x86vm/')

from common import common
from common import cli_fmwk
import grc
import json
import cmd
import inspect

class receiver_cli(cli_fmwk.VCCli):
    def __init__(self):
        grc.debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro="Receiver subcommands")
        self.prompt='cpackgen:Receiver)'

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

        self.p_ref=grc.start_proc('receiver')

    def do_start(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('start', self.p_ref.stdin)

    def help_start(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Start Receiver     ")

    def do_stop(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('stop', self.p_ref.stdin)
        return True

    def help_stop(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Stop Receiver     ")

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
        print ("     Pause Receiver     ")

    def do_resume(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('resume', self.p_ref.stdin)

    def help_resume(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Resume Receiver     ")

    def do_filter(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('filter', self.p_ref.stdin)

    def help_filter(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Receiver Filters     ")

    def do_save(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        json.dump('save', self.p_ref.stdin)

    def help_save(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("      Save captured packets     ")
