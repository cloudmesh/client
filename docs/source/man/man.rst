Commands
======================================================================
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
        cloud list [--cloud=CLOUD] [--format=FORMAT]
        cloud activate CLOUD
        cloud deactivate CLOUD
        cloud info CLOUD

    managing the admins test test test test

    Arguments:
      KEY    the name of the admin
      VALUE  the value to set the key to

    Options:
       --cloud=CLOUD    the name of the cloud [default: general]
       --format=FORMAT  the output format [default: table]

    Description:
       Cloudmesh contains a cloudmesh.yaml file that contains
       templates for multiple clouds that you may or may not have
       access to. Hence it is useful to activate and deacivate clouds
       you like to use in other commands.

       To activate a cloud a user can simply use the activate
       command followed by the name of the cloud to be
       activated. To find out which clouds are available you can
       use the list command that will provide you with some
       basic information. As default it will print a table. Thus
       the commands       cloud activate india
         cloud deactivate aws

       Will result in

          +----------------------+--------+-------------------+
          | Cloud name           | Active | Type              |
          +----------------------+--------+-------------------+
          | india                | True   | Openstack         |
          +----------------------+--------+-------------------+
          | aws                  | False  | AWS               |
          +----------------------+--------+-------------------+

       To get ore information about the cloud you can use the command

          cloud info CLOUD

       It will call internally also the command uses in register

    See also:
       register


color
----------------------------------------------------------------------

Command - color::

    Usage:
        color FLAG

    Arguments:

        FLAG    color mode flag ON/OFF

    Description:

        Global switch for the console color mode.
        One can switch the color mode on/off with
            cm color mode ON
            cm color mode OFF

        By default, the color mode is ON

    Examples:
        color mode ON
        color mode OFF


comet
----------------------------------------------------------------------

Command - comet::

    Usage:
       comet status
       comet tunnel start
       comet tunnel stop
       comet tunnel status
       comet logon
       comet logoff
       comet ll [ID] [--format=FORMAT]
       comet docs
       comet info [--user=USER]
                    [--project=PROJECT]
                    [--format=FORMAT]
       comet cluster [ID][--name=NAMES]
                    [--user=USER]
                    [--project=PROJECT]
                    [--hosts=HOSTS]
                    [--start=TIME_START]
                    [--end=TIME_END]
                    [--hosts=HOSTS]
                    [--format=FORMAT]
       comet computeset [COMPUTESETID]
       comet start ID
       comet stop ID
       comet power (on|off|reboot|reset|shutdown) CLUSTERID PARAM
       comet delete [all]
                      [--user=USER]
                      [--project=PROJECT]
                      [--name=NAMES]
                      [--hosts=HOSTS]
                      [--start=TIME_START]
                      [--end=TIME_END]
                      [--host=HOST]
       comet delete --file=FILE
       comet update [--name=NAMES]
                      [--hosts=HOSTS]
                      [--start=TIME_START]
                      [--end=TIME_END]
       comet add [--user=USER]
                   [--project=PROJECT]
                   [--host=HOST]
                   [--description=DESCRIPTION]
                   [--start=TIME_START]
                   [--end=TIME_END]
                   NAME
       comet add --file=FILENAME

    Options:
        --user=USER           user name
        --name=NAMES          Names of the vcluster
        --start=TIME_START    Start time of the vcluster, in
                              YYYY/MM/DD HH:MM:SS format.
                              [default: 1901-01-01]
        --end=TIME_END        End time of the vcluster, in YYYY/MM/DD
                              HH:MM:SS format. In addition a duratio
                              can be specified if the + sign is the
                              first sig The duration will than be
                              added to the start time.
                              [default: 2100-12-31]
        --project=PROJECT     project id
        --host=HOST           host name
        --description=DESCRIPTION  description summary of the vcluster
        --file=FILE           Adding multiple vclusters from one file
        --format=FORMAT       Format is either table, json, yaml,
                              csv, rest
                              [default: table]

    Arguments:
        FILENAME  the file to open in the cwd if . is
                  specified. If file in in cwd
                  you must specify it with ./FILENAME

    Opens the given URL in a browser window.


