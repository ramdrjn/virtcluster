
from common import common
from common import cli_fmwk
import json
import inspect
import subprocess

def debug(msg):
    print(msg)
    pass

def start_proc(mod):
    p_ref=None
    if mod == 'generator':
        p_ref=subprocess.Popen(["/opt/cpackgen.exe", "generator"],
                               stdin=subprocess.PIPE)
    elif mod == 'receiver':
        p_ref=subprocess.Popen(["/opt/cpackgen.exe", "receiver"],
                               stdin=subprocess.PIPE)
    return (p_ref)

def process_stats(fd):
    pass

def jdump(data, fd):
    debug("In Function {0}".format(inspect.stack()[0][3]))
    json.dump(data, fd)

class comCls(cli_fmwk.VCCli):
    def __init__(self, intro, prompt, ftype):
        debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro=intro)
        self.prompt=prompt
        self._ftype=ftype

    def postloop(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.terminate()
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            self.p_ref.kill()

    def preloop(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref=start_proc(self._ftype)

    def do_start(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('start', self.p_ref.stdin)

    def help_start(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Start {0}     ".format(self._ftype))

    def do_stop(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('stop', self.p_ref.stdin)
        return True

    def help_stop(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Stop {0}     ".format(self._ftype))

    def do_stats(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('stats', self.p_ref.stdin)
        process_stats(self.p_ref.stdout)

    def help_stats(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Display stats    ")

    def do_pause(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('pause', self.p_ref.stdin)

    def help_pause(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Pause {0}     ".format(self._ftype))

    def do_resume(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('resume', self.p_ref.stdin)

    def help_resume(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Resume {0}     ".format(self._ftype))
