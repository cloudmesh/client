Existing original cloudmesh commands
=====================================

Notes:

* --format should become --output? reasoning in api format is keyword. in case we keep format we want to do output_format as api variable.

currently we have

* list flavors and flavor list, ... maybe not needed and if the one should call just the other
* --refresh in list seems useful

* we need a refresh command that just refreshes and does not list
* we need to urgently work on defaults for list columns
  
* we need to work on vm/boot command.


Refresh
-------


::

   Refreshes the database with information from the clouds


   Usage:
       refresh
       refresh CLOUD
       refresh status

   Description:

       refresh
           refreshes the information 
       
       refresh CLOUD
           refreshes the information form the specific cloud
   
       refresh status
           as the refresh may be done asynchronously, the stats will show you the progress of the ongoing refresh
	   NOT IMPLEMENTED
	   It also shows when the last refresh on a specific cloud object took place.
	   
       refresh list
           lists all the Clouds that need a refresh

       Refreshes are activated on all cloudsthat are "active". A cloud can be activated with the cloud command

          cloud activate CLOUD
	
   
List
----

::

      List available flavors, images, vms, projects and clouds


      
      Usage:
          list flavor [CLOUD...] 
                      [--refresh]
		      [--format=FORMAT]
                      [--columns=COLUMNS]
                      [--detail]
          list image [CLOUD...] 
                     [--refresh] 
                     [--format=FORMAT] 
                     [--columns=COLUMNS]
                     [--detail]
          list vm [CLOUD...] 
                  [--group=<group>]
                  [--refresh] 
                  [--format=FORMAT] 
                  [--columns=COLUMNS] 
                  [--detail]
          list default [CLOUD...] 
                  [--format=FORMAT] 
                  [--columns=COLUMNS] 
                  [--detail]
          list cloud 
                  [--format=FORMAT] 
                  [--columns=COLUMNS] 
                  [--detail]

      Arguments:

          CLOUD...    the name of the clouds e.g. india

      Options:

          --all                  list information of all active clouds
          --refresh              refresh data before list
          --group=<group>        give the group name in list vm
          --detail               for table print format, a brief version 
                                 is used as default, use this flag to print
                                 detailed table
          --columns=COLUMNS      specify what information to display in
                                 the columns of the list command. For
                                 example, --column=active,label prints
                                 the columns active and label. Available
                                 columns are active, label, host,
                                 type/version, type, heading, user,
                                 credentials, defaults (all to display
                                 all, email to display all except
                                 credentials and defaults)
          --format=FORMAT        output format: table, json, csv [default: table]

      Description:

          List clouds and projects information, if the CLOUD argument is not specified, the
          selected default cloud will be used. You can interactively set the default cloud with the command
          'cloud select'.

          list flavor
          : list the flavors
          list image
          : list the images
          list vm
          : list the vms
          list project
          : list the projects
          list cloud
          : same as cloud list

	  If no cloud is specified it lists the information for all clouds.

	  
      See Also:

          man cloud


Security group
----------------------------

::

      Usage:
          security_group list CLOUD...
          security_group add CLOUD LABEL PARAMETERS
          security_group delete CLOUD LABEL
      security_group -h | --help
          security_group --version

      Options:
         -h                   help message
          LABEL        the label
	  PARAMETERS   TBD
	 
      Arguments:
          CLOUD    Name of the IaaS cloud e.g. india_openstack_grizzly.

	  
      Description:
         security_group command provides list of available security_groups.

      Result:

      Examples:
          $ security_group list india_openstack_grizzly

      TODO: much better examples
      
Cloud (do)
-------------