context
----------------------------------------------------------------------

Command - context::

    Usage:
        context

    Description:
        Lists the context variables and their values


default
----------------------------------------------------------------------

Command - default::

      Usage:
          default list [--cloud=CLOUD] [--format=FORMAT] [--all]
          default delete KEY [--cloud=CLOUD]
          default KEY [--cloud=CLOUD]
          default KEY=VALUE [--cloud=CLOUD]

      Arguments:

        KEY    the name of the default
        VALUE  the value to set the key to

      Options:

         --cloud=CLOUD    the name of the cloud
         --format=FORMAT  the output format [default: table]
         --all            lists all the default values

    Description:


        Cloudmesh has the ability to manage easily multiple
        clouds. One of the key concepts to make the list of such
        clouds easier is the introduction of defaults for each
        cloud or globally. Hence it is possible to set default
        images, flavors for each cloud, and also the default
        cloud. The default command is used to set and list the
        default values. These defaults are used in other commands
        if they are not overwritten by a command parameter.


    The current default values can by listed with --all option:(
    if you have a default cloud specified. You can also add a
    cloud parameter to apply the command to a specific cloud)

           default list

        A default can be set with

            default KEY=VALUE

        To look up a default value you can say

            default KEY

        A default can be deleted with

            default delete KEY


    Examples:
        default list --all
        default list --cloud=general
        default image=xyz
        default image=abc --cloud=kilo
        default image
        default image --cloud=kilo
        default delete image
        default delete image --cloud=kilo


EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF

    Description:
        Command to the shell to terminate reading a script.


exec
----------------------------------------------------------------------

Command - exec::

    Usage:
       exec FILENAME

    executes the commands in the file. See also the script command.

    Arguments:
      FILENAME   The name of the file


flavor
----------------------------------------------------------------------

Command - flavor::

    Usage:
        flavor refresh [--cloud=CLOUD]
        flavor list [ID] [--cloud=CLOUD] [--format=FORMAT] [--refresh]

        This lists out the flavors present for a cloud

    Options:
       --format=FORMAT  the output format [default: table]
       --cloud=CLOUD    the cloud name
       --refresh        refreshes the data before displaying it
                        from the cloud

    Examples:
        cm flavor refresh
        cm flavor list
        cm flavor list --format=csv
        cm flavor show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh



group
----------------------------------------------------------------------

Command - group::

    Usage:
        group add NAME [--type=TYPE] [--cloud=CLOUD] [--id=IDs]
        group list [--cloud=CLOUD] [--format=FORMAT] [NAME]
        group delete NAME [--cloud=CLOUD]
        group remove [--cloud=CLOUD] --name=NAME --id=ID
        group copy FROM TO
        group merge GROUPA GROUPB MERGEDGROUP

    manage the groups

    Arguments:

        NAME         name of a group
        FROM         name of a group
        TO           name of a group
        GROUPA       name of a group
        GROUPB       name of a group
        MERGEDGROUP  name of a group

    Options:
        --cloud=CLOUD    the name of the cloud
        --format=FORMAT  the output format
        --type=TYPE     the resource type
        --name=NAME      the name of the group


    Description:

        Todo: design parameters that are useful and match
        description
        Todo: discuss and propose command

        cloudmesh can manage groups of resources and cloud related
        objects. As it would be cumbersome to for example delete
        many virtual machines or delete VMs that are in the same
        group, but are running in different clouds.

        Hence it is possible to add a virtual machine to a
        specific group. The group name to be added to can be set
        as a default. This way all subsequent commands use this
        default group. It can also be set via a command parameter.
        Another convenience function is that the group command can
        use the last used virtual machine. If a vm is started it
        will be automatically added to the default group if it is set.

        The delete command has an optional cloud parameter so that
        deletion of vms of a partial group by cloud can be
        achieved.

        If finer grained deletion is needed, it can be achieved
        with the delete command that supports deletion by name

        It is also possible to remove a VM from the group using the
        remove command, by supplying the ID

    Example:
        default group mygroup

        group add --type=vm --id=albert-[001-003]
            adds the vms with teh given name using the Parameter
            see base

        group add --type=vm
         adds the last vm to the group

        group delete --name=mygroup
            deletes all objects in the group


