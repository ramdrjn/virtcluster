
from common import common

import inspect
import json
import os
import logging

class sshError(Exception):
    def __init__(self, value):
        self.value=value
    def __str__(self):
        return repr(self.value)

class ssh_Cls():
    def __init__(self, domain, domain_dir, net_dir, log):
        self.logger=log
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.domain=domain
        self.domain_dir=domain_dir
        self.net_dir=net_dir
        self.ssh_dir=os.path.join(net_dir, "ssh")

        try:
            os.mkdir(self.ssh_dir)
            self.logger.debug("Mkdir SSH directory")
        except OSError:
            self.logger.debug("Skipping SSH directory creation")

        self.known_host = os.path.join(self.ssh_dir, "known_hosts")
        self.id = os.path.join(self.ssh_dir, "host_key.pub")
        self.ip_host = self._get_ip_host_from_domain()
        self.ssh_config = os.path.join(self.domain_dir, "ssh_config")
        self.logger.debug("Starting SSH")

    def _get_ip_host_from_domain(self):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        dom_net=os.path.join(self.net_dir, "{0}.net".format(self.domain))
        self.logger.info("Checking domain network file {0}".format(dom_net))
        with open(dom_net, 'r') as f:
            j_dict=json.load(f)
        self.logger.debug("Domain IP {0}".format(j_dict['fab0_dom_ip']))
        return ((j_dict['fab0_dom_ip'], 'ip'))

    def createHostKeys(self):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        key_fname = os.path.join(self.ssh_dir, "host_key")
        self.logger.info("Generating ssh keys {0}".format(key_fname))
        op=common.exec_cmd_op(["ssh-keygen", "-P", "", "-f", key_fname])
        self.logger.info(op)

    def do_ssh_linkup(self):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.logger.debug("Attempting ssh linkup")
        op=common.exec_cmd_op(["ssh",
                         "-o","UserKnownHostsFile={0}".format(self.known_host),
                         "-o", "StrictHostKeyChecking=no",
                         "-i", self.id,
                         self.ip_host[0],
                         "hostname"])
        self.logger.info(op)

    def do_ssh_config(self):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.logger.debug("Writing ssh config {0}".format(self.ssh_config))
        with open(self.ssh_config, "w") as f:
            f.write("Host {0}\n".format(self.ip_host[0]))
            f.write("  User root\n")
            f.write("  IdentityFile {0}\n".format(self.id))
            f.write("  UserKnownHostsFile {0}\n".format(self.known_host))

    def exec_remote_cmd(self, cmd):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.logger.debug("Executing ssh command")
        op=common.exec_cmd_op(["ssh",
                               "-F", self.ssh_config,
                               self.ip_host[0],
                               cmd])
        self.logger.info( op)

    def remote_cp(self, src, dst):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.logger.debug("Executing remote copy")
        op=common.exec_cmd_op(["scp",
                               "-F", self.ssh_config,
                               src,
                               self.ip_host[0]+":"+dst])
        self.logger.info( op)

    def remove_domain_from_known_host(self):
        self.logger.debug("In Function {0}".format(inspect.stack()[0][3]))

        self.logger.debug("Removing domain from known hosts")
        op=common.exec_cmd_op(["ssh-keygen",
                               "-R", self.ip_host[0],
                               "-f", self.known_host])
        self.logger.info( op)
