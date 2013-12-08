
from common import common

import inspect
import json
import os

class ssh_Cls():
    def __init__(self, domain, domain_dir, net_dir):
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
        common.exec_cmd(["ssh-keygen", "-P", "", "-f", key_fname])
        return ((0, "success"))

    def do_ssh_linkup(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        common.exec_cmd(["ssh",
                         "-o","UserKnownHostsFile={0}".format(self.known_host),
                         "-o", "StrictHostKeyChecking=no",
                         "-i", self.id,
                         self.ip_host[0],
                         "hostname"])
        return ((0, "success"))

    def do_ssh_config(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        with open(self.ssh_config, "w") as f:
            f.write("Host {0}\n".format(self.ip_host[0]))
            f.write("  User root\n")
            f.write("  IdentityFile {0}\n".format(self.id))
            f.write("  UserKnownHostsFile {0}\n".format(self.known_host))
        return ((0, "success"))

    def exec_remote_cmd(self, cmd):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        common.exec_cmd(["ssh",
                         "-F", self.ssh_config,
                         self.ip_host[0],
                         cmd])
        return ((0, "success"))

    def remote_cp(self, src, dst):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        common.exec_cmd(["scp",
                         "-F", self.ssh_config,
                         src,
                         self.ip_host[0]+":"+dst])
        return ((0, "success"))

    def remove_domain_from_known_host(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        common.exec_cmd(["ssh-keygen",
                         "-R", self.ip_host[0],
                         "-f", self.known_host])
        return ((0, "success"))
