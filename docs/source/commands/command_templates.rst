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
command:

.. prompt:: bash

    default format FORMAT

Once you have set it, the default format will be used for all commands
the do not explicitly set the format option on the commandline.

To switch off this behavior and use the build in behavior for each
command, we specify:

.. prompt:: bash

     default format False



Cloud
----------------------------------------------------------------------

Many commands are specific to a particular cloud. this cloud can be
set with the::

    --cloud CLOUD

option for individual commands that support it. As we deal with many
clouds it may be inconvenient to specify the name of the cloud every
time, thus we have introduced the concept of a default cloud. The
default cloud can be set with the command:

.. prompt:: bash

    default cloud CLOUDNAME

where cloudname is the name of the cloud that we have registered with
cloudmesh (see registration).

.. todo:: put link to registration here

History
----------------------------------------------------------------------

The manual page of the history command can be found at:
`register <../man/man.html#history>`_

Not yet completed. As we may want to run multiple commands we also
provide a history that can be invoked from cloudmesh to show which
cloudmesh commands have been issued in the past. This allows a more
easy review of past activities:

.. prompt:: bash

     cm history

Commands in history are preceeded by a number. A past command can be
reissued by appending the number to the history. Thus the command:

.. prompt:: bash

     cm history 3

would execute the 3rd command in the command history. Instead of
using the command history, you can also use the abbreviation `h`.

Help
----------------------------------------------------------------------

To see the list of all available commands use the command:

.. prompt:: bash

   cm help

The commands are sorted by topic, while the first list gives all
commands in alphabetical order. To opbtain an individual man page
simply say:

.. prompt:: bash

       cm help COMMAND

where command is the command you which to get the help message for. To
optain the manual pages of all commands yo can use the command:

.. prompt:: bash

   cm man

which will print all man pages out.


Shell & Commandline
----------------------------------------------------------------------

Cloudmesh client is a shell as well as a commandline tool. Thus all
commands that you can type in as a single command could also be
executed as a command shell. To enter the command shell, please type:

.. prompt:: bash

     cm

::

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

The current list of commands contains:

.. prompt:: bash

    cm help

::

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


Elementary Commands
-------------------

We have build in some convenience commands into the shell that include comments and execution of cm scripts.

Comments
^^^^^^^^^

Comments are identified by the first characters in a command line. We allow the following comment charater identification
strings::

   #
   /*
   //

If comments are to be done over multiple lines in a cloudmesh script, they have to be done for each line. If a space or other
 character is in front of a comment string, the it will not be considered as a comment.

Cloudmesh File Execution
^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple cloudmesh commands can be placed in a single file. We recommend that you use the ending `.cm`. You can satrt the
execution of such a file with:

.. prompt:: bash

   cm filename.cm

A cloudmesh file could itself include references to other cloudmesh files. They can be started in one of two ways. You can
use the `exec` command::

   $ cm
   cm> exec filename.cm

or you can use simply the filename. Cloudmesh will check if the filename exists and than execute it::

   $ cm
   cm> filename.cm


Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can execute a python command as follows::

    cm> py COMMAND

where command is the command you like to execute


Quitting the shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To quit the shell you can use either the commands::

  cm> q
  cm> quit
  cm> EOF

Manual Pages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often you will run in the situation where you may have to create a
list of manual pages for your commands for your users. To simplify
that we have not provided this in Unix Man format, but simply in RST
format. You can type in the command::

  cm> man

and it will print you in RST format a list of all commands available
to you for your cmd3 shell. This naturally you could put into a sphinx
documentation to create a nice user manual for your users.


Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloudmesh can easily execute multiple cloudmesh commands that are stored in
cloudmesh script files. TO do so we recommend to place them in a file ending
with `.cm`. Let us assume we call the file test.cm.

Now we can simply execute the script with:

.. prompt:: bash

    cm test.cm

you can also cat the file with:

.. prompt:: bash

    cat test.cm | cm


Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloudmesh client contains the ability to use variables within the shell.
Variables are preserved between calls to cm. To see a list of all variables,
use the command::

  var list

To set variable values you can use::

    cm> var name=value

which will set the variable with the given name to the specified value.
In case the value specifies an entry in the cloudmesh.yaml file it will
be read from it and put into the named variable. For example the command::

    cm> var username=cloudmesh.profile.username

Will create a variable username and get the value form the yaml file
specified by its object hierarchy.

To use the content of the variable, simple use it on the shell with a
dollar sign such as::

  cm> banner $name

In this example a banner will be created that contains the value of the
variable name. Note that the variables `$date` and `$time` are predefined
and give the current date and time and are updated at the time they are called.

As `cm` can also be used in a terminal, many terminal use a $ to indicate
variables for this terminal/shell. In order to mask this you will need to
use the ' ' or the \ sign. Thus, ::

    $ cm banner '$name'
    $ cm banner \$name

will result in the ability to ue the cloudmesh shell variables. If you
However want to use the terminal shell variables such as `$HOME` you can
access them directly::

    $ cm banner $HOME

Special syntax detection of variables allow also easy use of operating
system/terminal variables while prepending them with os. Thus::

    cm> banner $HOME
    cm> banner $os.HOME

Will be the same the advantage is that with os. we clearly mark an os
systems variable that we like to access and no confusion between internal
cloudmesh shell and OS variables occur. Furthermore variables defined in the
cloudmesh yaml file can be directly accessed while using the . notation. Thus::

  cm> banner $cloudmesh.profile.username

Will print a banner with the username being `myusername` as defined in the
yaml hierarchy under given this example::

  cloudmesh:
    profile:
      username: myusername


To show the usage of the different variables in one line, please review the
following example:

.. prompt:: bash

    cm var a=hello
    cm banner '$a-[0-100] $os.HOME $cloudmesh.profile.username'

This will print, where albert is your username::

  ######################################################################
  # hallo-[0-100] /Users/albert albert
  ######################################################################

Timers
-------

Sometimes it is a good idea to measure the time it takes to execute a
particular command. For this reason we have a timer command that can switch
on and off this behaviour.

::

   timer on
   timer off

switches the timer on or off. If the timer is switched on every command will
be followed with the time it takes toe execute that command. Special named
timers can be defined and used.

::

   timer start mytimer

   timer stop mytimer
   timer print mytimer

Intuitive start, stop, and print options can be used. A timer will be reset
with

::

   timer reset mytimer





