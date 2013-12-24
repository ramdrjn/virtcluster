
import sys
sys.path.append('/opt/x86vm/')

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
        p_ref=subprocess.Popen(["./cpackgen.exe", "generator"],
                               stdin=subprocess.PIPE)
    elif mod == 'receiver':
        p_ref=subprocess.Popen(["./cpackgen.exe", "receiver"],
                               stdin=subprocess.PIPE)
    return (p_ref)

def process_stats(fd):
    pass
