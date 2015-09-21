from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


class VmCommand(object):

    topics = {"vm": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cloud")

    @command
    def do_vm(self, args, arguments):
        """
        ::

            Usage:
                vm start [--name=NAME]
                         [--count=COUNT]
                         [--cloud=CLOUD]
                         [--image=IMAGE_OR_ID]
                         [--flavor=FLAVOR_OR_ID]
                         [--group=GROUP]
                vm delete [NAME_OR_ID...]
                          [--group=GROUP]
                          [--cloud=CLOUD]
                          [--force]
                vm ip_assign [NAME_OR_ID...]
                             [--cloud=CLOUD]
                vm ip_show [NAME_OR_ID...]
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--format=FORMAT]
                           [--refresh]
                vm login NAME [--user=USER]
                         [--ip=IP]
                         [--cloud=CLOUD]
                         [--key=KEY]
                         [--command=COMMAND]
                vm list [CLOUD|--all]
                        [--group=GROUP]
                        [--refresh]
                        [--format=FORMAT]
                        [--columns=COLUMNS]
                        [--detail]

            Arguments:
                COMMAND   positional arguments, the commands you want to
                          execute on the server(e.g. ls -a) separated by ';',
                          you will get a return of executing result instead of login to
                          the server, note that type in -- is suggested before
                          you input the commands
                NAME      server name

            Options:
                --ip=IP          give the public ip of the server
                --cloud=CLOUD    give a cloud to work on, if not given, selected
                                 or default cloud will be used
                --count=COUNT    give the number of servers to start
                --detail         for table print format, a brief version
                                 is used as default, use this flag to print
                                 detailed table
                --flavor=FLAVOR_OR_ID  give the name or id of the flavor
                --group=GROUP          give the group name of server
                --image=IMAGE_OR_ID    give the name or id of the image
                --key=KEY        spicfy a key to use, input a string which
                                 is the full path to the public key file
                --user=USER      give the user name of the server that you want
                                 to use to login
                --name=NAME      give the name of the virtual machine
                --force          delete vms without user's confirmation
                --command=COMMAND
                                 specify the commands to be executed



            Description:
                commands used to start or delete servers of a cloud

                vm start [options...]       start servers of a cloud, user may specify
                                            flavor, image .etc, otherwise default values
                                            will be used, see how to set default values
                                            of a cloud: cloud help
                vm delete [options...]      delete servers of a cloud, user may delete
                                            a server by its name or id, delete servers
                                            of a group or servers of a cloud, give prefix
                                            and/or range to find servers by their names.
                                            Or user may specify more options to narrow
                                            the search
                vm ip_assign [options...]   assign a public ip to a VM of a cloud
                vm ip_show [options...]     show the ips of VMs
                vm login [options...]       login to a server or execute commands on it
                vm list [options...]        same as command "list vm", please refer to it

            Tip:
                give the VM name, but in a hostlist style, which is very
                convenient when you need a range of VMs e.g. sample[1-3]
                => ['sample1', 'sample2', 'sample3']
                sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']

            Examples:
                vm start --count=5 --group=test --cloud=india
                        start 5 servers on india and give them group
                        name: test

                vm delete --group=test --names=sample_[1-9]
                        delete servers on selected or default cloud with search conditions:
                        group name is test and the VM names are among sample_1 ... sample_9

                vm ip show --names=sample_[1-5,9] --format=json
                        show the ips of VM names among sample_1 ... sample_5 and sample_9 in
                        json format

        """
        # pprint(arguments)
        if arguments["start"]:
            name = arguments["--name"]
            count = arguments["--count"]
            cloud = arguments["--cloud"]
            image = arguments["--image"]
            flavor = arguments["--flavor"]
            group = arguments["--group"]
            Command_vm.start(name, count, cloud, image, flavor, group)
        elif arguments["delete"]:
            name_or_id = arguments["NAME_OR_ID"]
            group = arguments["--group"]
            cloud = arguments["--cloud"]
            force = arguments["--force"]
            Command_vm.delete(name_or_id, group, cloud, force)
        elif arguments["ip_assign"]:
            name_or_id = arguments["NAME_OR_ID"]
            cloud = arguments["--cloud"]
            Command_vm.ip_assign(name_or_id, cloud)

        elif arguments["ip_show"]:
            name_or_id = arguments["NAME_OR_ID"]
            group = arguments["--group"]
            cloud = arguments["--cloud"]
            output_format = arguments["--format"]
            refresh = arguments["--refresh"]
            Command_vm.ip_show(name_or_id, group, cloud, output_format, refresh)

        elif arguments["login"]:
            name = arguments["NAME"]
            user = arguments["--user"]
            ip = arguments["--ip"]
            cloud = arguments["--cloud"]
            key = arguments["--key"]
            commands = arguments["--command"]
            commands = commands.split(';')
            Command_vm.loging(name, user, ip, cloud, key, commands)

        elif arguments["list"]:
            if arguments["--all"]:
                cloud = "all"
            else:
                cloud = arguments["CLOUD"]
            group = arguments["--group"]
            refresh = arguments["--refresh"]
            output_format = arguments["--format"]
            columns = arguments["--columns"]
            detail = arguments["--detail"]

            Command_vm.list(group, refresh, output_format, columns, detail)
        pass


if __name__ == '__main__':
    command = cm_shell_vm()
    command.do_vm("list")
    command.do_vm("a=x")
    command.do_vm("x")
