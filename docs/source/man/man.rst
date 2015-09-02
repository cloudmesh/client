Commands
======================================================================
EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF

    Command to the shell to terminate reading a script.


bar
----------------------------------------------------------------------

Command - bar::

    Usage:
          bar -f FILE
          bar FILE
          bar list

    This command does some useful things.

    Arguments:
        FILE   a file name

    Options:
        -f      specify the file



context
----------------------------------------------------------------------

Command - context::

    Command documentation context missing, help_context

group
----------------------------------------------------------------------

Command - group::

      Usage:
          group info [--output=FORMAT]
          group add [--name=NAME] --id=IDs
          group add [--cloud=CLOUD] [--type=TABLE] --name=NAME
          group list [--cloud=CLOUD] [--type=TABLE] [--name=NAME]
          group delete [--cloud=CLOUD] [--type=TABLE] [--name=NAME]
          group copy FROM TO
          group merge GROUPA GROUPB MERGEDGROUP

      manage the groups

      Arguments:

        FROM    name of a group
        TO      name of a group
        GROUPA  name of a group
        GROUPB  name of a group
        GROUPC  name of a group

      Options:

         --cloud=CLOUD    the name of the cloud [default: general]
         --output=FORMAT  the output format [default: table]
         --type=TABLE     the table type [default: all]
         --name=NAME      the name of the group [default: None]

    Example:
        default group mygroup
        group add --type=vm --id=gregor-[001-003]
            # adds the vms with teh given name using the Parameter see base
        group delete --name=mygroup
            # deletes all objects in the group


help
----------------------------------------------------------------------

Command - help::
List available commands with "help" or detailed help with "help cmd".

key
----------------------------------------------------------------------

Command - key::

    Usage:
      key  -h | --help
      key list [--source=db] [--format=FORMAT]
      key list --source=cloudmesh [--format=FORMAT]
      key list --source=ssh [--dir=DIR] [--format=FORMAT]
      key list --source=git [--format=FORMAT] [--username=USERNAME]
      key add --git KEYNAME
      key add --ssh KEYNAME
      key add [--path=PATH]  KEYNAME
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
      --path=PATH           the path of the key [default: ~/.ssh/id_rsa.pub]
       --all                delete all keys

    Description:

    key list --source=git  [--username=USERNAME]

       lists all keys in git for the specified user. If the name is not specified it is read from cloudmesh.yaml

    key list --source=ssh  [--dir=DIR] [--format=FORMAT]

       lists all keys in the directory. If the directory is not
       specified the default will be ~/.ssh

    key list --source=cloudmesh  [--dir=DIR] [--format=FORMAT]

       lists all keys in cloudmesh.yaml file in the specified directory.
        dir is by default ~/.cloudmesh

    key list [--format=FORMAT]

        list the keys in teh giiven format: json, yaml, table. table is default

    key list

         Prints list of keys. NAME of the key can be specified


    key add [--name=keyname] FILENAME

        adds the key specifid by the filename to the key database


    key default [NAME]

         Used to set a key from the key-list as the default key if NAME
         is given. Otherwise print the current default key

    key delete NAME

         deletes a key. In yaml mode it can delete only key that
         are not saved in the database

    key rename NAME NEW

         renames the key from NAME to NEW.



man
----------------------------------------------------------------------

Command - man::

    Usage:
           man COMMAND
           man [--noheader]

    Options:
           --norule   no rst header

    Arguments:
           COMMAND   the command to be printed

    Description:
        man
            Prints out the help pages
        man COMMAND
            Prints out the help page for a specific command


nova
----------------------------------------------------------------------

Command - nova::

    Usage:
           nova set CLOUD
           nova info [CLOUD] [--password]
           nova help
           nova ARGUMENTS...

    A simple wrapper for the openstack nova command

    Arguments:

      ARGUMENTS      The arguments passed to nova
      help           Prints the nova manual
      set            reads the information from the current cloud
                     and updates the environment variables if
                     the cloud is an openstack cloud
      info           the environment values for OS

    Options:
       --password    Prints the password
       -v            verbose mode



q
----------------------------------------------------------------------

Command - q::

    Usage:
        quit

    Action to be performed whne quit is typed


quit
----------------------------------------------------------------------

Command - quit::

    Usage:
        quit

    Action to be performed whne quit is typed


register
----------------------------------------------------------------------

Command - register::

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
            checks the yaml file and executes tests to check if we
            can use the cloud. TODO: maybe this should be in a test
            command


select
----------------------------------------------------------------------

Command - select::

    Usage:
        select image [CLOUD]
        select flavor [CLOUD]
        select cloud [CLOUD]
        select key [CLOUD]

    selects interactively the default values

    Arguments:

      CLOUD    the name of the cloud

    Options:



ssh
----------------------------------------------------------------------

Command - ssh::

    Usage:
        ssh list [--format=FORMAT]
        ssh register NAME PARAMETERS
        ssh ARGUMENTS


    conducts a ssh login on a machine while using a set of
    registered machines specified in ~/.ssh/config

    Arguments:

      NAME        Name or ip of the machine to log in
      list        Lists the machines that are registered and
                  the commands to login to them
      PARAMETERS  Register te resource and add the given
                  parameters to the ssh config file.  if the
                  resoource exists, it will be overwritten. The
                  information will be written in /.ssh/config

    Options:

       -v       verbose mode
       --format=FORMAT   the format in which this list is given
                         formats incluse table, json, yaml, dict
                         [default: table]

       --user=USER       overwrites the username that is
                         specified in ~/.ssh/config

       --key=KEY         The keyname as defined in the key list
                         or a location that contains a pblic key


