from __future__ import print_function
# import os
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from pprint import pprint
# from cloudmesh_client.cloud.command_key import command_key
from cloudmesh_client.common.ConfigDict import Config
# from os import listdir
# from os.path import expanduser, isfile, abspath
# from cloudmesh_base.tables import dict_printer, two_column_table
from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_client.common.tables import dict_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
import yaml
import json
from cloudmesh_client.cloud.default import Default
# from cloudmesh_base.menu import num_choice, dict_choice


class KeyCommand(object):

    topics = {"key": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command key")

    @command
    def do_key(self, args, arguments):
        """
        ::

           Usage:
             key  -h | --help
             key list [--source=db] [--format=FORMAT]
             key list --source=cloudmesh [--format=FORMAT]
             key list --source=ssh [--dir=DIR] [--format=FORMAT]
             key list --source=git [--format=FORMAT] [--username=USERNAME]
             key add --git [--name=KEYNAME] FILENAME
             key add --ssh [--name=KEYNAME]
             key add [--name=KEYNAME] FILENAME
             key get NAME
             key default [KEYNAME | --select]
             key delete (KEYNAME | --select | --all) [-f]

           Manages the keys

           Arguments:

             SOURCE         db, ssh, all
             KEYNAME        The name of a key
             FORMAT         The format of the output (table, json, yaml)
             FILENAME       The filename with full path in which the key
                            is located

           Options:

              --dir=DIR            the directory with keys [default: ~/.ssh]
              --format=FORMAT      the format of the output [default: table]
              --source=SOURCE      the source for the keys [default: db]
              --username=USERNAME  the source for the keys [default: none]              
              --name=KEYNAME       The name of a key
              --all                delete all keys

           Description:

           key list --source=git  [--username=USERNAME]

              lists all keys in git for the specified user. If the
              name is not specified it is read from cloudmesh.yaml

           key list --source=ssh  [--dir=DIR] [--format=FORMAT]

              lists all keys in the directory. If the directory is not
              specified the default will be ~/.ssh

           key list --source=cloudmesh  [--dir=DIR] [--format=FORMAT]

              lists all keys in cloudmesh.yaml file in the specified directory.
               dir is by default ~/.cloudmesh

           key list [--format=FORMAT]

               list the keys in teh giiven format: json, yaml,
               table. table is default

           key list

                Prints list of keys. NAME of the key can be specified

               
           key add [--name=keyname] FILENAME

               adds the key specifid by the filename to the key
               database


           key default [NAME]

                Used to set a key from the key-list as the default key
                if NAME is given. Otherwise print the current default
                key

           key delete NAME

                deletes a key. In yaml mode it can delete only key that
                are not saved in the database

           key rename NAME NEW

                renames the key from NAME to NEW.
                
        """
        pprint(arguments)

        def _print_dict(d, header=None, format='table'):
            if format == "json":
                return json.dumps(d, indent=4)
            elif format == "yaml":
                return yaml.dump(d, default_flow_style=False)
            elif format == "table":
                return dict_printer(d,
                                    order=["name",
                                           "comment",
                                           "uri",
                                           "fingerprint",
                                           "source"],
                                    output="table",
                                    sort_keys=True)
            else:
                return d
                # return dict_printer(d,order=['cm_id, name, fingerprint'])

        directory = Config.path_expand(arguments["--dir"])

        if arguments['list']:
            _format = arguments['--format']
            _source = arguments['--source']
            _dir = arguments['--dir']

            if arguments['--source'] == 'ssh':

                sshm = SSHKeyManager()
                sshm.get_from_dir(directory)
                d = dict(sshm.__keys__)
                print(_print_dict(d, format=_format))
                msg = "info. OK."
                Console.ok(msg)

            elif arguments['--source'] in ['cm', 'cloudmesh']:

                sshm = SSHKeyManager()
                m = sshm.get_from_yaml(load_order=directory)
                d = dict(m.__keys__)
                print(_print_dict(d, format=_format))
                msg = "info. OK."
                Console.ok(msg)

            elif arguments['--source'] in ['git']:

                username = arguments["--username"]
                print(username)
                if username == 'none':
                    conf = ConfigDict("cloudmesh.yaml")
                    username = conf["cloudmesh.github.username"]

                sshm = SSHKeyManager()
                try:
                    sshm.get_from_git(username)
                except:
                    Console.error("problem reading keys from user: " + username)
                    return
                d = dict(sshm.__keys__)
                print(_print_dict(d, format=_format))
                msg = "info. OK."
                Console.ok(msg)

            elif arguments['--source'] == 'db':
                sshdb = SSHKeyDBManager()
                d = sshdb.table_dict()
                if d != {}:
                    print(_print_dict(d, format=arguments['--format']))
                    msg = "info. OK."
                    Console.ok(msg)
                else:
                    Console.error("No keys in the database")

        elif arguments['get']:

            name = arguments['NAME']
            sshdb = SSHKeyDBManager()
            d = sshdb.table_dict()
            try:
                for i in d:
                    if d[i]["name"] == name:
                        key = d[i]
                        print(key['fingerprint'])
                        msg = "info. OK."
                        Console.ok(msg)
                        return
                    else:
                        pass
                Console.error("The key is not in the database")
            except:
                Console.error("The key is not in the database")

        # key add --git KEYNAME
        #      key add --ssh KEYNAME
        #      key add [--path=PATH]  KEYNAME

        elif arguments['add'] and arguments["--git"]:

            print('git add')
            sshdb = SSHKeyDBManager()
            keyname = arguments['--name']
            gitkeyname = arguments['NAME']
            filename = arguments['FILENAME']

            # Are we adding to the database as well?
            # sshdb.add(filename, keyname, source="ssh", uri="file://"+filename)

            username = arguments["--username"]

            if username == 'none':
                conf = ConfigDict("cloudmesh.yaml")
                username = conf["cloudmesh.github.username"]
            print(username)

            sshm = SSHKeyManager()
            try:
                sshm.get_from_git(username)
                d = dict(sshm.__keys__)
                print(d)
            except:
                Console.error("problem reading keys from user: " + username)
                return

            try:
                # FIXME: correct code to add to git
                d[gitkeyname]['keyname'] = keyname
                d[gitkeyname]['user'] = None
                d[gitkeyname]['source'] = 'git'
                # sshdb.add_from_dict(d[gitkeyname])
            except:
                Console.error("the key may already there")

        elif arguments['add'] and arguments["--ssh"]:

            print('ssh dd')
            sshdb = SSHKeyDBManager()
            keyname = arguments['--name']
            filename = Config.path_expand("~/.ssh/id_rsa.pub")

            try:
                sshdb.add(filename, keyname, source="ssh", uri="file://" + filename)
            except Exception, e:
                import traceback
                print(traceback.format_exc())
                print (e)
                print (keyname)
                print (filename)
                Console.error("problem adding the key `{}` from file `{}`".format(keyname, filename))
        elif arguments['add'] and not arguments["--git"]:

            print('ssh dd')
            sshdb = SSHKeyDBManager()
            keyname = arguments['--name']
            filename = arguments['FILENAME']
            try:
                sshdb.add(filename, keyname, source="ssh", uri="file://" + filename)
                msg = "info. OK."
                Console.ok(msg)
            except Exception, e:
                import traceback
                print(traceback.format_exc())
                print (e)
                print (keyname)
                print (filename)
                Console.error("problem adding the key `{}` from file `{}`".format(keyname, filename))

        elif arguments['default']:

            print("default")
            if arguments['KEYNAME']:
                keyname = arguments['KEYNAME']
                sshdb = SSHKeyDBManager()
                sshdb.set_default(keyname)
                Default.set("key", keyname, "general")
                msg = "info. OK."
                Console.ok(msg)
            elif arguments['--select']:

                command = cm_shell_select()
                command.do_select("key")

            else:
                sshdb = SSHKeyDBManager()
                default = sshdb.object_to_dict(sshdb.get_default())
                print('default key', default)

        elif arguments['delete']:
            print('delete')
            if arguments['--all']:
                sshdb = SSHKeyDBManager()
                sshdb.delete_all()
                msg = "info. OK."
                Console.ok(msg)
            elif arguments['--select']:
                sshdb = SSHKeyDBManager()
                select = sshdb.select()
                if select != 'q':
                    keyname = select.split(':')[0]
                    print(keyname)
                sshdb.delete(keyname)
                msg = "info. OK."
                Console.ok(msg)
            else:
                keyname = arguments['KEYNAME']
                sshdb = SSHKeyDBManager()
                sshdb.delete(keyname)
                msg = "info. OK."
                Console.ok(msg)


if __name__ == '__main__':
    command = cm_shell_key()
    command.do_key("list")
    command.do_key("a=x")
    command.do_key("x")
