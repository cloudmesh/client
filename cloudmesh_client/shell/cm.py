import cmd
from plugins.KeyCommands import KeyCommands
import textwrap

from collections import namedtuple
# import inspect


class CloudmeshContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs



class CloudmeshConsole(cmd.Cmd,
                       KeyCommands):
    """
    CLoudmesh Console
    """
    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.context = context
        if self.context.debug:
            print "init CloudmeshConsole"

        self.prompt = 'cm> '


        self.banner = textwrap.dedent("""
            +=======================================================+
            .   ____ _                 _                     _      .
            .  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   .
            . | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  .
            . | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | .
            .  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| .
            +=======================================================+
                                 Cloudmesh Shell
            """)
        # KeyCommands.__init__(self, context)
        for c in CloudmeshConsole.__bases__[1:]:
            c.__init__(self, context)


    def preloop(self):
        """adds the banner to the preloop"""

        if self.context.splash:
            lines = textwrap.dedent(self.banner).split("\n")
            for line in lines:
                print line

    def do_EOF(self, args):
        """
        Usage:
            EOF

        Command to the shell to terminate reading a script.
        """
        return True

    def do_quit(self, args):
        """
        Usage:
            quit

        Action to be performed whne quit is typed
        """
        return True

    do_q = do_quit

    def emptyline(self):
        return


    def do_context(self, args):
        print self.context


if __name__ == '__main__':
    context = CloudmeshContext(debug=False,
                               splash=True)
    con = CloudmeshConsole(context)
    con.cmdloop()
