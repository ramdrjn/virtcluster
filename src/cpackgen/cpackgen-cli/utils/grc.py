
from common import common
from common import cli_fmwk
import json
import inspect
import subprocess

def debug(msg):
    print(msg)
    pass

def start_proc(mod):
    debug("In Function {0}".format(inspect.stack()[0][3]))

    p_ref=None
    if mod == 'generator':
        p_ref=subprocess.Popen(["/opt/cpackgen.exe", "generator"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, close_fds=True)
    elif mod == 'receiver':
        p_ref=subprocess.Popen(["./cpackgen.exe", "receiver"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, close_fds=True)
    return (p_ref)

def process_stats(fd):
    pass

def jdump(data, fd):
    debug("In Function {0}".format(inspect.stack()[0][3]))
    s=json.dumps(data)
    cnt=fd.write(bytes(s))
    debug("Written {0}".format(cnt))

class comCls(cli_fmwk.VCCli):
    def __init__(self, intro, prompt, ftype):
        debug("Initialized {0} class".format(self.__class__))
        cli_fmwk.VCCli.__init__(self, intro=intro)
        self.prompt=prompt
        self.ftype=ftype

    def __del__(self):
        debug("Finalized {0} class".format(self.__class__))

    def postloop(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))

    def preloop(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))

        self.p_ref=start_proc(self.ftype)

    def do_start(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('start', self.p_ref.stdin)
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            error("Generator process terminated")
        else:
            debug("Generator process still active")

    def help_start(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Start    ")

    def do_stop(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('stop', self.p_ref.stdin)
        return True

    def help_stop(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Stop     ")

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
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            error("Generator process terminated")
        else:
            debug("Generator process still active")

    def help_pause(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Pause     ")

    def do_resume(self, args):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        jdump('resume', self.p_ref.stdin)
        self.p_ref.poll()
        if self.p_ref.returncode != None:
            error("Generator process terminated")
        else:
            debug("Generator process still active")

    def help_resume(self):
        debug("In Function {0}".format(inspect.stack()[0][3]))
        print ("     Resume     ")