::

        Usage:
            cloud refresh
            cloud list [CLOUD...] [--refresh] [--columns=COLUMNS] [--format=FORMAT] [--details]	    
            cloud alias NAME [CLOUD]
            cloud on [CLOUD...]
            cloud off [CLOUD...]
            cloud TODO add YAMLFILE [--force] REMOVE_REPLACED_BY_REGISTER
            cloud TODO remove [CLOUD|--all]   MOVE_TO_REGISTER 
	    cloud default
	    cloud default CLOUD
            cloud set flavor [CLOUD] [--name=NAME|--id=ID]
            cloud set image [CLOUD] [--name=NAME|--id=ID]

	TODO: aad the selector
	
        Arguments:

          CLOUD                  the name of a cloud
          YAMLFILE               a yaml file (with full file path) containing
                                 cloud information
          NAME                   name for a cloud (or flavor and image)

        Options:

           --columns=COLUMNS       specify what information to display in
                                 the columns of the list command. For
                                 example, --column=active,label prints the
                                 columns active and label. Available
                                 columns are active, label, host,
                                 type/version, type, heading, user,
                                 credentials, defaults (all to display all,
                                 semiall to display all except credentials
                                 and defaults)
                                 
           --format=FORMAT       output format: table, json, csv

           --all                 display all available columns

           --force               if same cloud exists in database, it will be
                                 overwritten

           --name=NAME           provide flavor or image name

           --id=ID               provide flavor or image id


        Description:

            TODO fix the description
	    
            The cloud command allows easy management of clouds in the
            command shell. The following subcommands exist:

            cloud [list] [--column=COLUMN] [--json|--table]
                lists the stored clouds, optionally, specify columns for more
                cloud information. For example, --column=active,label

            cloud info [CLOUD|--all] [--json|--table]
                provides the available information about the cloud in dict
                format
                options: specify CLOUD to display it, --all to display all,
                         otherwise selected cloud will be used

            cloud alias NAME [CLOUD]
                sets a new name for a cloud
                options: CLOUD is the original label of the cloud, if
                         it is not specified the default cloud is used.


            cloud select [CLOUD]
                selects a cloud to work with from a list of clouds.If the cloud 
                is not specified, it asks for the cloud interactively

            cloud on [CLOUD]
            cloud off [CLOUD]
                activates or deactivates a cloud. if CLOUD is not
                given, the default cloud will be used.


            cloud add <cloudYAMLfile> [--force]
                adds the cloud information to database that is
                specified in the <cloudYAMLfile>. This file is a yaml. You
                need to specify the full path. Inside the yaml, a
                cloud is specified as follows:

                cloudmesh:
                   clouds:
                     cloud1: ...
                     cloud2: ...

                For examples on how to specify the clouds, please see
                cloudmesh.yaml

                options: --force. By default, existing cloud in
                         database cannot be overwirtten, the --force
                         allows overwriting the database values.

            cloud remove [CLOUD|--all]
                remove a cloud from the database, The default cloud is
                used if CLOUD is not specified.
                This command should be used with caution. It is also
                possible to remove all clouds with the option --all

            cloud default [CLOUD|--all]

                show default settings of a cloud, --all to show all clouds

            cloud set flavor [CLOUD] [--name=NAME|--id=ID]

                sets the default flavor for a cloud. If the cloud is
                not specified, it used the default cloud.

            cloud set image [CLOUD] [--name=NAME|--id=ID]

                sets the default flavor for a cloud. If the cloud is
                not specified, it used the default cloud.

VM (do)
---------

::

            Usage:
                vm start [--name=NAME]
                         [--count=COUNT]
                         [--cloud=CLOUD]
                         [--image=IMAGE_OR_ID]
                         [--flavor=FLAVOR_OR_ID]
                         [--group=<group>]
                vm delete [NAME_OR_ID...]
                          [--group=GROUP]
                          [--cloud=CLOUD]
                          [--force]
                vm ip assign [NAME_OR_ID...]
                             [--cloud=CLOUD]
                vm ip show [NAME_OR_ID...]
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--format=FORMAT]
                           [--refresh]
                vm login NAME [--user=USER]
		         [--ip=IP]
                         [--cloud=CLOUD]
                         [--key=KEY]
                         [--] [COMMAND...]
                vm list [CLOUD|--all] 
                        [--group=GROUP]
                        [--refresh] 
                        [--format=FORMAT] 
                        [--columns=COLUMNS] 
                        [--detail]

            Arguments:
                COMMAND                positional arguments, the commands you want to
                                       execute on the server(e.g. ls -a), you will get
                                       a return of executing result instead of login to
                                       the server, note that type in -- is suggested before
                                       you input the commands
                NAME                   server name

            Options:
                --ip=IP                give the public ip of the server
                --cloud=CLOUD    give a cloud to work on, if not given, selected
                                       or default cloud will be used
                --count=COUNT        give the number of servers to start
                --detail               for table print format, a brief version 
                                       is used as default, use this flag to print
                                       detailed table
                --flavor=FLAVOR_OR_ID  give the name or id of the flavor
                --group=GROUP          give the group name of server
                --image=IMAGE_OR_ID    give the name or id of the image
                --key=KEY              spicfy a key to use, input a string which
                                       is the full path to the public key file
                --user=USER            give the user name of the server that you want
                                       to use to login
                --name=NAME            give the name of the virtual machine
                --force                delete vms without user's confirmation



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
                vm ip assign [options...]   assign a public ip to a VM of a cloud
                vm ip show [options...]     show the ips of VMs
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


