from __future__ import print_function
import json

import yaml

from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.Error import Error
from cloudmesh_client.cloud.key import Key

from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint


class KeyCommand(PluginCommand, CloudPluginCommand):
    topics = {"key": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command key")

    # noinspection PyUnusedLocal
    @command
    def do_key(self, args, arguments):
        """
        ::

           Usage:
             key  -h | --help
             key list --cloud=CLOUD
             key list --source=db [--format=FORMAT]
             key list --source=yaml [--format=FORMAT]
             key list --source=ssh [--dir=DIR] [--format=FORMAT]
             key list --source=git [--format=FORMAT] [--username=USERNAME]
             key list
             key load [--format=FORMAT]
             key add [NAME] [--source=FILENAME]
             key add [NAME] [--git]
             key add [NAME] [--ssh]
             key get NAME
             key default --select
             key delete (KEYNAME | --select | --all) [--force] [--active]
             key delete KEYNAME --cloud=CLOUD
             key upload [KEYNAME] [--cloud=CLOUD]
             key upload [KEYNAME] --active

           Manages the keys

           Arguments:

             CLOUD          The cloud
             NAME           The name of the key.
             SOURCE         db, ssh, all
             KEYNAME        The name of a key. For key upload it defaults to the default key name.
             FORMAT         The format of the output (table, json, yaml)
             FILENAME       The filename with full path in which the key
                            is located
             NAME_ON_CLOUD  Typically the name of the keypair on the cloud.

           Options:

              --dir=DIR                     the directory with keys [default: ~/.ssh]
              --format=FORMAT               the format of the output [default: table]
              --source=SOURCE               the source for the keys [default: db]
              --username=USERNAME           the source for the keys [default: none]
              --name=KEYNAME                The name of a key
              --all                         delete all keys
              --force                       delete the key form the cloud
              --name_on_cloud=NAME_ON_CLOUD Typically the name of the keypair on the cloud.

           Description:

           key list --source=git  [--username=USERNAME]

              lists all keys in git for the specified user. If the
              name is not specified it is read from cloudmesh.yaml

           key list --source=ssh  [--dir=DIR] [--format=FORMAT]

              lists all keys in the directory. If the directory is not
              specified the default will be ~/.ssh

           key list --source=yaml  [--dir=DIR] [--format=FORMAT]

              lists all keys in cloudmesh.yaml file in the specified directory.
               dir is by default ~/.cloudmesh

           key list [--format=FORMAT]

               list the keys in the giiven format: json, yaml,
               table. table is default

           key list

                Prints list of keys. NAME of the key can be specified

               
           key add [--name=keyname] FILENAME

               adds the key specifid by the filename to the key
               database

           key get NAME

               Retrieves the key indicated by the NAME parameter from database
               and prints its fingerprint.

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
        # pprint(arguments)

        invalid_names = ['tbd', 'none', "", 'id_rsa']

        def _print_dict(d, header=None, format='table'):
            if format == "json":
                return json.dumps(d, indent=4)
            elif format == "yaml":
                return yaml.dump(d, default_flow_style=False)
            elif format == "table":
                return Printer.write(d,
                                     order=["name",
                                            "comment",
                                            "uri",
                                            "fingerprint",
                                            "source"],
                                     output="table",
                                     sort_keys=True)
            else:
                return d
                # return Printer.write(d,order=['cm_id, name, fingerprint'])

        directory = Config.path_expand(arguments["--dir"])

        cloud = arguments["--cloud"] or Default.cloud

        if arguments['list']:
            _format = arguments['--format']
            _source = arguments['--source']
            _dir = arguments['--dir']

            if "--source" not in arguments and "--cloud" not in arguments:
                arguments["--source"] = 'db'

            pprint (arguments)

            if arguments['--cloud']:

                    #
                    # get key list from openstack cloud
                    #
                    keys = Key.list(cloud, format=_format)
                    if keys is None:
                        Console.ok("The Key list is empty")
                    else:
                        print(keys)
                    return ""

            elif arguments['--source'] == 'ssh':

                try:
                    sshm = SSHKeyManager()
                    sshm.get_from_dir(directory)

                    print("SSS", type(sshm.__keys__))
                    d = dict(sshm.__keys__)
                    print(d)
                    print(Printer.write(d,
                                        order=["name",
                                               "comment",
                                               "uri",
                                               "fingerprint",
                                               "source"],
                                        output="table"))

                    # d = dict(sshm.__keys__)

                    # print(_print_dict(d, format=_format))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Problem listing keys from ssh")

            elif arguments['--source'] in ['cm', 'cloudmesh', 'yaml']:

                try:
                    sshm = SSHKeyManager()
                    m = sshm.get_from_yaml(load_order=directory)
                    d = dict(m.__keys__)
                    print(_print_dict(d, format=_format))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Problem listing keys from `{:}`".format(arguments['--source']))

            elif arguments['--source'] in ['git']:

                username = arguments["--username"]
                # print(username)
                if username == 'none':
                    conf = ConfigDict("cloudmesh.yaml")
                    username = conf["cloudmesh.github.username"]

                sshm = SSHKeyManager()
                try:
                    sshm.get_from_git(username)
                    d = dict(sshm.__keys__)
                    print(_print_dict(d, format=_format))
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Problem listing git keys from database")
                    return ""

            elif arguments['--source'] == 'db':
                print ("RUTYUTRYT")
                try:
                    sshdb = SSHKeyDBManager()
                    d = sshdb.table_dict()
                    print ("HHHHH", d)
                    if d is not None or d != []:
                        print(_print_dict(d, format=arguments['--format']))
                        msg = "info. OK."
                        Console.ok(msg)
                    else:
                        Console.error("No keys in the database")
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Problem listing keys from database")



        elif arguments['get']:

            try:
                name = arguments['NAME']
                sshdb = SSHKeyDBManager()
                d = sshdb.table_dict()

                for key in d:
                    if key["name"] == name:
                        print("{:}: {:}".format(key['name'], key['fingerprint']))
                        msg = "info. OK."
                        Console.ok(msg)
                        return ""
                    else:
                        pass
                Console.error("The key is not in the database")
            except Exception as e:
                Error.traceback(e)
                Console.error("The key is not in the database")

        # key add [NAME] [--source=FILENAME]
        #     key add [NAME] [--git]

        elif arguments['add'] and arguments["--git"]:

            # Console.error("This feature is not yet implemented", traceflag=False)
            # return ""

            print('git add')
            sshdb = SSHKeyDBManager()

            data = dotdict(arguments)

            keyname = data.NAME

            #
            # get name
            #
            conf = ConfigDict("cloudmesh.yaml")
            data.username = conf["cloudmesh.github.username"]
            data.name = arguments['NAME'] or data.username

            #
            # get git username
            #
            data.username = ConfigDict("cloudmesh.yaml")["cloudmesh.github.username"]

            if str(data.name).lower() in invalid_names:
                Console.error("The github user name is not set in the yaml file", traceflag=False)
                return ""

            try:
                Console.msg("Retrieving github ssh keys for user {username}".format(**data))
                sshm = SSHKeyManager()
                sshm.get_from_git(data.username)
                d = dict(sshm.__keys__)
                # pprint(d)
            except Exception as e:
                Console.error("Problem adding keys to git for user: {username}".format(**data))
                return ""

            for name in d:
                key = d[name]
                if key['key'] is not None:
                    key["keyname"] = data.name + "_" + name
                    key["keyname"] = key["keyname"].replace("-", "_")
                    key["source"] = "git"
                    key["user"] = data.name
                    try:
                        o = dict(key)
                        o['value'] = key["string"]
                        sshdb.add_from_dict(key)
                    except Exception as e:
                        Console.error("The key {keyname} with that finger print already exists".format(**key),
                                      traceflag=False)

        elif arguments['add'] and not arguments["--git"]:

            #     key add [NAME] [--source=FILENAME]
            #     key add [NAME] [--git]

            sshdb = SSHKeyDBManager()

            data = dotdict()

            #
            # get name
            #
            conf = ConfigDict("cloudmesh.yaml")
            data.username = conf["cloudmesh.profile.username"]
            data.name = arguments['NAME'] or data.username

            data.filename = arguments['--source']
            if data.filename == "db" or data.filename is None:
                data.filename = Config.path_expand("~/.ssh/id_rsa.pub")

            if str(data.name).lower() in invalid_names:
                msg = ("Your choice of keyname {name} is insufficient. \n"
                       "You must be chosing a keyname that is distingct on all clouds. \n"
                       "Possible choices are your gmail name, your XSEDE name, or \n"
                       "some name that is uniqe. "
                       "Best is also to set this name in \n"
                       "cloudmesh.profile.username as "
                       "part of your \n~/cloudmesh/cloudmesh.yaml file.")
                Console.error(msg.format(**data), traceflag=False)
                return ""

            try:
                sshdb.add(data.filename,
                          data.name,
                          source="ssh",
                          uri="file://" + data.filename)
                print("Key {name} successfully added to the database".format(**data))
                msg = "info. OK."
                Console.ok(msg)

            except ValueError as e:
                Console.error("A key with this fingerprint already exists".format(**data), traceflag=False)
                Console.msg("Please use check with: key list")

            return ""

        elif arguments['default']:

            # print("default")

            if arguments['--select']:
                keyname = None
                try:
                    sshdb = SSHKeyDBManager()
                    select = sshdb.select()
                    if select != 'q':
                        keyname = select.split(':')[0]
                        print("Setting key: {:} as default.".format(keyname))
                        sshdb.set_default(keyname)
                        msg = "info. OK."
                        Console.ok(msg)
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Setting default for selected key {:} failed.".format(keyname))

            else:
                try:
                    sshdb = SSHKeyDBManager()
                    d = sshdb.table_dict()

                    for i in d:
                        if d[i]["is_default"] == "True":
                            key = d[i]
                            print("{:}: {:}".format(key['name'], key['fingerprint']))
                            msg = "info. OK."
                            Console.ok(msg)
                            return ""
                        else:
                            pass
                    Console.error("The key is not in the database")
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Problem retrieving default key.")

        elif arguments['delete'] and arguments["--cloud"]:

            key = dotdict({
                'cloud': arguments["--cloud"],
                'name': arguments["KEYNAME"]
            })
            try:
                Key.delete(key.name, key.cloud)
                msg = "info. OK."
                Console.ok(msg)
            except:
                Console.error("Problem deleting the key {name} on the cloud {cloud}".format(**key))

        elif arguments['delete']:

            # key delete (KEYNAME | --select| --all) [--force] [--active]

            data = dotdict({
                "on_cloud": arguments["--force"] or False,
                'all': arguments['--all'] or False,
                'active': arguments['--active'] or False,
                'keyname': arguments['KEYNAME'] or False,
                'clouds': arguments["--cloud"] or Default.cloud
            })

            pprint(data)

            if data.active or data.all:
                config = ConfigDict("cloudmesh.yaml")
                data.clouds = config["cloudmesh"]["active"]

            remove = []
            for cloud in data.clouds:
                if data.all:

                    keys = Key.list(cloud, format="dict", live=True)
                    for id in keys:
                        key = keys[id]
                        name = key["keypair__name"]
                        remove.append((name, cloud))

            for name, cloud in remove:
                try:
                    Key.delete(name, cloud)
                    Console.ok("Remove key {} from cloud {}.".format(name, cloud))
                except Exception as e:
                    Error.traceback(e)
                    Console.error("Remove key {} from cloud {}.".format(name, cloud), traceflag=False)

            #### delete in db.

            msg = "info. OK."
            Console.ok(msg)

        elif arguments['upload']:

            pprint(arguments)

            try:
                #
                # get username
                #
                conf = ConfigDict("cloudmesh.yaml")
                username = conf["cloudmesh"]["profile"]["username"]
                if username in ['None', 'TBD']:
                    username = None

                #
                # get cloudnames
                #
                clouds = []

                if arguments["--active"]:
                    cloud = 'active'
                else:
                    cloud = arguments["--cloud"] or Default.cloud

                if cloud == "all":
                    config = ConfigDict("cloudmesh.yaml")
                    clouds = config["cloudmesh"]["clouds"]
                elif cloud == 'active':
                    config = ConfigDict("cloudmesh.yaml")
                    clouds = config["cloudmesh"]["active"]
                else:
                    clouds.append(cloud)

                print("CCC", cloud, clouds)
                #
                # get keyname
                #

                for cloud in clouds:
                    status = 0
                    sshdb = SSHKeyDBManager()
                    sshm = SSHKeyManager()
                    keys = sshdb.find_all()
                    for key in keys:

                        print("upload key {} -> {}".format(key["name"],
                                                           cloud))

                        try:
                            status = sshm.add_key_to_cloud(
                                username,
                                key["name"],
                                cloud,
                                key["name"])

                        except Exception as e:
                            Console.error("problem")
                            if "already exists" in str(e):
                                print("key already exists. Skipping upload. OK.")
                        if status == 1:
                            print("Problem uploading key {} to {}. failed.".format(key["name"],
                                                                                   cloud))
                msg = "info. OK."
                Console.ok(msg)

            except Exception as e:
                Console.error("Problem adding key to cloud")
