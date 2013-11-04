
import common
import readline
import cmd

class VCCli(cmd.Cmd):
      def __init__(self, intro="virtcluster", prompt="(vc)"):
            cmd.Cmd.__init__(self)
            self.intro=intro
            self.prompt=prompt
            self.doc_header="virtcluster commands (type help <topic>):"
      def emptyline(self):
            pass
      def do_EOF(self, args):
            return True
      def help_EOF(self, args):
            return True
      def do_quit(self, args):
            return True
      def help_quit(self, args):
            return True
      def _autocomp(self, lst, text):
            return [i for i in lst if i.startswith(text)]
