from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command

from cloudmesh_search.command_search import command_search


class cm_shell_search:

    def activate_cm_shell_search(self):
        self.register_command_topic('mycommands', 'search')

    @command
    def do_search(self, args, arguments):
        """
        ::

          Usage:
              search [NAME] [FILTER]...

          search the table NAME on the database

          Arguments:

            NAME      Name of the table to search. If the name is not specified, the table DEFAULT will be searched
            FILTER    Filter to be used when searching

          Options:

             -v       verbose mode

        """
        # pprint(arguments)

        if arguments["NAME"] is None:
            command_search.do_search('default')
        elif arguments["NAME"]:
            filter = ""
            if (arguments["FILTER"]):
                filter = arguments["FILTER"]
            table = arguments["NAME"]
            command_search.do_search(table,filter)
        pass

if __name__ == '__main__':
    command = cm_shell_search()
    command.do_search("vm")
