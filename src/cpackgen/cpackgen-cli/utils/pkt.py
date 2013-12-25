
from common import common
from common import cli_fmwk
import grc
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
