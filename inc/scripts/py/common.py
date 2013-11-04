
import subprocess
import inspect

debug=1
info=3
error=5

debug_lvl=info

screen=0
file=1
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
      return lvl

def exec_cmd(cmd, out=None, err=None):
      log(debug, "In Function {0}".format(inspect.stack()[0][3]))
      if out:
            err = subprocess.STDOUT
      try:
            log(debug, "Executing command {0}".format(cmd))
            subprocess.check_call(cmd, stdout=out, stderr=err)
      except subprocess.CalledProcessError as e:
            log(error, "Cmd: {0} returned {1}\n".format(e.cmd, e.returncode))

'''                           CLI Framework                       '''