help
----------------------------------------------------------------------

Command - help::

    Usage:
        help
        help COMMAND

    Description:
        List available commands with "help" or detailed help with
        "help COMMAND".

hpc
----------------------------------------------------------------------

Command - hpc::

    Usage:
        hpc queue [--name=NAME][--cluster=CLUSTER][--format=FORMAT]
        hpc info [--cluster=CLUSTER][--format=FORMAT]
        hpc run SCRIPT [--queue=QUEUE] [--t=TIME] [--N=nodes] [--name=NAME] [--cluster=CLUSTER][--dir=DIR][--group=GROUP][--format=FORMAT]
        hpc kill --job=NAME [--cluster=CLUSTER][--group=GROUP]
        hpc kill all [--cluster=CLUSTER][--group=GROUP][--format=FORMAT]
        hpc status [--cluster=CLUSTER][--group=GROUP][--job=ID]
        hpc test --cluster=CLUSTER [--time=SECONDS]

    Options:
       --format=FORMAT  the output format [default: table]

    Examples:

        Special notes

           if the group is specified only jobs from that group are
           considered. Otherwise the default group is used. If the
           group is set to None, all groups are used.

        cm hpc queue
            lists the details of the queues of the hpc cluster

        cm hpc queue --name=NAME
            lists the details of the job in the queue of the hpc cluster

        cm hpc info
            lists the details of the hpc cluster

        cm hpc run SCRIPT
            submits the script to the cluster. The script will be
            copied prior to execution into the home directory on the
            remote machine. If a DIR is specified it will be copied
            into that dir.
            The name of the script is either specified in the script
            itself, or if not the default nameing scheme of
            cloudmesh is used using the same index incremented name
            as in vms fro clouds: cloudmeshusername-index

        cm hpc kill all
            kills all jobs on the default hpc cluster

        cm hpc kill all -cluster=all
            kills all jobs on all clusters

        cm hpc kill --job=NAME
            kills a job with a given name or job id

        cm hpc default cluster=NAME
            sets the default hpc cluster

        cm hpc status
            returns the status of all jobs

        cm hpc status job=ID
            returns the status of the named job

        cm hpc test --cluster=CLUSTER --time=SECONDS
            submits a simple test job to the named cluster and returns
            if the job could be successfully executed. This is a
            blocking call and may take a long time to complete
            dependent on if the queuing system of that cluster is
            busy. It will only use one node/core and print the message

            #CLOUDMESH: Test ok

            in that is being looked for to identify if the test is
            successful. If time is used, the job is terminated
            after the time is elapsed.

    Examples:
        cm hpc queue
        cm hpc queue --name=xxx
        cm hpc info
        cm hpc kill --job=6
        cm hpc run uname


image
----------------------------------------------------------------------

Command - image::

    Usage:
        image refresh [--cloud=CLOUD]
        image list [ID] [--cloud=CLOUD] [--format=FORMAT] [--refresh]

        This lists out the images present for a cloud

    Options:
       --format=FORMAT  the output format [default: table]
       --cloud=CLOUD    the cloud name
       --refresh        live data taken from the cloud

    Examples:
        cm image refresh
        cm image list
        cm image list --format=csv
        cm image list 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh



inventory
----------------------------------------------------------------------

