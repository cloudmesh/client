from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_key import command_key


class cm_shell_key:
    def activate_cm_shell_key(self):
        self.register_command_topic('cloud', 'key')

    @command
    def do_key(self, args, arguments):
        """
        ::

           Usage:
             key  -h | --help
             key list [--source=SOURCE] [--dir=DIR] [--format=FORMAT]
             key add [--keyname=KEYNAME] FILENAME
             key default [KEYNAME]
             key delete KEYNAME

           Manages the keys

           Arguments:

             SOURCE         mongo, yaml, ssh
             KEYNAME        The name of a key
             FORMAT         The format of the output (table, json, yaml)
             FILENAME       The filename with full path in which the key
                            is located

           Options:

              --dir=DIR            the directory with keys [default: ~/.ssh]
              --format=FORMAT      the format of the output [default: table]
              --source=SOURCE      the source for the keys [default: mongo]
              --keyname=KEYNAME    the name of the keys

           Description:


           key list --source=ssh  [--dir=DIR] [--format=FORMAT]

              lists all keys in the directory. If the directory is not
              specified the default will be ~/.ssh

           key list --source=yaml  [--dir=DIR] [--format=FORMAT]

              lists all keys in cloudmesh.yaml file in the specified directory.
               dir is by default ~/.cloudmesh

           key list [--format=FORMAT]

               list the keys in mongo

           key add [--keyname=keyname] FILENAME

               adds the key specifid by the filename to mongodb


           key list

                Prints list of keys. NAME of the key can be specified

           key default [NAME]

                Used to set a key from the key-list as the default key if NAME
                is given. Otherwise print the current default key

           key delete NAME

                deletes a key. In yaml mode it can delete only key that
                are not saved in mongo

        """
        pprint(arguments)


        if arguments['list']:
            print ('list')
            if arguments['--source']:
                source = arguments['--source']
                print (source)
            if arguments['--dir']:
                dir = arguments['--dir']
                print (dir)
            if arguments['--format']:
                format = arguments['--format']
                print (format)
        elif arguments['add']:
            print ('add')
            keyname = None
            if arguments['--keyname']:
                keyname = arguments['--keyname']
                print (keyname)
            filename = arguments['FILENAME']
            print (filename)
        elif arguments['default']:
            print ("default")
            if arguments['KEYNAME']:
                keyname = arguments['KEYNAME']
                print (keyname)
        elif arguments['delete']:
            print ('delete')
            if arguments['KEYNAME']:
                keyname = arguments['KEYNAME']
                print (keyname)


if __name__ == '__main__':
    command = cm_shell_key()
    command.do_key("list")
    command.do_key("a=x")
    command.do_key("x")
