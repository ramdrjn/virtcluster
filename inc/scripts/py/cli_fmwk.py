
import common
import cmd


def exec_cmd(cmd, out=None, err=None):
      log(debug, "In Function {0}".format(inspect.stack()[0][3]))
      if out:
            err = subprocess.STDOUT
      try:
            log(debug, "Executing command {0}".format(cmd))
            subprocess.check_call(cmd, stdout=out, stderr=err)
      except subprocess.CalledProcessError as e:
            log(error, "Cmd: {0} returned {1}\n".format(e.cmd, e.returncode))
