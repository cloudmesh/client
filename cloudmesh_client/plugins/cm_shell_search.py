from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint

from cloudmesh_client.cloud.command_search import command_search


class cm_shell_search:
    def activate_cm_shell_search(self):
        self.register_command_topic('cloud', 'search')

    @command
    def do_search(self, args, arguments):
        """
        ::

          Usage:
              search NAME
              search NAME [--order=FORMAT] [FILTER]...

          search the table NAME on the database

          Arguments:

            NAME            Name of the table to search. If the name is
                            not specified, the table DEFAULT will be searched
            --order=FORMAT  Columns that will be displayed
            FILTER          Filter to be used when searching

          Options:

             -v       verbose mode

        """

        if arguments["NAME"] is None:
            # command_search.do_search('default','')
            print(self.do_search.__doc__)
        elif arguments["NAME"]:
            format = ""
            filter = ""
            if arguments["--order"]:
                format = arguments["--order"]
            if arguments["FILTER"]:
                filter = arguments["FILTER"]
            table = arguments["NAME"]
            command_search.do_search(table, format, filter)
        pass


if __name__ == '__main__':
    command = cm_shell_search()
    command.do_search("vm")
