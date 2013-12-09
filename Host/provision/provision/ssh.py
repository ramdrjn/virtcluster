
from common import common

import inspect
import json
import os
import time

class sshError(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

class ssh_Cls():
    def __init__(self, domain, domain_dir, net_dir, log):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        self.domain=domain
        self.domain_dir=domain_dir
        self.net_dir=net_dir
        self.ssh_dir=os.path.join(net_dir, "ssh")

        try:
            os.mkdir(self.ssh_dir)
        except OSError:
            pass

        self.known_host = os.path.join(self.ssh_dir, "known_hosts")
        self.id = os.path.join(self.ssh_dir, "host_key.pub")
        self.ip_host = self._get_ip_host_from_domain()
        self.ssh_config = os.path.join(self.domain_dir, "ssh_config")
        self.log_file=log
        common.log([common.info, common.lfile, self.log_file],
                   "\nStarting SSH at {0}".format(time.asctime()))

    def _get_ip_host_from_domain(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        dom_net=os.path.join(self.net_dir, "{0}.net".format(self.domain))
        with open(dom_net, 'r') as f:
            j_dict=json.load(f)
        return ((j_dict['fab0_dom_ip'], 'ip'))

    def createHostKeys(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        key_fname = os.path.join(self.ssh_dir, "host_key")
        common.log([common.info, common.lfile, self.log_file],
                   "\nGenerating ssh keys {0}".format(key_fname))
        op=common.exec_cmd_op(["ssh-keygen", "-P", "", "-f", key_fname])
        common.log([common.info, common.lfile, self.log_file], op)

    def do_ssh_linkup(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        op=common.exec_cmd_op(["ssh",
                         "-o","UserKnownHostsFile={0}".format(self.known_host),
                         "-o", "StrictHostKeyChecking=no",
                         "-i", self.id,
                         self.ip_host[0],
                         "hostname"])
        common.log([common.info, common.lfile, self.log_file], op)

    def do_ssh_config(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        with open(self.ssh_config, "w") as f:
            f.write("Host {0}\n".format(self.ip_host[0]))
            f.write("  User root\n")
            f.write("  IdentityFile {0}\n".format(self.id))
            f.write("  UserKnownHostsFile {0}\n".format(self.known_host))

    def exec_remote_cmd(self, cmd):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        op=common.exec_cmd_op(["ssh",
                               "-F", self.ssh_config,
                               self.ip_host[0],
                               cmd])
        common.log([common.info, common.lfile, self.log_file], op)

    def remote_cp(self, src, dst):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        op=common.exec_cmd_op(["scp",
                               "-F", self.ssh_config,
                               src,
                               self.ip_host[0]+":"+dst])
        common.log([common.info, common.lfile, self.log_file], op)

    def remove_domain_from_known_host(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        op=common.exec_cmd_op(["ssh-keygen",
                               "-R", self.ip_host[0],
                               "-f", self.known_host])
        common.log([common.info, common.lfile, self.log_file], op)
