from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_loglevel import command_loglevel


class cm_shell_loglevel:
    def activate_cm_shell_loglevel(self):
        self.register_command_topic('cloud', 'loglevel')

    @command
    def do_loglevel(self, args, arguments):
        """
        ::

          Usage:
            loglevel
            loglevel critical
            loglevel error
            loglevel warning
            loglevel info
            loglevel debug


          Shows current log level or changes it.

          Arguments:

          Description:

            loglevel - shows current log level
            critical - shows log message in critical level
            error    - shows log message in error level including critical
            warning  - shows log message in warning level including error
            info     - shows log message in info level including warning
            debug    - shows log message in debug level including info


          Options:


        """
        pprint(arguments)

        if arguments['critical']:
            print ('critical')
        elif arguments['error']:
            print ("error")
        elif arguments['warning']:
            print ("warning")
        elif arguments['info']:
            print ("info")
        elif arguments['debug']:
            print ("debug")
        else:
            print ("loglevel")


if __name__ == '__main__':
    command = cm_shell_loglevel()
    command.do_loglevel("list")
    command.do_loglevel("a=x")
    command.do_loglevel("x")