Volume (do)
------------

::

          Usage:
              volume list
              volume create <size>
                            [--snapshot-id=<snapshot-id>]
                            [--image-id=<image-id>]
                            [--display-name=<display-name>]
                            [--display-description=<display-description>]
                            [--volume-type=<volume-type>]
                            [--availability-zone=<availability-zone>]
              volume delete <volume>
              volume attach <server> <volume> <device>
              volume detach <server> <volume>
              volume show <volume>
              volume snapshot-list
              volume snapshot-create <volume-id>
                                     [--force]
                                     [--display-name=<display-name>]
                                     [--display-description=<display-description>]
              volume snapshot-delete <snapshot>
              volume snapshot-show <snapshot>
              volume help


          volume management

          Arguments:
              <size>            Size of volume in GB
              <volume>          Name or ID of the volume to delete
              <volume-id>       ID of the volume to snapshot
              <server>          Name or ID of server(VM).
              <device>          Name of the device e.g. /dev/vdb. Use "auto" for 
                                autoassign (if supported)
              <snapshot>        Name or ID of the snapshot

          Options:
              --snapshot-id <snapshot-id>
                                      Optional snapshot id to create the volume from.
                                      (Default=None)
              --image-id <image-id>
                                      Optional image id to create the volume from.
                                      (Default=None)
              --display-name <display-name>
                                      Optional volume name. (Default=None)
              --display-description <display-description>
                                      Optional volume description. (Default=None)
              --volume-type <volume-type>
                                      Optional volume type. (Default=None)
              --availability-zone <availability-zone>
                                      Optional Availability Zone for volume. (Default=None)
              --force                 Optional flag to indicate whether to snapshot a volume
                                      even if its attached to an instance. (Default=False)

          Description:
              volume list
                  List all the volumes
              volume create <size> [options...]
                  Add a new volume
              volume delete <volume>
                  Remove a volume   
              volume attach <server> <volume> <device>
                  Attach a volume to a server    
              volume-detach <server> <volume>
                  Detach a volume from a server
              volume show <volume>        
                  Show details about a volume
              volume snapshot-list
                  List all the snapshots
              volume snapshot-create <volume-id> [options...]
                  Add a new snapshot
              volume snapshot-delete <snapshot>
                  Remove a snapshot
              volume-snapshot-show <snapshot>
                  Show details about a snapshot
              volume help 
                  Prints the nova manual


Status (do)
-------------

::

          Usage:
              status
	      status db
	      status CLOUD...
	  
          Shows system status

	  Description:
              status
	          shows the status of al relevant subystems
		  
	      status db
	          shows the status of the db
		  
	      status CLOUD...
	          shows the status of the clouds specified        

		  
Stack (do)
-----

::

          Usage:
              stack start NAME [--template=TEMPLATE] [--param=PARAM]
              stack stop NAME
              stack show NAME
              stack list [--refresh] [--column=COLUMN] [--format=FORMAT]
              stack help | -h

          An orchestration tool (OpenStack Heat)

          Arguments:

            NAME           stack name
            help           Prints this message

          Options:

             -v       verbose mode


Launcher (do)
--------------

::

          Usage:
                launcher start MENU
                launcher stop STACK_NAME
                launcher list
                launcher show STACK_NAME
                launcher menu [--column=COLUMN] [--format=FORMAT]
                launcher import [FILEPATH] [--force]
                launcher export FILEPATH
                launcher help | -h

            An orchestration tool with Chef Cookbooks

            Arguments:

              MENU           Name of a cookbook
              STACK_NAME     Name of a launcher
              FILEPATH       Filepath
              COLUMN         column name to display
              FORMAT         display format (json, table)
              help           Prints this message

            Options:

               -v       verbose mode

Key (do)
---------

::

         Usage:
                   key -h|--help
                   key list [--source=SOURCE] [--dir=DIR] [--format=FORMAT]
                   key add [--keyname=KEYNAME] FILENAME
                   key default [KEYNAME]
                   key delete KEYNAME

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
               --source=SOURCE      the source for the keys [default: mongo]
               --keyname=KEYNAME    the name of the keys

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


Inventory (not)
----------------