Command - inventory::

    Usage:
        inventory add NAMES [--label=LABEL]
                            [--service=SERVICES]
                            [--project=PROJECT]
                            [--owners=OWNERS]
                            [--comment=COMMENT]
                            [--cluster=CLUSTER]
                            [--ip=IP]
        inventory set NAMES for ATTRIBUTE to VALUES
        inventory delete NAMES
        inventory clone NAMES from SOURCE
        inventory list [NAMES] [--format=FORMAT] [--columns=COLUMNS]
        inventory info

    Arguments:

      NAMES     Name of the resources (example i[10-20])

      FORMAT    The format of the output is either txt,
                yaml, dict, table [default: table].

      OWNERS    a comma separated list of owners for this resource

      LABEL     a unique label for this resource

      SERVICE   a string that identifies the service

      PROJECT   a string that identifies the project

      SOURCE    a single host name to clone from

      COMMENT   a comment

    Options:

       -v       verbose mode

    Description:

          add -- adds a resource to the resource inventory

          list -- lists the resources in the given format

          delete -- deletes objects from the table

          clone -- copies the content of an existing object
                   and creates new once with it

          set   -- sets for the specified objects the attribute
                   to the given value or values. If multiple values
                   are used the values are assigned to the and
                   objects in order. See examples

          map   -- allows to set attibutes on a set of objects
                   with a set of values

    Examples:

      cm inventory add x[0-3] --service=openstack

          adds hosts x0, x1, x2, x3 and puts the string
          openstack into the service column

      cm lists

          lists the repository

      cm x[3-4] set temperature to 32

          sets for the resources x3, x4 the value of the
          temperature to 32

      cm x[7-8] set ip 128.0.0.[0-1]

          sets the value of x7 to 128.0.0.0
          sets the value of x8 to 128.0.0.1

      cm clone x[5-6] from x3

          clones the values for x5, x6 from x3



key
----------------------------------------------------------------------

Command - key::

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



launcher
----------------------------------------------------------------------

Command - launcher::

      Usage:
          launcher list [--cloud=CLOUD] [--format=FORMAT] [--all]
          launcher kill KEY [--cloud=CLOUD]
          launcher run
          launcher resume
          launcher suspend
          launcher details
          launcher clear
          launcher refresh

      Arguments:

        KEY    the name of the launcher

      Options:

         --cloud=CLOUD    the name of the cloud
         --format=FORMAT  the output format [launcher: table]
         --all            lists all the launcher values

    Description:

    Launcher is a command line tool to test the portal launch functionalities through command

    The current launcher values can by listed with --all option:(
    if you have a launcher cloud specified. You can also add a
    cloud parameter to apply the command to a specific cloud)

           launcher list

        A launcher can be deleted with

            launcher kill KEY


    Examples:
        launcher list --all
        launcher list --cloud=general
        launcher kill <KEY>


limits
----------------------------------------------------------------------

Command - limits::

    Usage:
        limits list [--cloud=CLOUD] [--tenant=TENANT] [--format=FORMAT]

        Current list data with limits on a selected project/tenant.
        The --tenant option can be used by admin only

    Options:
       --format=FORMAT  the output format [default: table]
       --cloud=CLOUD    the cloud name
       --tenant=TENANT  the tenant name

    Examples:
        cm limits list
        cm limits list --cloud=juno --format=csv



list
----------------------------------------------------------------------

Command - list::

    Usage:
        list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] default
        list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] vm
        list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] flavor
        list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] image

    List the items stored in the database

    Options:
        --cloud=CLOUD    the name of the cloud
        --format=FORMAT  the output format
        --tenant=TENANT     Name of the tenant, e.g. fg82.

    Description:
        List command prints the values stored in the database
        for [default/vm/flavor/image].
        Result can be filtered based on the cloud, user & tenant arguments.
        If these arguments are not specified, it reads the default

    Examples:
        $ list --cloud india default
        $ list --cloud india --format table flavor
        $ list --cloud india --user albert --tenant fg82 flavor


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


network
----------------------------------------------------------------------

