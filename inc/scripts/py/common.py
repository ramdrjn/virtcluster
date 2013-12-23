import subprocess

import inspect

class execCmdError(Exception):
      def __init__(self, value):
            self.value=value
      def __str__(self):
            return repr(self.value)

def exec_cmd(cmd, out=None, err=None):

      try:
            if not err:
                  err = subprocess.STDOUT
            subprocess.check_call(cmd, stdout=out, stderr=err)
      except subprocess.CalledProcessError as e:
            raise execCmdError("Cmd: {0} returned {1} \n".format(
                  e.cmd, e.returncode))

def exec_cmd_op(cmd):

      try:
            out=subprocess.check_output(cmd)
      except subprocess.CalledProcessError as e:
            errstr="Cmd: {0} returned {1}\n".format(e.cmd, e.returncode)
            if e.output != None:
                  errstr=errstr+"Output {0}\n".format(e.output)
            raise execCmdError(errstr)
      return (out)
