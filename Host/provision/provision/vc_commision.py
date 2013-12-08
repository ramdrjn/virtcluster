
from common import common
from provision import ssh

import inspect
import os
import json
import urlparse

def _prep_commision(dat_dir, fname, sshi):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    status=sshi.createHostKeys()
    return (status)

def _check_commision_prep(dat_dir, sshi):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    prep_status=(0, "success")
    try:
        os.mkdir(dat_dir)
    except OSError:
        pass

    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        prep_status=_prep_commision(dat_dir, fname, sshi)

    if prep_status[0] != 0:
        return prep_status

    return ((0, "success"))

def _do_pm_config_file(pm_config, arg_d):
    with open(pm_config, "w") as f:
        f.write("[main]\n")
        f.write("   type = rpm-md\n")
        f.write("   baseurl = {0}\n".format(arg_d['pm-url']))
    return ((0, "success"))

def start(comi_dir, net_dir, arg_d):
    common.log(common.debug,
               "In Function {0}".format(inspect.stack()[0][3]))

    domain=arg_d['domain']
    domain_dir = os.path.join(comi_dir, domain)
    try:
        os.mkdir(domain_dir)
    except OSError:
        return ((-1, "Unable to create domain directory"))

    sshi=ssh.ssh_Cls(domain, domain_dir, net_dir)

    dat_dir = os.path.join(comi_dir, "dat")

    ck_status = _check_commision_prep(dat_dir, sshi)
    if ck_status[0] != 0:
        return ck_status

    lk_status=sshi.do_ssh_linkup()
    if lk_status[0] != 0:
        return lk_status

    status=sshi.do_ssh_config()
    if status[0] != 0:
        return status

    rmt_conf_dir='/opt/x86vm'
    cmd='mkdir -p {0}'.format(rmt_conf_dir)
    exec_status=sshi.exec_remote_cmd(cmd)
    if exec_status[0] != 0:
        return exec_status

    conf={}
    conf['pkg-mgmt']=arg_d['pkg-mgmt']

    url=urlparse.urlparse(arg_d['pm-url'])
    conf['pm-url-scheme']=url.scheme

    pm_config_fname="pm_config"
    pm_config = os.path.join(domain_dir, pm_config_fname)
    pm_status=_do_pm_config_file(pm_config, arg_d)
    if pm_status[0] != 0:
        return pm_status

    cp_status=sshi.remote_cp(pm_config, rmt_conf_dir)
    if cp_status[0] != 0:
        return cp_status

    conf['pm-config-file']=os.path.join(rmt_conf_dir, pm_config_fname)

    comm_fname="commision.conf"
    rem_comm_file = os.path.join(rmt_conf_dir, comm_fname)
    comm_conf = os.path.join(domain_dir, comm_fname)
    with open(comm_conf, 'w') as f:
        json.dump(conf, f)

    cp_status=sshi.remote_cp(comm_conf, rem_comm_file)
    if cp_status[0] != 0:
        return cp_status

    bootstrap_f = os.path.join(comi_dir, "../provision/bootstrap_com.sh")
    cp_status=sshi.remote_cp(bootstrap_f, rmt_conf_dir)
    if cp_status[0] != 0:
        return cp_status

    cmd="sh -x /opt/x86vm/bootstrap_com.sh {0}".format(rem_comm_file)
    exec_status=sshi.exec_remote_cmd(cmd)
    if exec_status[0] != 0:
        return exec_status

    return ((0, "success"))