Command - network::

    Usage:
        network get fixed [ip] [--cloud=CLOUD] FIXED_IP
        network get floating [ip] [--cloud=CLOUD] FLOATING_IP_ID
        network reserve fixed [ip] [--cloud=CLOUD] FIXED_IP
        network unreserve fixed [ip] [--cloud=CLOUD] FIXED_IP
        network associate floating [ip] [--cloud=CLOUD] --server=SERVER FLOATING_IP
        network disassociate floating [ip] [--cloud=CLOUD] --server=SERVER FLOATING_IP
        network create floating [ip] [--cloud=CLOUD] --pool=FLOATING_IP_POOL
        network delete floating [ip] [--cloud=CLOUD] FLOATING_IP
        network list floating [ip] [--cloud=CLOUD] [--instance=INS_ID_OR_NAME] [IP_OR_ID]
        network list floating pool [--cloud=CLOUD]
        network -h | --help

    Options:
        -h                          help message
        --cloud=CLOUD               Name of the IaaS cloud e.g. india_openstack_grizzly.
        --server=SERVER             Server Name
        --pool=FLOATING_IP_POOL     Name of Floating IP Pool
        --instance=INS_ID_OR_NAME   ID of the vm instance

    Arguments:
        IP_OR_ID        IP Address or ID
        FIXED_IP        Fixed IP Address, e.g. 10.1.5.2
        FLOATING_IP     Floating IP Address, e.g. 192.1.66.8
        FLOATING_IP_ID  ID associated with Floating IP, e.g. 185c5195-e824-4e7b-8581-703abec4bc01

    Examples:
        $ network get fixed ip --cloud=india 10.1.2.5
        $ network get fixed --cloud=india 10.1.2.5
        $ network get floating ip --cloud=india 185c5195-e824-4e7b-8581-703abec4bc01
        $ network get floating --cloud=india 185c5195-e824-4e7b-8581-703abec4bc01
        $ network reserve fixed ip --cloud=india 10.1.2.5
        $ network reserve fixed --cloud=india 10.1.2.5
        $ network unreserve fixed ip --cloud=india 10.1.2.5
        $ network unreserve fixed --cloud=india 10.1.2.5
        $ network associate floating ip --cloud=india --server=albert-001 192.1.66.8
        $ network associate floating --cloud=india --server=albert-001 192.1.66.8
        $ network disassociate floating ip --cloud=india --server=albert-001 192.1.66.8
        $ network disassociate floating --cloud=india --server=albert-001 192.1.66.8
        $ network create floating ip --cloud=india --pool=albert-f01
        $ network create floating --cloud=india --pool=albert-f01
        $ network delete floating ip --cloud=india 192.1.66.8
        $ network delete floating --cloud=india 192.1.66.8
        $ network list floating ip --cloud=india
        $ network list floating --cloud=india
        $ network list floating --cloud=india 192.1.66.8
        $ network list floating --cloud=india --instance=323c5195-7yy34-4e7b-8581-703abec4b
        $ network list floating pool --cloud=india



nova
----------------------------------------------------------------------

Command - nova::

    Usage:
        nova set CLOUD
        nova info [CLOUD] [--password]
        nova help
        nova [--group=GROUP] ARGUMENTS...

    A simple wrapper for the openstack nova command

    Arguments:
        GROUP           The group to add vms to
        ARGUMENTS       The arguments passed to nova
        help            Prints the nova manual
        set             reads the information from the current cloud
                        and updates the environment variables if
                        the cloud is an openstack cloud
        info            the environment values for OS

    Options:
        --group=GROUP   Add VM to GROUP group
        --password      Prints the password
        -v              verbose mode



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

    Description:
        Action to be performed whne quit is typed


quit
----------------------------------------------------------------------

Command - quit::

    Usage:
        quit

    Description:
        Action to be performed whne quit is typed


quota
----------------------------------------------------------------------

Command - quota::

    Usage:
        quota list [--cloud=CLOUD] [--tenant=TENANT] [--format=FORMAT]

        Prints quota limit on a current project/tenant

    Options:
       --format=FORMAT  the output format [default: table]
       --cloud=CLOUD    the cloud name
       --tenant=TENANT  the tenant id

    Examples:
        cm quota list
        cm quota list --cloud=india --format=csv



register
----------------------------------------------------------------------

