try:
      import subprocess
except ImportError:
      import commands

import inspect

debug=1
info=3
error=5

debug_lvl=info

screen=0
lfile=1
screen_file=2

def set_debug_lvl(lvl):
      global debug_lvl
      debug_lvl = lvl

def log(ctrl, arg):
      if not isinstance(ctrl, list):
            ctrl_lst=[]
            ctrl_lst.append(ctrl)
            ctrl_lst.append(screen)
            ctrl_lst.append(None)
      else:
            ctrl_lst=ctrl
      lvl=ctrl_lst[0]
      if lvl >= debug_lvl and ctrl_lst[1] != 1:
            print(arg)
      if ctrl_lst[1] and ctrl_lst[2]:
            ctrl_lst[2].write(arg)
      return (lvl)

class execCmdError(Exception):
      def __init__(self, value):
            self.value=value
      def __str__(self):
            return repr(self.value)

def exec_cmd(cmd, out=None, err=None):
      log(debug, "In Function {0}".format(inspect.stack()[0][3]))
      log(debug, "Executing command {0}".format(cmd))
      try:
            if not err:
                  err = subprocess.STDOUT
            subprocess.check_call(cmd, stdout=out, stderr=err)
      except subprocess.CalledProcessError as e:
            raise execCmdError("Cmd: {0} returned {1} \n".format(
                  e.cmd, e.returncode))

def exec_cmd_op(cmd):
      log(debug, "In Function {0}".format(inspect.stack()[0][3]))
      log(debug, "Executing command {0}".format(cmd))
      try:
            out=subprocess.check_output(cmd)
      except subprocess.CalledProcessError as e:
            errstr="Cmd: {0} returned {1}\n".format(e.cmd, e.returncode)
            if e.output != None:
                  errstr=errstr+"Output {0}\n".format(e.output)
            raise execCmdError(errstr)
      return (out)

def exec_command(cmd):
      log(debug, "In Function {0}".format(inspect.stack()[0][3]))

      try:
            log(debug, "Executing command {0}".format(cmd))
            (status, op)=commands.getstatusoutput(cmd)
      except:
            raise execCmdError("Cmd failed returned {0} output {1}".format(
                        status, op))
      return (op)
