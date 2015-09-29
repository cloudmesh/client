Basic Commands and Options
======================================================================

Cloudmesh contains a number of commands that makes the management of
multiple heterogeneous clouds easier. In order to better manage the
various clouds it is convenient to introduce a number of options and
behaviors. This includes the following concepts.

Format
----------------------------------------------------------------------

Many commands have a format parameter that allows to provide output of
the command in various formats. These formats include:

* json
* yaml
* table
* csv

The format can be changed on each command that supports it with::

   --format FORMAT

where FORMAT is one of the values from the list above.

.. todo:: setting a default format via defaults

Not yet done: It is also possible to set the default format for all
commands that accept the format option. THis is done with the
command::

	$ default format FORMAT

Once you have set it, the default format will be used for all commands
the do not explicitly set the format option on the commandline.

To switch off this behavior and use the build in behavior for each
command, we specify::

	 $ default format False

Cloud
----------------------------------------------------------------------

Many commands are specific to a particular cloud. this cloud can be
set with the::

    --cloud CLOUD

option for individual commands that support it. As we deal with many
clouds it may be inconvenient to specify the name of the cloud every
time, thus we have introduced the concept of a default cloud. The
default cloud can be set with the command::

    $ default cloud CLOUDNAME

where cloudname is the name of the cloud that we have registered with
cloudmesh (see registration).

.. todo:: put link to registration here

History
----------------------------------------------------------------------

.. todo:: reintroduce the history command

Not yet completed. As we may want to ruan multiple commands we also
provide a history that can be invoked from cloudmesh to show which
cloudmesh commands have been issued in the past. This allows a more
easy review of past activities::

     $ cm history

Commands in history are preceeded by a number. A past command can be
reissued by appending the number to the history. Thus the command::

	 $cm history 3

would execute the 3rd command in the command history.

Help
----------------------------------------------------------------------

To see the list of all available commands use the command::

   $ cm help

The commands are sorted by topic, while the first list gives all
commands in alphabetical order. To opbtain an individual man page
simply say::

       $ cm help COMMAND

where command is the command you which to get the help message for. To
optain the manual pages of all commands yo can use the command::

   $cm man

which will print all man pages out.

Shell & Commandline
----------------------------------------------------------------------

Cloudmesh client is a shell as well as a commandline tool. Thus all
commands that you can type in as a single command could also be
executed as a command shell. To enter the command shell, please type::

	 $cm

	 +=======================================================+
	 .   ____ _                 _                     _      .
	 .  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   .
	 . | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  .
	 . | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | .
	 .  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| .
	 +=======================================================+
		            Cloudmesh Shell

	 cm> 

You will see the prompt and can interactively execute some of the
commands without needing to type in cm in front of each command.  To
see the commands type help. To get help for an individual command type
help COMMANDNAME.  You can quit the comamnd shell with the command
quit.

The current list of commands contains::

    cm help

    Documented commands (type help <topic>):
    ========================================
    EOF     cloud    group      key     man   pause  quota        secgroup  ssh    
    banner  context  help       limits  nova  q      register     select    version
    clear   default  inventory  list    open  quit   reservation  server    vm     

    Security Commands
    =================
    key  secgroup  ssh

    Shell Commands
    ==============
    banner  clear  EOF  man  man  open  q

    System Commands
    ===============
    inventory  reservation

    Cloud Commands
    ==============
    cloud  default  group  limits  list  nova  quota  register  select  server  vm