Command - register::

    Usage:
        register info
        register new
        register clean [--force]
        register list ssh [--format=FORMAT]
        register list [--yaml=FILENAMh bE][--info][--format=FORMAT]
        register cat [--yaml=FILENAME]
        register edit [--yaml=FILENAME]
        register export HOST [--password] [--format=FORMAT]
        register source HOST
        register merge FILEPATH
        register form [--yaml=FILENAME]
        register check [--yaml=FILENAME]
        register test [--yaml=FILENAME]
        register json HOST
        register remote CLOUD [--force]
        register india [--force]
        register CLOUD CERT [--force]
        register CLOUD --dir=DIR
        register env [--provider=PROVIDER]

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
      FILEPATH the path of the file
      CLOUD the cloud name
      CERT the path of the certificate
      PROVIDER the provider or type of cloud [Default: openstack]

    Options:

      --provider=PROVIDER     Provider to be used for cloud. Values are:
                              openstack, azure, ec2.
      --version=VERSION       Version of the openstack cloud.
      --openrc=OPENRC         The location of the openrc file
      --password              Prints the password
      --force                 ignore interactive questions and execute
                              the action

    Description:

        register info
            It looks out for the cloudmesh.yaml file in the current
            directory, and then in ~/.cloudmesh

        register list [--yaml=FILENAME] [--name] [--info]
            lists the clouds specified in the cloudmesh.yaml file. If
            info is specified it also prints the location of the yaml
            file.

        register list ssh
            lists hosts from ~/.ssh/config

        register cat [--yaml=FILENAME]
            outputs the cloudmesh.yaml file

        register edit [--yaml=FILENAME]
            edits the cloudmesh.yaml file

        register export HOST [--format=FORMAT]

              prints the contents of an openrc.sh file based on the
              information found in the cloudmesh.yaml file.

        register remote CLOUD [--force]

              reads the Openstack OPENRC file from a remote host that
              is described in cloudmesh.yaml file. We assume that
              the file has already a template for this host. If
              not it can be created from other examples before
              you run this command.

              It uses the OS_OPENRC variable to locate the file and
              copy it onto your computer.

        register merge FILENAME
            Replaces the TBD in cloudmesh.yaml with the contents
            present in the named file

        register form [--yaml=FILENAME]
            interactively fills out the form wherever we find TBD.

        register check [--yaml=FILENAME]
            checks the yaml file for completness

        register test [--yaml=FILENAME]
            checks the yaml file and executes tests to check if
            we can use the cloud. TODO: maybe this should be in
            a test command

        register json host
            displays the host details in json format

        register remote CLOUD
            registers a remote cloud and copies the openrc file
            specified in the credentials of the cloudmesh.yaml

        register CLOUD CERT [--force]
            Copies the CERT to the ~/.cloudmesh/clouds/host directory
            and registers that cert in the coudmesh.yaml file.
            For india, CERT will be in
            india:.cloudmesh/clouds/india/juno/cacert.pem
            and would be copied to ~/.cloudmesh/clouds/india/juno

        register CLOUD --dir
            Copies the entire directory from the cloud and puts it in
            ~/.cloudmesh/clouds/host
            For india, The directory would be copied to
            ~/.cloudmesh/clouds/india

        register env [--provider=PROVIDER] [HOSTNAME]
            Reads env OS_* variables and registers a new cloud in yaml,
            interactively. Default PROVIDER is openstack and HOSTNAME
            is localhost.


reservation
----------------------------------------------------------------------

