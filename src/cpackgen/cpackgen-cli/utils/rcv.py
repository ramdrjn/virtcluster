
from common import common
from common import cli_fmwk
import grc
import json
import inspect

class receiver_cli(grc.comCls):
    def __init__(self):
        grc.debug("Initialized {0} class".format(self.__class__))
        grc.comCls.__init__(self, "Receiver subcommands",
                            'cpackgen:Receiver)', 'receiver')

    def __del__(self):
        grc.debug("Finalized {0} class".format(self.__class__))
        grc.comCls.__del__(self)

    def do_filter(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        grc.jdump('filter', self.p_ref.stdin)

    def help_filter(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Receiver Filters     ")

    def do_save(self, args):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        grc.jdump('save', self.p_ref.stdin)

    def help_save(self):
        grc.debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("      Save captured packets     ")
