from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_key import command_key
from cloudmesh_base.util import path_expand
from os import listdir
from os.path import expanduser, isfile, abspath
from cloudmesh_base.tables import dict_printer, two_column_table
from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_client.common.tables import dict_printer

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
             key default [KEYNAME | --select]
             key delete (KEYNAME | --select | --all)

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
              --source=SOURCE      the source for the keys [default: ssh]
              --keyname=KEYNAME    the name of the keys
              --all                delete all keys

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
        sshm = SSHKeyManager()
        sshdb = SSHKeyDBManager()

        def _print_dict(d, header=None, format='table'):
            if format == "json":
                return json.dumps(d, indent=4)
            elif format == "yaml":
                return yaml.dump(d, default_flow_style=False)
            else:
                return two_column_table(d, header)


        directory = path_expand(arguments["--dir"])

        if arguments['list']:
            print('list')
            d = sshdb.dict()
            print (d)

            """
            if arguments['--source'] == 'ssh':
                source = arguments['--source']
                files = _find_keys(directory)

                ssh_keys = {}

                for key in files:
                    ssh_keys[key] = directory + "/" + key
                print(ssh_keys)

            print(_print_dict(ssh_keys))
            if arguments['--dir']:
                dir = arguments['--dir']
                print(dir)
            if arguments['--format']:
                format = arguments['--format']
                print(format)
            """

        elif arguments['add']:
            print('add')
            keyname = arguments['--keyname']
            filename = arguments['FILENAME']
            sshdb.add(filename, keyname)

        elif arguments['default']:
            print("default")
            if arguments['KEYNAME']:
                keyname = arguments['KEYNAME']
                sshdb.set_default(keyname)
            elif arguments['--select']:
                select = sshdb.select()
                if select != 'q':
                    keyname = select.split(':')[0]
                    print (keyname)
                sshdb.set_default(keyname)
            else:
                default = sshdb.object_to_dict(sshdb.get_default())
                print ('default key', default)

        elif arguments['delete']:
            print('delete')
            if arguments['--all']:
                sshdb.delete_all()
            elif arguments['--select']:
                select = sshdb.select()
                if select != 'q':
                    keyname = select.split(':')[0]
                    print (keyname)
                sshdb.delete(keyname)
            else:
                keyname = arguments['KEYNAME']
                sshdb.delete(keyname)



if __name__ == '__main__':
    command = cm_shell_key()
    command.do_key("list")
    command.do_key("a=x")
    command.do_key("x")