Command - reservation::

    Usage:
        reservation info --user=USER --project=PROJECT
        reservation list [--name=NAME]
                         [--user=USER]
                         [--project=PROJECT]
                         [--hosts=HOSTS]
                         [--start=TIME_START]
                         [--end=TIME_END]
                         [--format=FORMAT]
        reservation delete [all]
                           [--user=USER]
                           [--project=PROJECT]
                           [--name=NAME]
                           [--start=TIME_START]
                           [--end=TIME_END]
                           [--hosts=HOSTS]
        reservation delete --file=FILE
        reservation update --name=NAME
                          [--start=TIME_START]
                          [--end=TIME_END]
                          [--user=USER]
                          [--project=PROJECT]
                          [--hosts=HOSTS]
                          [--description=DESCRIPTION]
        reservation add --name=NAME
                        [--start=TIME_START]
                        [--end=TIME_END]
                        [--user=USER]
                        [--project=PROJECT]
                        [--hosts=HOSTS]
                        [--description=DESCRIPTION]
        reservation add --file=FILE

    Arguments:

        NAME            Name of the reservation
        USER            Registration will be done for this user
        PROJECT         Project to be used
        HOSTS           Hosts to reserve
        TIME_START      Start time of reservation
        TIME_END        End time of reservation
        FORMAT          Format of output
        DESCRIPTION     Description for reservation
        FILE            File that contains reservation data to be added/ deleted

    Options:

        --name=NAME           Names of the reservation
        --user=USER           user name
        --project=PROJECT     project id
        --start=TIME_START    Start time of the reservation, in
                              MM/DD/YYYY at hh:mm aa format. (default value: 01/01/1901 at 12:00 am])
        --end=TIME_END        End time of the reservation, in
                              MM/DD/YYYY at hh:mm aa format. (default value: 12/31/2100 at 11:59 pm])
        --host=HOSTS          host name
        --description=DESCRIPTION  description summary of the reservation
        --file=FILE           Adding multiple reservations from one file
        --format=FORMAT       Format is either table, json, yaml or csv
                              [default: table]

    Description:

        reservation info
            lists the resources that support reservation for
            a given user or project.


reset
----------------------------------------------------------------------

Command - reset::

      Usage:
          reset

    Description:

        DANGER: This method erases the database.


    Examples:
        clean



secgroup
----------------------------------------------------------------------

Command - secgroup::

    Usage:
        secgroup list [--cloud=CLOUD] [--tenant=TENANT]
        secgroup create [--cloud=CLOUD] [--tenant=TENANT] LABEL
        secgroup delete [--cloud=CLOUD] [--tenant=TENANT] LABEL
        secgroup rules-list [--cloud=CLOUD] [--tenant=TENANT] LABEL
        secgroup rules-add [--cloud=CLOUD] [--tenant=TENANT] LABEL FROMPORT TOPORT PROTOCOL CIDR
        secgroup rules-delete [--cloud=CLOUD] [--tenant=TENANT] LABEL FROMPORT TOPORT PROTOCOL CIDR
        secgroup -h | --help
        secgroup --version

    Options:
        -h                  help message
        --cloud=CLOUD       Name of the IaaS cloud e.g. india_openstack_grizzly.
        --tenant=TENANT     Name of the tenant, e.g. fg82.

    Arguments:
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
        $ secgroup list --cloud india --tenant fg82
        $ secgroup rules-list --cloud india --tenant fg82 default
        $ secgroup create --cloud india --tenant fg82 webservice
        $ secgroup rules-add --cloud india --tenant fg82 webservice 8080 8088 TCP "129.79.0.0/16"



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



server
----------------------------------------------------------------------

Command - server::

    Usage:
        server

    Options:
      -h --help
      -v       verbose mode

    Description:
      Starts up a REST service and a WEB GUI so one can browse the data in an
      existing cloudmesh database.

      The location of the database is supposed to be in

        ~/.cloud,esh/cloudmesh.db



ssh
----------------------------------------------------------------------

Command - ssh::

    Usage:
        ssh table
        ssh list [--format=FORMAT]
        ssh cat
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

    Description:

        ssh list
            lists the hostsnames  that are present in the
            ~/.ssh/config file

        ssh cat
            prints the ~/.ssh/config file

        ssh table
            prints contents of the ~/.ssh/config file in table format

        ssh register NAME PARAMETERS
            registers a host i ~/.ssh/config file
            Parameters are attribute=value pairs
            Note: Note yet implemented

        ssh ARGUMENTS
            executes the ssh command with the given arguments
            Example:
                ssh myhost

                    conducts an ssh login to myhost if it is defined in
                    ~/.ssh/config file


submit
----------------------------------------------------------------------

Command - submit::

    Command documentation submit missing, help_submit

usage
----------------------------------------------------------------------

Command - usage::

    Usage:
        usage list [--cloud=CLOUD] [--start=START] [--end=END] [--tenant=TENANT] [--format=FORMAT]

        Show usage data.

    Options:
       --format=FORMAT  the output format [default: table]
       --cloud=CLOUD    the cloud name
       --tenant=TENANT  the tenant name
       --start=START    Usage range start date ex 2012-01-20, default is: 4 weeks ago
       --end=END        Usage range end date, ex 2012-01-20, default is: tomorrow


    Examples:
        cm usage list