::
   
          Usage:
                 inventory clean
                 inventory create image DESCRIPTION
                 inventory create server [dynamic] DESCRIPTION
                 inventory create service [dynamic] DESCRIPTION
                 inventory exists server NAME
                 inventory exists service NAME
                 inventory
                 inventory print
                 inventory info [--cluster=CLUSTER] [--server=SERVER]
                 inventory list [--cluster=CLUSTER] [--server=SERVER]
                 inventory server NAME
                 inventory service NAME

          Manages the inventory

              clean       cleans the inventory
              server      define servers

          Arguments:

            DESCRIPTION    The hostlist"i[009-011],i[001-002]"

            NAME           The name of a service or server


          Options:

             v       verbose mode


Experiment (do)
----------------

::
        
          Usage:
                 exp NOTIMPLEMENTED clean
                 exp NOTIMPLEMENTED delete NAME
                 exp NOTIMPLEMENTED create [NAME]
                 exp NOTIMPLEMENTED info [NAME]
                 exp NOTIMPLEMENTED cloud NAME
                 exp NOTIMPLEMENTED image NAME
                 exp NOTIMPLEMENTED flavour NAME
                 exp NOTIMPLEMENTED index NAME
                 exp NOTIMPLEMENTED count N

          Manages the vm

          Arguments:

            NAME           The name of a service or server
            N              The number of VMs to be started


          Options:

             -v       verbose mode

debug (not cmd3)
------------------

::
       
        Usage:
              debug on
              debug off

              Turns the debug log level on and off.

color (not cmd3)
-----------------

::
        
          Usage:
              color on
              color off
              color

              Turns the shell color printing on or off

          Description:

              color on   switched the color on

              color off  switches the color off

              color      without parameters prints a test to display
                         the various colored mesages. It is intended
                         as a test to see if your terminal supports
                         colors.

Cluster (do)
--------------

::
       
          Usage:
              cluster list [--format=FORMAT]
              cluster create <name>
                             [--count=<count>]
                             [--ln=<LoginName>]
                             [--cloud=<CloudName>]
                             [--image=<imgName>|--imageid=<imgId>]
                             [--flavor=<flavorName>|--flavorid=<flavorId>]
                             [--force]
              cluster show <name> 
                           [--format=FORMAT] 
                           [--column=COLUMN]
                           [--detail]
              cluster remove <name> 
                             [--grouponly]

          Description:
              Cluster Management
              
              cluster list
                  list the clusters

              cluster create <name> --count=<count> --ln=<LoginName> [options...]
                  Start a cluster of VMs, and each of them can log into all others.
                  CAUTION: you should do some default setting before using
                  this command:
                  1. select cloud to work on, e.g. cloud select india
                  2. activate the cloud, e.g. cloud on india
                  3. set the default key to start VMs, e.g. key default [NAME]
                  4. set the start name of VMs, which is prefix and index, e.g. label --prefix=test --id=1
                  5. set image of VMs, e.g. default image
                  6. set flavor of VMs, e.g. default flavor
                  Also, it is better to choose a unused group name
              
              cluster show <name>
                  show the detailed information about the cluster VMs

              cluster remove <name> [--grouponly]
                  remove the cluster and its VMs, if you want to remove the cluster(group name)
                  without removing the VMs, use --grouponly flag
          
          Arguments:
              <name>        cluster name or group name

          Options:
              --count=<count>            give the number of VMs to add into the cluster
              --ln=<LoginName>           give a login name for the VMs, e.g. ubuntu
              --cloud=<CloudName>        give a cloud to work on
              --flavor=<flavorName>      give the name of the flavor
              --flavorid=<flavorId>      give the id of the flavor
              --image=<imgName>          give the name of the image
              --imageid=<imgId>          give the id of the image
              --force                    if a group exists and there are VMs in it, the program will
                                         ask user to proceed or not, use this flag to respond yes as 
                                         default(if there are VMs in the group before creating this 
                                         cluster, the program will include the exist VMs into the cluster)
              --grouponly                remove the group only without removing the VMs, otherwise 
                                         cluster remove command will remove all the VMs of this cluster
              FORMAT                     output format: table, json, csv
              COLUMN                     customize what information to display, for example:
                                         --column=status,addresses prints the columns status
                                         and addresses
              --detail                   for table print format, a brief version 
                                         is used as default, use this flag to print
                                         detailed table


Admin (do)
--------------

::
        
        Usage:
          admin password reset
          admin server start
          admin server stop
          admin server status
          admin mongo start
          admin mongo stop
          admin mongo reset
          admin mongo status
          admin mongo password
          admin celery start
          admin celery stop
          admin celery status
          admin rabbitmq status
          admin rabbitmq start
          admin rabbitmq stop
          admin version

        Options:


        Description:
            admin password reset
               reset portal password
