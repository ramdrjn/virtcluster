
from common import common
from provision import ssh

import inspect
import os
import json
import urlparse
import time
import logging
import shutil

logger=None

class commisionError(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

def _prep_commision(dat_dir, fname, sshi):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    logger.info("Updating {0} file".format(fname))
    with open(fname, 'w') as f:
        f.write("Done at {0}".format(time.asctime()))

    sshi.createHostKeys()

def _check_commision_prep(dat_dir, sshi):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    fname = os.path.join(dat_dir, "commision.dat")

    if not os.path.isfile(fname):
        logger.info("Commision prep")
        _prep_commision(dat_dir, fname, sshi)

def _do_pm_config_file(local_pm_config, local_pm_grp):
    logger.debug("In Function {0}".format(inspect.stack()[0][3]))
    arg_d={}
    with open(local_pm_grp, "r") as f:
        arg_d = json.load(f)
    with open(local_pm_config, "w") as f:
        if 'main' in arg_d:
            main_d=arg_d['main']
            f.write("[main]\n")
            f.write("   type = rpm-md\n")
            f.write("   baseurl = {0}\n".format(main_d['url']))
        if 'update' in arg_d:
            update_d=arg_d['update']
            f.write("[update]\n")
            f.write("   type = rpm-md\n")
            f.write("   baseurl = {0}\n".format(update_d['url']))

def start(comi_dir, net_dir, arg_d):
    global logger
    logger = logging.getLogger('provision.commision')

    logger.debug("In Function {0}".format(inspect.stack()[0][3]))
    logger.debug("Commision start args {0}", arg_d)

    logger.info("Commision initiated")

    domain=arg_d['domain']
    domain_dir = os.path.join(comi_dir, domain)

    logger.info("Commision domain directory {0}".format(domain_dir))
    os.mkdir(domain_dir)

    sshi=ssh.ssh_Cls(domain, domain_dir, net_dir,
                     logging.getLogger('provision.commision.ssh'))

    dat_dir = os.path.join(comi_dir, "dat")
    logger.info("Commision dat directory {0}".format(dat_dir))

    _check_commision_prep(dat_dir, sshi)

    logger.info("Attempting SSH linkup")
    sshi.do_ssh_linkup()

    logger.info("Building SSH config")
    sshi.do_ssh_config()

    rmt_dir='/opt/x86vm'
    rmt_conf_dir=os.path.join(rmt_dir, 'conf')
    logger.info("Building remote directory {0}".format(rmt_conf_dir))
    cmd='mkdir -p {0}'.format(rmt_conf_dir)
    sshi.exec_remote_cmd(cmd)

    logger.info("PM group {0}".format(arg_d['pkg-group']))

    pm_grp_fname="pm.grp"
    local_pm_grp=os.path.join(domain_dir, pm_grp_fname)
    logger.info("Local PM group file {0}".format(local_pm_grp))
    shutil.copy(os.path.join(dat_dir, "{0}.pg".format(arg_d['pkg-group'])),
                local_pm_grp)

    pm_config_fname="pm.cfg"
    local_pm_config = os.path.join(domain_dir, pm_config_fname)
    logger.info("Local PM config file {0}".format(local_pm_config))

    _do_pm_config_file(local_pm_config, local_pm_grp)

    logger.info("Moving PM group file to remote")
    sshi.remote_cp(local_pm_grp, rmt_conf_dir)

    logger.info("Moving PM config file to remote")
    sshi.remote_cp(local_pm_config, rmt_conf_dir)

    conf={}
    conf['pm-group-file']=os.path.join(rmt_conf_dir, pm_grp_fname)
    conf['pm-config-file']=os.path.join(rmt_conf_dir, pm_config_fname)

    comm_fname="commision.conf"
    rem_comm_file = os.path.join(rmt_conf_dir, comm_fname)
    comm_conf = os.path.join(domain_dir, comm_fname)
    logger.info("Writing to local commision config file {0}".format(comm_conf))
    with open(comm_conf, 'w') as f:
        json.dump(conf, f)

    logger.info("Moving commision config file to remote")
    sshi.remote_cp(comm_conf, rem_comm_file)

    bootstrap_f = os.path.join(comi_dir, "../provision/bootstrap_com.sh")
    logger.info("Moving local stage 1 {0} to remote".format(bootstrap_f))
    sshi.remote_cp(bootstrap_f, rmt_dir)

    cmd="sh /opt/x86vm/bootstrap_com.sh {0}".format(rem_comm_file)
    logger.info("Executing command {0} in target".format(cmd))
    logger.info("Commision stage 1 initiated for domain")
    sshi.exec_remote_cmd(cmd)
    logger.info("Domain commision cli end")

def cleanup(domain, comi_dir, net_dir):
    global logger
    logger = logging.getLogger('provision.commision')

    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    domain_dir = os.path.join(comi_dir, domain)
    sshi=ssh.ssh_Cls(domain, domain_dir, net_dir,
                     logging.getLogger('provision.commision.ssh'))
    logger.info("Removing domain entry from known host")
    sshi.remove_domain_from_known_host()

def pkg_config_add(comi_dir, p_dict):
    global logger
    logger = logging.getLogger('provision.commision')

    logger.debug("In Function {0}".format(inspect.stack()[0][3]))

    dat_dir=os.path.join(comi_dir, "dat")
    grp_fname=os.path.join(dat_dir, "{0}.pg".format(p_dict['group']))
    logger.info("Updating package management group file {0}".format(grp_fname))
    with open(grp_fname, 'w') as f:
        json.dump(p_dict, f)
    logger.info("Done configuring package management group")