version
----------------------------------------------------------------------

Command - version::

    Usage:
       version [--format=FORMAT] [--check=CHECK]

    Options:
        --format=FORMAT  the format to print the versions in [default: table]
        --check=CHECK    boolean tp conduct an additional check [default: True]

    Description:
        Prints out the version number


vm
----------------------------------------------------------------------

Command - vm::

    Usage:
        vm default [--cloud=CLOUD][--format=FORMAT]
        vm refresh [--cloud=CLOUD]
        vm boot [--name=NAME]
                [--cloud=CLOUD]
                [--image=IMAGE_OR_ID]
                [--flavor=FLAVOR_OR_ID]
                [--group=GROUP]
                [--secgroup=SECGROUP]
                [--keypair_name=KEYPAIR_NAME]
        vm start NAME...
                 [--group=GROUP]
                 [--cloud=CLOUD]
                 [--force]
        vm stop NAME...
                [--group=GROUP]
                [--cloud=CLOUD]
                [--force]
        vm delete NAME...
                  [--group=GROUP]
                  [--cloud=CLOUD]
                  [--force]
        vm floating_ip_assign NAME...
                              [--cloud=CLOUD]
        vm ip_show NAME...
                   [--group=GROUP]
                   [--cloud=CLOUD]
                   [--format=FORMAT]
                   [--refresh]
        vm login NAME [--user=USER]
                 [--ip=IP]
                 [--cloud=CLOUD]
                 [--key=KEY]
                 [--command=COMMAND]
        vm list [NAME_OR_ID]
                [--cloud=CLOUD|--all]
                [--group=GROUP]
                [--format=FORMAT]
        vm status [--cloud=CLOUD]

    Arguments:
        COMMAND        positional arguments, the commands you want to
                       execute on the server(e.g. ls -a) separated by ';',
                       you will get a return of executing result instead of login to
                       the server, note that type in -- is suggested before
                       you input the commands
        NAME           server name
        NAME_OR_ID     server name or ID
        KEYPAIR_NAME   Name of the openstack keypair to be used to create VM. Note this is not a path to key.

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
        --secgroup=SECGROUP    security group name for the server
        --image=IMAGE_OR_ID    give the name or id of the image
        --key=KEY        specify a key to use, input a string which
                         is the full path to the private key file
        --keypair_name=KEYPAIR_NAME   Name of the openstack keypair to be used to create VM.
                                      Note this is not a path to key.
        --user=USER      give the user name of the server that you want
                         to use to login
        --name=NAME      give the name of the virtual machine
        --force          delete vms without user's confirmation
        --command=COMMAND
                         specify the commands to be executed



    Description:
        commands used to boot, start or delete servers of a cloud

        vm default [options...]     Displays default parameters that are set for VM boot.
        vm boot [options...]        Boots servers on a cloud, user may specify
                                    flavor, image .etc, otherwise default values
                                    will be used, see how to set default values
                                    of a cloud: cloud help
        vm start [options...]       Starts a suspended or stopped vm instance.
        vm stop [options...]        Stops a vm instance .
        vm delete [options...]      delete servers of a cloud, user may delete
                                    a server by its name or id, delete servers
                                    of a group or servers of a cloud, give prefix
                                    and/or range to find servers by their names.
                                    Or user may specify more options to narrow
                                    the search
        vm floating_ip_assign [options...]   assign a public ip to a VM of a cloud
        vm ip_show [options...]     show the ips of VMs
        vm login [options...]       login to a server or execute commands on it
        vm list [options...]        same as command "list vm", please refer to it
        vm status [options...]      Retrieves status of last VM booted on cloud and displays it.

    Tip:
        give the VM name, but in a hostlist style, which is very
        convenient when you need a range of VMs e.g. sample[1-3]
        => ['sample1', 'sample2', 'sample3']
        sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']


