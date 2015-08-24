Commands
======================================================================
EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF

    Command to the shell to terminate reading a script.


TEMPLATE
----------------------------------------------------------------------

Command - TEMPLATE::

    Usage:
        TEMPLATE list [--output=FORMAT]


    managing the TEMPLATEs test test test test

    Arguments:

      KEY    the name of the TEMPLATE
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [TEMPLATE: general]
       --output=FORMAT  the output format [TEMPLATE: table]



admin
----------------------------------------------------------------------

Command - admin::

    Usage:
      admin password reset
      admin password

    Options:


    Description:
      admin password reset
        Reset portal password



banner
----------------------------------------------------------------------

Command - banner::

    Usage:
        banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT

    Arguments:
        TEXT   The text message from which to create the banner
        CHAR   The character for the frame.
        WIDTH  Width of the banner
        INDENT indentation of the banner
        COLOR  the color

    Options:
        -c CHAR   The character for the frame. [default: #]
        -n WIDTH  The width of the banner. [default: 70]
        -i INDENT  The width of the banner. [default: 0]
        -r COLOR  The color of the banner. [default: BLACK]

    Prints a banner form a one line text message.


clear
----------------------------------------------------------------------

Command - clear::

    Usage:
        clear

    Clears the screen.

cloud
----------------------------------------------------------------------

Command - cloud::

    Usage:
        cloud list [--output=FORMAT]


    managing the admins test test test test

    Arguments:

      KEY    the name of the admin
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [cloud: general]
       --output=FORMAT  the output format [cloud: table]



cluster
----------------------------------------------------------------------

Command - cluster::

    Usage:
        cluster list [--output=FORMAT]


    managing the clusters test test test test

    Arguments:

      KEY    the name of the cluster
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [cluster: general]
       --output=FORMAT  the output format [cluster: table]



default
----------------------------------------------------------------------

Command - default::

    Usage:
        default list [--format=FORMAT]
        default delete KEY [--cloud=CLOUD]
        default KEY [--cloud=CLOUD]
        default KEY=VALUE [--cloud=CLOUD]


    managing the defaults test test test test

    Arguments:

      KEY    the name of the default
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [default: general]
       --format=FORMAT  the output format [default: table]



edit
----------------------------------------------------------------------

Command - edit::

    Usage:
            edit FILENAME

    Edits the file with the given name

    Arguments:
        FILENAME  the file to edit



exec
----------------------------------------------------------------------

Command - exec::

    Usage:
       exec FILENAME

    executes the commands in the file. See also the script command.

    Arguments:
      FILENAME   The name of the file


exp
----------------------------------------------------------------------

Command - exp::

    Usage:
        exp list [--output=FORMAT]


    managing the exps test test test test

    Arguments:

      KEY    the name of the exp
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [exp: general]
       --output=FORMAT  the output format [exp: table]



generate
----------------------------------------------------------------------

Command - generate::

    Usage:
        generate command COMMAND [--path=PATH] [--topic=TOPIC]

    the command will generate the package and code for a sample cmd3 module.

    Arguments:

        COMMAND   the name of the command.

        PATH      path where to place the directory [default: ~]

        TOPIC     the topic listed in cm [default: mycommands]

    Options:
         -v       verbose mode

    Example:

        The command

            generate command example

        would create in the home directory  the following files

            ├── LICENSE
            ├── Makefile
            ├── __init__.py
            ├── __init__.pyc
            ├── cloudmesh_example
            │   ├── __init__.py
            │   ├── command_example.py
            │   └── plugins
            │       ├── __init__.py
            │       └── cm_shell_example.py
            ├── requirements.txt
            ├── setup.cfg
            └── setup.py

        To install the plugin go to the directory and say

            python setup.py install

        Next register it in cm with

            cm plugins add cloudmesh_example

        Now say

            cm help

        and you see the command example in cm.
        To modify the command, yous change the docopts and the logic in
        cm_shell_example.py and command_example.py




group
----------------------------------------------------------------------

Command - group::

    Usage:
        group list [--output=FORMAT]
        group set NAME


    managing the exps test test test test

    Arguments:

      KEY    the name of the exp
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [exp: general]
       --output=FORMAT  the output format [exp: table]



help
----------------------------------------------------------------------

Command - help::
List available commands with "help" or detailed help with "help cmd".

info
----------------------------------------------------------------------

Command - info::

    Usage:
           info [--all]

    Options:
           --all  -a   more extensive information

    Prints some internal information about the shell



key
----------------------------------------------------------------------

Command - key::

    Usage:
      key  -h | --help
      key list [--source=db] [--format=FORMAT]
      key list --source=cloudmesh [--format=FORMAT]
      key list --source=ssh [--dir=DIR] [--format=FORMAT]
      key list --source=git [--format=FORMAT] [--username=USERNAME]
      key add [--name=KEYNAME] FILENAME
      key add --git [--name=KEYNAME] NAME
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
       --keyname=KEYNAME    the name of the keys
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



launcher
----------------------------------------------------------------------

Command - launcher::

    Usage:
        launcher list [--output=FORMAT]


    managing the launchers test test test test

    Arguments:

      KEY    the name of the launcher
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [launcher: general]
       --output=FORMAT  the output format [launcher: table]



limits
----------------------------------------------------------------------

Command - limits::

    Usage:
        limits [CLOUD...] [--format=FORMAT]

    Current usage data with limits on a selected project/tenant

    Arguments:

      CLOUD          Cloud name to see the usage

    Options:

       -v       verbose mode



list
----------------------------------------------------------------------

Command - list::

    Usage:
        list [--cloud=CLOUD]
        list [--cloud=CLOUD] default
        list [--cloud=CLOUD] vm
        list [--cloud=CLOUD] flavor
        list [--cloud=CLOUD] image



load
----------------------------------------------------------------------

Command - load::

    Usage:
        load MODULE

    Loads the plugin given a specific module name. The plugin must be ina plugin directory.

    Arguments:
       MODULE  The name of the module.


loglevel
----------------------------------------------------------------------

Command - loglevel::

    Usage:
      loglevel
      loglevel critical
      loglevel error
      loglevel warning
      loglevel info
      loglevel debug


    Shows current log level or changes it.

    Arguments:

    Description:

      loglevel - shows current log level
      critical - shows log message in critical level
      error    - shows log message in error level including critical
      warning  - shows log message in warning level including error
      info     - shows log message in info level including warning
      debug    - shows log message in debug level including info


    Options:




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



open
----------------------------------------------------------------------

Command - open::

    Usage:
            open FILENAME

    ARGUMENTS:
        FILENAME  the file to open in the cwd if . is
                  specified. If file in in cwd
                  you must specify it with ./FILENAME

    Opens the given URL in a browser window.


pause
----------------------------------------------------------------------

Command - pause::

    Usage:
        pause [MESSAGE]

    Displays the specified text then waits for the user to press RETURN.

    Arguments:
       MESSAGE  message to be displayed


plugins
----------------------------------------------------------------------

Command - plugins::

    Usage:
        plugins add COMMAND [--dryrun] [-q]
        plugins delete COMMAND [--dryrun] [-q]
        plugins list [--output=FORMAT] [-q]
        plugins activate

    Arguments:

        FORMAT   format is either yaml, json, or list [default=yaml]

    Options:

        -q        stands for quiet and suppresses additional messages

    Description:

        Please note that adding and deleting plugins requires restarting
        cm to activate them

        plugins list

            lists the plugins in the yaml file

        plugins add COMMAND
        plugins delete COMMAND

            cmd3 contains a ~/.cloudmesh/cmd3.yaml file.
            This command will add/delete a plugin for a given command
            that has been generated with cm-generate-command
            To the yaml this command will add to the modules

                - cloudmesh_COMMAND.plugins

            where COMMAND is the name of the command. In case we add
            a command and the command is out commented the comment
            will be removed so the command is enabled.

        plugins activate

            NOT YET SUPPORTED.

    Example:

        plugins add pbs


project
----------------------------------------------------------------------

Command - project::

    Usage:
        project list [--output=FORMAT]


    managing the projects test test test test

    Arguments:

      KEY    the name of the project
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [project: general]
       --output=FORMAT  the output format [project: table]



py
----------------------------------------------------------------------

Command - py::

    Usage:
        py
        py COMMAND

    Arguments:
        COMMAND   the command to be executed

    Description:

        The command without a parameter will be executed and the
        interactive python mode is entered. The python mode can be
        ended with ``Ctrl-D`` (Unix) / ``Ctrl-Z`` (Windows),
        ``quit()``,'`exit()``. Non-python commands can be issued with
        ``cmd("your command")``.  If the python code is located in an
        external file it can be run with ``run("filename.py")``.

        In case a COMMAND is provided it will be executed and the
        python interpreter will return to the command shell.

        This code is copied from Cmd2.


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


quota
----------------------------------------------------------------------

Command - quota::

    Usage:
        quota [CLOUD...] [--format=FORMAT]

    print quota limit on a current project/tenant

    Arguments:

      CLOUD          Cloud name

    Options:

       -v       verbose mode



refresh
----------------------------------------------------------------------

Command - refresh::

    Refreshes the database with information from the clouds


    Usage:
        refresh
        refresh status
        refresh list
        refresh CLOUD...

    Arguments:

        CLOUD  (parameterized) the name of a cloud

    Description:

        Refreshes are activated on all clouds that are "active". A cloud
        can be activated with the cloud command

           cloud activate CLOUD

        refresh
            refreshes the information that we have about all
            activeclouds.

        refresh CLOUD...
            refreshes the information form the specific clouds

        refresh status
            as the refresh may be done asynchronously, the stats will
            show you the progress of the ongoing refresh NOT
            IMPLEMENTED It also shows when the last refresh on a
            specific cloud object took place.

        refresh list
            lists all the Clouds that need a refresh

    Example:

         The following command sequences each refresh the clouds named
         india and aws.

             refresh india,aws
             refresh india aws
             refresh india
             refresh aws

      To utilize the refresh command without parameters you need to
      assure the clouds are activated

         cloud activate india
         cloud activate aws
         refresh


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


script
----------------------------------------------------------------------

Command - script::

    Usage:
           script
           script load
           script load LABEL FILENAME
           script load REGEXP
           script list
           script LABEL

    Arguments:
           load       indicates that we try to do actions toload files.
                      Without parameters, loads scripts from default locations
            NAME      specifies a label for a script
            LABEL     an identification name, it must be unique
            FILENAME  the filename in which the script is located
            REGEXP    Not supported yet.
                      If specified looks for files identified by the REGEXP.

    NOT SUPPORTED YET

       script load LABEL FILENAME
       script load FILENAME
       script load REGEXP

    Process FILE and optionally apply some options



search
----------------------------------------------------------------------

Command - search::

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



secgroup
----------------------------------------------------------------------

Command - secgroup::

    Usage:
        secgroup list CLOUD TENANT
        secgroup create CLOUD TENANT LABEL
        secgroup delete CLOUD TENANT LABEL
        secgroup rules-list CLOUD TENANT LABEL
        secgroup rules-add CLOUD TENANT LABEL FROMPORT TOPORT PROTOCOL CIDR
        secgroup rules-delete CLOUD TENANT LABEL FROMPORT TOPORT PROTOCOL CIDR
        secgroup -h | --help
        secgroup --version

    Options:
        -h            help message

    Arguments:
        CLOUD         Name of the IaaS cloud e.g. india_openstack_grizzly.
        TENANT        Name of the tenant, e.g. fg82.
        LABEL         The label/name of the security group
        FROMPORT      Staring port of the rule, e.g. 22
        TOPORT        Ending port of the rule, e.g. 22
        PROTOCOL      Protocol applied, e.g. TCP,UDP,ICMP
        CIDR          IP address range in CIDR format, e.g., 129.79.0.0/16

    Description:
        security_group command provides list/add/delete
        security_groups for a tenant of a cloud, as well as
        list/add/delete of rules for a security group from a
        specified cloud and tenant.


    Examples:
        $ secgroup list india fg82
        $ secgroup rules-list india fg82 default
        $ secgroup create india fg82 webservice
        $ secgroup rules-add india fg82 webservice 8080 8088 TCP "129.79.0.0/16"



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



setup
----------------------------------------------------------------------

Command - setup::

    Usage:
      setup init [--force]
      setup test

    Copies a cmd3.yaml file into ~/.cloudmesh/cmd3.yaml


setup_yaml
----------------------------------------------------------------------

Command - setup_yaml::

    Usage:
        setup_yaml  [--force]

    Copies a cmd3.yaml file into ~/.cloudmesh/cmd3.yaml


ssh
----------------------------------------------------------------------

Command - ssh::

    Usage:
        ssh list [--format=FORMAT]
        ssh register NAME PARAMETERS
        ssh NAME [--user=USER] [--key=KEY]


    conducts a ssh login into a machine while using a set of
    registered commands under the name of the machine.

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



stack
----------------------------------------------------------------------

Command - stack::

    Usage:
        stack list [--output=FORMAT]


    managing the stacks test test test test

    Arguments:

      KEY    the name of the stack
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [stack: general]
       --output=FORMAT  the output format [stack: table]



status
----------------------------------------------------------------------

Command - status::

    Usage:
        status
        status db
        status CLOUDS...




    Arguments:



    Options:





timer
----------------------------------------------------------------------

Command - timer::

    Usage:
        timer on
        timer off
        timer list
        timer start NAME
        timer stop NAME
        timer resume NAME
        timer reset [NAME]

    Description (NOT IMPLEMENTED YET):

         timer on | off
             switches timers on and off not yet implemented.
             If the timer is on each command will be timed and its
             time is printed after the command. Please note that
             background command times are not added.

        timer list
            list all timers

        timer start NAME
            starts the timer with the name. A start resets the timer to 0.

        timer stop NAME
            stops the timer

        timer resume NAME
            resumes the timer

        timer reset NAME
            resets the named timer to 0. If no name is specified all
            timers are reset

        Implementation note: we have a stopwatch in cloudmesh,
                             that we could copy into cmd3


use
----------------------------------------------------------------------

Command - use::

    USAGE:

        use list           lists the available scopes

        use add SCOPE      adds a scope <scope>

        use delete SCOPE   removes the <scope>

        use                without parameters allows an
                           interactive selection

    DESCRIPTION
       Often we have to type in a command multiple times. To save
       us typng the name of the command, we have defined a simple
       scope that can be activated with the use command

    ARGUMENTS:
        list         list the available scopes
        add          add a scope with a name
        delete       delete a named scope
        use          activate a scope



var
----------------------------------------------------------------------

Command - var::

    Usage:
        var list
        var delete NAMES
        var NAME=VALUE
        var NAME

    Arguments:
        NAME    Name of the variable
        NAMES   Names of the variable separated by spaces
        VALUE   VALUE to be assigned

    special vars date and time are defined


verbose
----------------------------------------------------------------------

Command - verbose::

    Usage:
        verbose (True | False)
        verbose

    If it sets to True, a command will be printed before execution.
    In the interactive mode, you may want to set it to False.
    When you use scripts, we recommend to set it to True.

    The default is set to False

    If verbose is specified without parameter the flag is
    toggled.



version
----------------------------------------------------------------------

Command - version::

    Usage:
       version

    Prints out the version number


vm
----------------------------------------------------------------------

Command - vm::

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



volume
----------------------------------------------------------------------

Command - volume::

    Usage:
        volume list
        volume create SIZE
                      [--snapshot-id=SNAPSHOT-ID]
                      [--image-id=IMAGE-ID]
                      [--display-name=DISPLAY-NAME]
                      [--display-description=DISPLAY-DESCRIPTION]
                      [--volume-type=VOLUME-TYPE]
                      [--availability-zone=AVAILABILITY-ZONE]
        volume delete VOLUME
        volume attach SERVER VOLUME DEVICE
        volume detach SERVER VOLUME
        volume show VOLUME
        volume SNAPSHOT-LIST
        volume snapshot-create VOLUME-ID
                               [--force]
                               [--display-name=DISPLAY-NAME]
                               [--display-description=DISPLAY-DESCRIPTION]
        volume snapshot-delete SNAPSHOT
        volume snapshot-show SNAPSHOT
        volume help


    volume management

    Arguments:
        SIZE              Size of volume in GB
        VOLUME            Name or ID of the volume to delete
        VOLUME-ID         ID of the volume to snapshot
        SERVER            Name or ID of server(VM).
        DEVICE            Name of the device e.g. /dev/vdb. Use "auto" for
                          autoassign (if supported)
        SNAPSHOT          Name or ID of the snapshot

    Options:
        --snapshot-id SNAPSHOT-ID     Optional snapshot id to create
                                      the volume from.  (Default=None)
        --image-id IMAGE-ID           Optional image id to create the
                                      volume from.  (Default=None)
        --display-name DISPLAY-NAME   Optional volume name. (Default=None)
        --display-description DISPLAY-DESCRIPTION
                                      Optional volume description. (Default=None)
        --volume-type VOLUME-TYPE
                                      Optional volume type. (Default=None)
        --availability-zone AVAILABILITY-ZONE
                                      Optional Availability Zone for
                                      volume. (Default=None)
        --force                       Optional flag to indicate whether to snapshot a
                                      volume even if its
                                      attached to an
                                      instance. (Default=False)

    Description:
        volume list
            List all the volumes
        volume create SIZE [options...]
            Add a new volume
        volume delete VOLUME
            Remove a volume
        volume attach SERVER VOLUME DEVICE
            Attach a volume to a server
        volume-detach SERVER VOLUME
            Detach a volume from a server
        volume show VOLUME
            Show details about a volume
        volume snapshot-list
            List all the snapshots
        volume snapshot-create VOLUME-ID [options...]
            Add a new snapshot
        volume snapshot-delete SNAPSHOT
            Remove a snapshot
        volume-snapshot-show SNAPSHOT
            Show details about a snapshot
        volume help
            Prints the nova manual


