from __future__ import print_function

import os
import os.path
import json

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.cloud.register import CloudRegister


class RegisterCommand(object):

    topics = {"register": "cloud"}

    def __init__(self, context):
        # super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print("init command register")

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
              register json HOST
              register [--yaml=FILENAME]
              register india [--force]
              register CLOUD CERT [--force]
              register CLOUD --dir=DIR

          managing the registered clouds in the cloudmesh.yaml file.
          It looks for it in the current directory, and than in
          ~/.cloudmesh.  If the file with the cloudmesh.yaml name is
          there it will use it.  If neither location has one a new
          file will be created in ~/.cloudmesh/cloudmesh.yaml. Some
          defaults will be provided.  However you will still need to
          fill it out with valid entries.

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

                    reads the Openstack OPENRC file from a host that
                    is described in ./ssh/config and adds it to the
                    configuration cloudmehs.yaml file. We assume that
                    the file has already a template for this host. If
                    nt it can be created from other examples before
                    you run this command.

                    The hostname can be specified as follows in the
                    ./ssh/config file.

                    Host india
                        Hostname india.futuresystems.org
                        User yourusername

                    If the host is india and the OPENRC file is
                    ommitted, it will automatically fill out the
                    location for the openrc file. To obtain the
                    information from india simply type in

                        register rc india

              register [--yaml=FILENAME]

                  read the yaml file instead of ./cloudmesh.yaml or
                  ~/.cloudmesh/cloudmesh.yaml which is used when the
                  yaml filename is ommitted.

              register edit [--yaml=FILENAME]
                  edits the cloudmesh yaml file

              register form [--yaml=FILENAME]
                  interactively fills out the form wherever we find TBD.

              register check [--yaml=FILENAME]
                  checks the yaml file for completness

              register test [--yaml=FILENAME]
	      
                  checks the yaml file and executes tests to check if
                  we can use the cloud. TODO: maybe this should be in
                  a test command

         """
        # pprint(arguments)

        def _get_file(arguments):
            if arguments["--yaml"]:
                filename = Config.find_file(arguments["--yaml"])
            else:
                filename = Config.find_file("cloudmesh.yaml")
            return filename

        if arguments["info"]:

            filename = _get_file(arguments)
            if os.path.isfile(filename):
                Console.ok('File ' + filename + " exists")
            else:
                Console.ok('File ' + filename + " does not exist")
            return

        elif arguments["cat"]:
            filename = _get_file(arguments)
            os.system("cat {:}".format(filename))
            return

        elif arguments["edit"]:
            filename = _get_file(arguments)
            Console.ok("edit", filename)
            self.do_edit(filename)
            return

        elif arguments['list'] and arguments['ssh']:

            CloudRegister.list_ssh()
            return

        elif arguments['list']:

            filename = _get_file(arguments)
            CloudRegister.list(filename)
            return

        elif arguments['check']:
            filename = _get_file(arguments)
            CloudRegister.check_yaml_for_completeness(filename)
            return

        elif arguments['--yaml']:
            filename = arguments['FILENAME']
            Console.ok("--yaml", filename)
            CloudRegister.from_file(filename)
            return

        elif arguments['test']:
            filename = _get_file(arguments)
            CloudRegister.test(filename)
            return
        elif arguments['form']:
            filename = _get_file(arguments)
            CloudRegister.fill_out_form(filename)
            return

        elif arguments['rc']:
            filename = arguments['OPENRC']
            host = arguments['HOST']
            CloudRegister.read_rc_file(host, filename)
            return

        elif arguments['json']:
            host = arguments['HOST']
            result = CloudRegister.get(host)
            print(json.dumps(result, indent=4))
            return

        elif arguments['india']:
            force = arguments['--force']
            CloudRegister.host("india", force)
            return

        elif arguments['CLOUD']:
            if arguments['CERT']:  # path to the cacert.pem
                cloud = arguments['CLOUD']
                path = arguments['CERT']
                force = False
                if arguments['--force']:
                    force = True
                CloudRegister.certificate(cloud, path, force)
            elif arguments['--dir']:
                cloud = arguments['CLOUD']
                dir = arguments['--dir']
                Console.ok(dir)
                CloudRegister.directory(cloud, dir)

        # if all fails do a simple list

        filename = _get_file(arguments)
        CloudRegister.list(filename)

        pass


if __name__ == '__main__':
    command = cm_shell_register()
    command.do_register("list")
