Basic Commands and Options
======================================================================

Cloudmesh contains a number of commands that makes the management of
multiple heterogeneous clouds easier. The commands are defined in an
uniform fashion and use for many some convenient built in options and
behaviors. We describe them next. As they are general to many commands
we have not described them in detail for each command that utilize
them. You can check with the command manual pages for more details for
each command.


Format
----------------------------------------------------------------------

Many commands have a `--format` parameter that allows to provide output of
the command in various formats. These formats include:

* json
* yaml
* table
* csv

The format can be changed on each command that supports it with::

   --format FORMAT

where FORMAT is one of the values from the list above. In many cases
the default format is set to `table`.

.. comment::

  .. prompt:: bash
  
      default format=FORMAT

  Once you have set it, the default format will be used for all commands
  the do not explicitly set the format option on the commandline.




Cloud
----------------------------------------------------------------------

Many commands are specific to a particular cloud. this cloud can be
set with the

::

    --cloud CLOUD

option for individual commands that support it. As we often execute
multiple commands on the same cloud consecutively, will be
inconvenient to specify the name of the cloud every time, thus we have
introduced the concept of a default cloud. The default cloud can be
set with the command:

.. prompt:: bash, cm>

    default cloud=CLOUDNAME

where `CLOUDNAME` is the name of the cloud that we use 


Help
----------------------------------------------------------------------

To see the list of all available commands use the command:


.. prompt:: bash, cm>
	    
   help

   
The commands are sorted by topic, while the first list gives all
commands in alphabetical order. To obtain an individual man page
simply say:


.. prompt:: bash, cm>
	    
       help COMMAND
   
       
where command is the command you which to get the help message for. To
obtain the manual pages of all commands yo can use the command:

.. prompt:: bash, cm>

   man

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
help COMMANDNAME.  You can quit the command shell with the command
quit.

The current list of commands contains:

.. prompt:: bash

    cm help

::
   
    Documented commands (type help <command>):
    ==========================================
    EOF      comet    h          launcher  pause     reservation  ssh     verbose 
    akey     context  help       limits    portal    reset        submit  version 
    banner   debug    history    list      py        rsync        sync    vm      
    check    default  hpc        load      q         secgroup     test    workflow
    clear    echo     image      man       quit      select       timer 
    cloud    exec     info       network   quota     server       usage 
    cluster  flavor   inventory  nova      refresh   shell        var   
    color    group    key        open      register  sleep        vc    

    Undocumented commands:
    ======================
    shell_exec

    Shell Commands
    ==============
    banner  color  echo  help     load  man   pause  q     refresh  var    
    clear   debug  EOF   history  man   open  puase  quit  timer    version

    System Commands
    ===============
    hpc  rsync  submit  sync

    Comet Commands
    ==============
    comet

    Security Commands
    =================
    key  secgroup  ssh

    Cloud Commands
    ==============
    cloud    flavor  image  limits  network  portal  register  select  test   vm
    default  group   info   list    nova     quota   reset     server  usage


The manual page of the `cm` command can be found at:
`register <../man/man.html#cm>`__    

Elementary Commands
-------------------

We have build in some convenience commands into the shell that include
comments and execution of cm scripts.

Comments
^^^^^^^^^

