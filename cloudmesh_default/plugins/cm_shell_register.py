from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
from cloudmesh_default.command_default import command_default

class cm_shell_register:

    def activate_cm_shell_register(self):
        self.register_command_topic('mycommands', 'register')

    @command
    def do_register(self, args, arguments):
        """
        ::

          Usage:
              register list
              register --rc OPENRC [--host=HOST] [--user=USER]
              register USER@HOST OPENRC
              register --yaml FILENAME
              register
              register edit
              register form
              register check
              register test

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

              register edit
                  edits the cloudmesh.yaml file

              register list
                  lists the registration yaml file

              register --type CLOUDTYPE --name NAME --rc OPENRC [--host=HOST] [--user=USER]
                  reads the openrc file and registers it under the given name
                  if this name already exists its values will be overwritten with
                  values from the OPENRC file

              register CLOUDTYPE NAME USER@HOST OPENRC
                  just as the above command with less verbose options

              register --yaml=FILENAME
                  read the yaml file instead of ./cloudmesh.yaml or ~/.cloudmesh/cloudmesh.yaml

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
        pass

if __name__ == '__main__':
    command = cm_shell_register()
    command.do_register("list")
