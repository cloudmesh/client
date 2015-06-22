from __future__ import print_function
from cmd3.shell import command
from pprint import pprint
from cloudmesh_client.common.ConfigDict import Config
import os
import os.path
from cloudmesh_client.cloud.command_cloud import command_cloud
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.common.tables import dict_printer

class cm_shell_cloud:
    def activate_cm_shell_cloud(self):
        self.register_command_topic('cloud', 'register')
        self.register_command_topic('cloud', 'list')

    @command
    def do_list(self, args, arguments):
        """
        ::

          Usage:
              list [--cloud=CLOUD]
              list [--cloud=CLOUD] vm
              list [--cloud=CLOUD] flavor
              list [--cloud=CLOUD] image

        """
        pprint(arguments)

        def get_kind():
            for k in ["vm","image", "flavor"]:
                if arguments[k]:
                    return k
            return "help"

        if arguments["--cloud"] is None:
            cloud = "india"

        cm = CloudmeshDatabase(cm_user="gregor")
        kind = get_kind()
        if kind == "help":
            print ("HELP HERE")
        else:
            cm.update(kind, "india")
            result = cm.list(kind, output="flat")
            header = None
            if kind == 'flavor':
                order = [
                         'cm_cloud',
                         'disk',
                         'ephemeral_disk',
                         'id',
                         'name',
                         'ram',
                         'vcpus'
                        ]
            elif kind == 'image':
                order = [
                         'cm_cloud',
                         'cm_user',
                         'instance_type_ephemeral_gb',
                         'instance_type_flavorid',
                         'instance_type_id',
                         'instance_type_memory_mb',
                         'instance_type_name',
                         'instance_type_root_gb',
                         'instance_type_rxtx_factor',
                         'instance_type_swap',
                         'instance_type_vcpus',
                         'minDisk',
                         'minRam',
                         'name',
                        ]
                header = [
                         'cloud',
                         'user',
                         'ephemeral_gb',
                         'flavorid',
                         'id',
                         'memory_mb',
                         'flavor',
                         'root_gb',
                         'rxtx_factor',
                         'swap',
                         'vcpus',
                         'minDisk',
                         'minRam',
                         'name',
                        ]
            print (dict_printer(result,
                         order=order,
                         header=header,
                         output="table",
                         sort_keys=True,
                         show_none=""))

        # d = cm.get(FLAVOR)
        # print("9999")
        # pprint(d)
        # print("8888")


    @command
    def do_register(self, args, arguments):
        """
        ::

          Usage:
              register info
              register list [--yaml=FILENAME]
              register list ssh
              register cat [--yaml=FILENAME]
              register edit [--yaml=FILENAME]
              register form [--yaml=FILENAME]
              register check [--yaml=FILENAME]
              register test [--yaml=FILENAME]
              register rc HOST [OPENRC]
              register [--yaml=FILENAME]

          managing the registered clouds in the cloudmesh.yaml file.
          It looks for it in the current directory, and than in ~/.cloudmesh.
          If the file with the cloudmesh.yaml name is there it will use it.
          If neither location has one a new file will be created in
          ~/.cloudmesh/cloudmesh.yaml. Some defaults will be provided.
          However you will still need to fill it out with valid entries.

          Arguments:

            HOST   the host name
            USER   the user name
            OPENRC  the location of the openrc file

          Options:

             -v       verbose mode

          Description:

              register edit [--yaml=FILENAME]
                  edits the cloudmesh.yaml file

              register list [--yaml=FILENAME]
                  lists the registration yaml file

              register rc HOST [OPENRC]

                    reads the Openstack OPENRC file from a host that is described in ./ssh/config and adds it to the
                    configuration cloudmehs.yaml file. We assume that the file has already a template for this
                    host. If nt it can be created from other examples before you run this command.

                    The hostname can be specified as follows in the ./ssh/config file.

                    Host india
                        Hostname india.futuresystems.org
                        User yourusername

                    If the host is india and the OPENRC file is ommitted, it will automatically fill out the location
                    for the openrc file. To obtain the information from india simply type in

                        register rc india

              register [--yaml=FILENAME]
                  read the yaml file instead of ./cloudmesh.yaml or ~/.cloudmesh/cloudmesh.yaml which is used when the
                  yaml filename is ommitted.

              register edit [--yaml=FILENAME]
                  edits the cloudmesh yaml file

              register form [--yaml=FILENAME]
                  interactively fills out the form wherever we find TBD.

              register check [--yaml=FILENAME]
                  checks the yaml file for completness

              register test [--yaml=FILENAME]
                  checks the yaml file and executes tests to check if we
                  can use the cloud. TODO: maybe this should be in a test
                  command
        """
        pprint(arguments)

        def _get_file(arguments):
            if arguments["--yaml"]:
                filename = Config.find_file(arguments["--yaml"])
            else:
                filename = Config.find_file("cloudmesh.yaml")
            return filename

        if arguments["info"]:
            filename = _get_file(arguments)
            print("File", filename, end=' ')
            if os.path.isfile(filename):
                print("exists")
        elif arguments["cat"]:
            filename = _get_file(arguments)
            os.system("cat {:}".format(filename))
        elif arguments["edit"]:
            filename = _get_file(arguments)
            print("edit", filename)
            self.do_edit(filename)
        elif arguments['list'] and arguments['ssh']:
            print("list ssh")
            command_cloud.list_ssh()
        elif arguments['list']:
            filename = _get_file(arguments)
            print("list", filename)
            command_cloud.list(filename)
        elif arguments['check']:
            filename = _get_file(arguments)
            command_cloud.check_yaml_for_completeness(filename)
        elif arguments['--yaml']:
            filename = arguments['FILENAME']
            print("--yaml", filename)
            command_cloud.register(filename)
        elif arguments['test']:
            filename = _get_file(arguments)
            command_cloud.test(filename)
        elif arguments['form']:
            filename = _get_file(arguments)
            command_cloud.fill_out_form(filename)
        elif arguments['rc']:
            filename = arguments['OPENRC']
            host = arguments['HOST']
            command_cloud.read_rc_file(host, filename)
        pass


if __name__ == '__main__':
    command = cm_shell_register()
    command.do_register("list")
