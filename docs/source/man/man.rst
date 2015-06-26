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

default
----------------------------------------------------------------------

Command - default::

    Usage:
        default list [--output=FORMAT]
        default delete KEY [--cloud=CLOUD]
        default KEY [--cloud=CLOUD]
        default KEY=VALUE [--cloud=CLOUD]


    managing the defaults test test test test

    Arguments:

      KEY    the name of the default
      VALUE  the value to set the key to

    Options:

       --cloud=CLOUD    the name of the cloud [default: general]
       --output=FORMAT  the output format [default: table]



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

    THIS COMMAND IS NOT IMPLEMENTED


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
        register [--yaml=FILENAME]
        register india
        register CLOUD CERT
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

              reads the Openstack OPENRC file from a host that is described in ./ssh/config and adds it to the
              configuration cloudmehs.yaml file. We assume that the file has already a template for this
              host. If nt it can be created from other examples before you run this command.

              The hostname can be specified as follows in the ./ssh/config file.

              Host india
                  Hostname india.futuresystems.org
                  User yourusername

              If the host is india and the OPENRC file is ommitted, it will automatically fill out the location
              for the openrc file. To obtain the information from india simply type in

                  register rc india

        register [--yaml=FILENAME]
            read the yaml file instead of ./cloudmesh.yaml or ~/.cloudmesh/cloudmesh.yaml which is used when the
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

      NAME            Name of the table to search. If the name is not specified, the table DEFAULT will be searched
      --order=FORMAT  Columns that will be displayed
      FILTER          Filter to be used when searching

    Options:

       -v       verbose mode



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

