
from common import common
from provision import ssh

import inspect
import os
import json
import urlparse
import time

log_file=None

class commisionError(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

def _prep_commision(dat_dir, fname, sshi):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    with open(fname, 'w') as f:
        f.write("Done at {0}".format(time.asctime()))

    sshi.createHostKeys()

def _check_commision_prep(dat_dir, sshi):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    os.mkdir(dat_dir)
    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        common.log([common.info, common.lfile, log_file],
                   "\nCommision prep at {0}".format(time.asctime()))
        _prep_commision(dat_dir, fname, sshi)

def _do_pm_config_file(pm_config, arg_d):
    with open(pm_config, "w") as f:
        f.write("[main]\n")
        f.write("   type = rpm-md\n")
        f.write("   baseurl = {0}\n".format(arg_d['pm-url']))

def start(comi_dir, net_dir, arg_d):
    global log_file

    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    log_file=open(os.path.join("logs", "commision.log"), 'a+')

    common.log([common.info, common.lfile, log_file],
               "\nCommision initiated on {0}".format(time.asctime()))

    domain=arg_d['domain']
    domain_dir = os.path.join(comi_dir, domain)

    os.mkdir(domain_dir)
    common.log([common.info, common.lfile, log_file],
               "\nCommision directory {0}".format(domain_dir))

    sshi=ssh.ssh_Cls(domain, domain_dir, net_dir, log_file)

    dat_dir = os.path.join(comi_dir, "dat")
    common.log([common.info, common.lfile, log_file],
               "\nCommision dat directory {0}".format(dat_dir))

    _check_commision_prep(dat_dir, sshi)

    common.log([common.info, common.lfile, log_file],
               "\nAttempting SSH linkup")
    sshi.do_ssh_linkup()

    common.log([common.info, common.lfile, log_file],
               "\nBuilding SSH config")
    sshi.do_ssh_config()

    rmt_conf_dir='/opt/x86vm'
    common.log([common.info, common.lfile, log_file],
               "\nBuilding remote directory {0}".format(rmt_conf_dir))
    cmd='mkdir -p {0}'.format(rmt_conf_dir)
    sshi.exec_remote_cmd(cmd)

    conf={}
    conf['pkg-mgmt']=arg_d['pkg-mgmt']

    url=urlparse.urlparse(arg_d['pm-url'])
    conf['pm-url-scheme']=url.scheme

    common.log([common.info, common.lfile, log_file],
               "\nPM {0} url {1} {0}".format(arg_d['pkg-mgmt'], arg_d['pm-url']))

    pm_config_fname="pm_config"
    pm_config = os.path.join(domain_dir, pm_config_fname)
    common.log([common.info, common.lfile, log_file],
               "\nLocal PM config file {0}".format(pm_config))

    _do_pm_config_file(pm_config, arg_d)

    common.log([common.info, common.lfile, log_file],
               "\nMoving PM config file to remote")
    sshi.remote_cp(pm_config, rmt_conf_dir)

    conf['pm-config-file']=os.path.join(rmt_conf_dir, pm_config_fname)

    comm_fname="commision.conf"
    rem_comm_file = os.path.join(rmt_conf_dir, comm_fname)
    comm_conf = os.path.join(domain_dir, comm_fname)
    common.log([common.info, common.lfile, log_file],
               "\nLocal commision config file {0}".format(comm_conf))
    with open(comm_conf, 'w') as f:
        json.dump(conf, f)

    common.log([common.info, common.lfile, log_file],
               "\nMoving commision config file to remote")
    sshi.remote_cp(comm_conf, rem_comm_file)

    bootstrap_f = os.path.join(comi_dir, "../provision/bootstrap_com.sh")
    common.log([common.info, common.lfile, log_file],
               "\nMoving local bootstrap {0} to remote".format(bootstrap_f))
    sshi.remote_cp(bootstrap_f, rmt_conf_dir)

    cmd="sh /opt/x86vm/bootstrap_com.sh {0}".format(rem_comm_file)
    common.log([common.info, common.lfile, log_file],
               "\nExecuting command {0} in target".format(cmd))
    sshi.exec_remote_cmd(cmd)
    common.log([common.info, common.lfile, log_file],
               "\nCommision initiated for domain")
    log_file.close()

def cleanup(domain, comi_dir, net_dir):
    global log_file

    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    log_file=open(os.path.join("logs", "commision.log"), 'a+')

    domain_dir = os.path.join(comi_dir, domain)
    sshi=ssh.ssh_Cls(domain, domain_dir, net_dir, log_file)
    common.log([common.info, common.lfile, log_file],
               "\nRemoving domain entry from known host")
    sshi.remove_domain_from_known_host()
    log_file.close()
