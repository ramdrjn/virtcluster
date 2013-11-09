
import common
import readline
import cmd
import sys

class VCCli(cmd.Cmd):
      def __init__(self, intro="virtcluster", prompt="(vc)"):
            cmd.Cmd.__init__(self)
            self.intro=intro
            self.prompt=prompt
            self.doc_header="virtcluster commands (type help <topic>):"
      def emptyline(self):
            pass
      def do_end(self, args):
            return True
      def help_end(self, args):
            print("End session")
      do_EOF = do_end
      help_EOF = help_end
      def do_quit(self, args):
            return True
      def help_quit(self, args):
            print("Quit session")
      def _autocomp(self, lst, text):
            return [i for i in lst if i.startswith(text)]
