
from common import common
from common import cli_fmwk
from provision import py_libvirt
import inspect

class provCLI(cli_fmwk.VCCli):
    def __init__(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="virtcluster provision cli")
        self.def_comp_lst=['domain', 'network']

    def postloop(self):
        py_libvirt.con_fin(self._con)
    def preloop(self):
        self._con = py_libvirt.con_init()

    def _complete_nwk_dom(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='domain':
                print("<domain name>")
                comp_type=['']
            if args[1]=='network':
                print("<network name>")
                comp_type=['']
        return comp_type

    def _complete_dom(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='domain':
                print("<domain name>")
                comp_type=['']
        return comp_type

    def _complete_network(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='network':
                print("<network name>")
                comp_type=['']
        return comp_type

    def do_domain(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        dom_cli=provCLI_domain()
        dom_cli.cmdloop()

    def help_domain(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Domain subcommands    ")

    def do_network(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        nwk_cli=provCLI_network()
        nwk_cli.cmdloop()

    def help_network(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Network subcommands    ")

    def do_info(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_info()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, ['domain'], arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.info_domain(dom)
        else:
            print("Enter domain")
            return

    def help_info(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Info domain <domain name>    ")

    def complete_info(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

    def do_list(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        py_libvirt.list_domains(self._con)

    def help_list(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     List domains    ")

    def do_dumpxml(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_dumpxml()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.dumpxml_domain(dom)
        elif comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            py_libvirt.dumpxml_network(nwk)
        else:
            print("Enter either domain or network")
            return

    def help_dumpxml(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Dump XML of either:      ")
        print("      domain <domain name>    ")
        print("             or               ")
        print("      network <network name>  ")

    def complete_dumpxml(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_nwk_dom(text, line, begidx, endidx)

class provCLI_domain(cli_fmwk.VCCli):
    def __init__(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="Domain subcommands")
        self.prompt = self.prompt[:-1]+':Domain)'
        self.def_comp_lst=['domain']

    def _complete_dom(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='domain':
                print("<domain name>")
                comp_type=['']
        return comp_type

    def do_define(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_define()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if dom:
                print("Domain already defined")
                return
        else:
            print("Enter domain ")
            return

    def help_define(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Define domain <domain name>    ")

    def complete_define(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

    def do_undefine(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            dom = py_libvirt.dom_undefine(dom)
        else:
            print("Enter network")
            return

    def help_undefine(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Undefine domain <domain name>    ")

    def complete_undefine(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_nwk_dom(text, line, begidx, endidx)

    def do_start(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.dom_start(dom)
        else:
            print("Enter domain")
            return

    def help_start(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Start domain <domain name>    ")

    def complete_start(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_nwk_dom(text, line, begidx, endidx)

    def do_stop(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.dom_stop(dom)
        else:
            print("Enter either domain or network")
            return

    def help_stop(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Stop domain <domain name>    ")

    def complete_stop(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_nwk_dom(text, line, begidx, endidx)

    def do_shut(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_shut()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.dom_shut(dom)
        else:
            print("Enter domain")
            return

    def help_shut(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Shut domain <domain name>    ")

    def complete_shut(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

    def do_pause(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_pause()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.dom_pause(dom)
        else:
            print("Enter domain")
            return

    def help_pause(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Pause domain <domain name>    ")

    def complete_pause(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

    def do_resume(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_resume()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['domain']:
            dom_name=arg_lst[1]
            dom = py_libvirt.dom_lookup(self._con, dom_name)
            if not dom:
                print("Domain not defined")
                return
            py_libvirt.dom_resume(dom)
        else:
            print("Enter domain")
            return

    def help_resume(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Resume domain <domain name>    ")

    def complete_resume(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_dom(text, line, begidx, endidx)

class provCLI_network(cli_fmwk.VCCli):
    def __init__(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        cli_fmwk.VCCli.__init__(self, intro="Network subcommands")
        self.prompt = self.prompt[:-1]+':Network)'
        self.def_comp_lst=['network']

    def _complete_network(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, text)

        args=line.split()
        if len(args) == 2 and line[-1] == ' ':
            #Second level.
            if args[1]=='network':
                print("<network name>")
                comp_type=['']
        return comp_type

    def do_define(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_define()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if nwk:
                print("Network already defined")
                return
            nwk = py_libvirt.network_defineXML(self._con, None)
        else:
            print("Enter network")
            return

    def help_define(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Define network <network name>  ")

    def complete_define(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        return self._complete_network(text, line, begidx, endidx)

    def do_undefine(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_undefine()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            nwk = py_libvirt.network_undefine(nwk)
        else:
            print("Enter network")
            return

    def help_undefine(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Undefine network <network name>  ")

    def complete_undefine(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_network(text, line, begidx, endidx)

    def do_start(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_start()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            py_libvirt.network_start(nwk)
        else:
            print("Enter network")
            return

    def help_start(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Start network <network name>  ")

    def complete_start(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_network(text, line, begidx, endidx)

    def do_stop(self, args):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))

        arg_lst=args.split()
        if len(arg_lst) != 2:
            self.help_stop()
            return

        comp_type=cli_fmwk.VCCli._autocomp(self, self.def_comp_lst, arg_lst[0])

        if comp_type==['network']:
            nwk_name=arg_lst[1]
            nwk = py_libvirt.network_lookup(self._con, nwk_name)
            if not nwk:
                print("Network not defined")
                return
            py_libvirt.network_stop(nwk)
        else:
            print("Enter network")
            return

    def help_stop(self):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        print("     Stop network <network name>  ")

    def complete_stop(self, text, line, begidx, endidx):
        common.log(common.debug,
                   "In Function {0}".format(inspect.stack()[0][3]))
        return self._complete_network(text, line, begidx, endidx)

if __name__=='__main__':
#    common.set_debug_lvl(common.debug)

    prov_cmd=provCLI()
    prov_cmd.cmdloop()

#    name = 'x86vm'
#    nwk_name = 'virtcluster_fabric0'