Comments are identified by the first characters in a command line. We
allow the following comment character identification strings::

   #
   /*
   //

If comments are to be done over multiple lines in a cloudmesh script,
they have to be done for each line at the very beginning. If a space
or other character is in front of a comment string, then it will not
be considered as a comment.

Cloudmesh File Execution
^^^^^^^^^^^^^^^^^^^^^^^^^

Multiple cloudmesh commands can be placed in a single cloudmesh script
file. We recommend that you use the ending `.cm`. You can start the
execution of such a file with:

.. prompt:: bash

   cm filename.cm

A cloudmesh file could itself include references to other cloudmesh
files. They can be started in one of two ways. You can use the `exec`
command::

   $ cm
   cm> exec filename.cm

or you can use simply the filename. Cloudmesh will check if the
filename exists and than execute it::

   $ cm
   cm> filename.cm


Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can execute a python command as follows:

.. prompt:: bash, cm>
	    
    py COMMAND
    
where command is the command you like to execute


Quitting the shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To quit the shell you can use either the commands:


.. prompt:: bash, cm>
	    
  q

.. prompt:: bash, cm>
	       
   quit


.. prompt:: bash, cm>
	       
   EOF

   
	    
Manual Pages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Often you will run in the situation where you may have to create a
list of manual pages for your commands. To simplify that we have not
provided this in Unix Man format, but simply in RST format. You can
type in the command:

.. prompt:: bash, cm>
	    
  man
  
and it will print you in RST format a list of all commands available
to you for your cmd3 shell. This naturally you could put into a sphinx
documentation to create a nice user manual for your users
automatically. IN fact we use this feature to create our manual pages.


The manual page of the `man` command can be found at:
`register <../man/man.html#man>`__

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
use the command:

.. prompt:: bash, cm>
	    
	    var list

To set variable values you can use:

.. prompt:: bash

	    var name=value

which will set the variable with the given name to the specified value.
In case the value specifies an entry in the cloudmesh.yaml file it will
be read from it and put into the named variable. For example the
command:

.. prompt:: bash

	    var username=cloudmesh.profile.user

Will create a variable username and get the value form the yaml file
specified by its object hierarchy.

To use the content of the variable, simple use it on the shell with a
dollar sign such as:

.. prompt:: bash

	    banner $name

In this example a banner will be created that contains the value of the
variable name. Note that the variables `$date` and `$time` are predefined
and give the current date and time and are updated at the time they are called.

As `cm` can also be used in a terminal, many terminal use a $ to indicate
variables for this terminal/shell. In order to mask this you will need to
use the ' ' or the `\` sign:

.. prompt:: bash, cm>

	    banner '$name'

.. prompt:: bash, cm>
		
	    banner \$name

   
	    
will result in the ability to ue the cloudmesh shell variables. If you
However want to use the terminal shell variables such as `$HOME` you can
access them directly:

.. prompt:: bash, cm>
	    
    banner $HOME

    
Special syntax detection of variables allow also easy use of operating
system/terminal variables while prepending them with os. Thus:

.. prompt:: bash, cm>
	    
    banner $HOME

Furthermore variables defined in the
cloudmesh yaml file can be directly accessed while using the . notation. Thus:

.. prompt:: bash, cm>
	      
  banner $cloudmesh.profile.username

  
Will print a banner with the username being `myusername` as defined in the
yaml hierarchy under given this example::

  cloudmesh:
    profile:
      user: myusername


To show the usage of the different variables in one line, please review the
following example:

.. prompt:: bash, cm>

    var a=hello
    banner '$a-[0-100] $HOME $cloudmesh.profile.username'

This will print, where albert is your username::

  ######################################################################
  # hallo-[0-100] /Users/albert albert
  ######################################################################


The manual page of the `var` command can be found at:
`register <../man/man.html#var>`__
  
Timers
-------

Sometimes it is a good idea to measure the time it takes to execute a
particular command. For this reason we have a timer command that can switch
on and off this behavior.

.. prompt:: bash, cm>
	    
   timer on

.. prompt:: bash, cm>
	       
   timer off

   
switches the timer on or off. If the timer is switched on every command will
be followed with the time it takes toe execute that command. Special named
timers can be defined and used.

.. prompt:: bash, cm>
	    
	    timer start mytimer


.. prompt:: bash, cm>
	       
	    timer stop mytimer


.. prompt:: bash, cm>
	       
	    timer print mytimer

   
	       
Intuitive start, stop, and print options can be used. A timer will be reset
with

.. prompt:: bash, cm>
	    
   timer reset mytimer


The manual page of the `timer` command can be found at:
`register <../man/man.html#timer>`__
   
History
^^^^^^^
.. warning:: This command has not yet been implemented and should not
	     be used
	     
The manual page of the `history` command can be found at:
`register <../man/man.html#history>`__

The history command allows the execution of previously run commands.
You can view them with 

.. prompt:: bash, cm>

     history

Commands in history are proceeded by a number. A past command can be
reissued by appending the number to the history. Thus the command:

.. prompt:: bash, cm>

     history 3

would execute the 3rd command in the command history. Instead of
using the command history, you can also use the abbreviation `h`.
   




