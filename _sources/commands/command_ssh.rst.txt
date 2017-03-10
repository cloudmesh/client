Ssh Command
======================================================================

Often the ssh command needs to be used to login to remote machines. As the
interaction with such machines could be frequent via the ssh command, it is
often a good idea to include them into the ~/.ssh/config file. To simplify
interaction, we provide a simple ssh command in cloudmesh.

The manual page of the `ssh` command can be found at: `ssh
<../man/man.html#ssh>`__

Lists
^^^^^^^^^^^^^^

To lists the hostsnames that are present in the `~/.ssh/config` file use
the command

.. prompt:: bash, cm>

  ssh list


To list the contents of the `~/.ssh/config` file use the command

.. prompt:: bash, cm>
	    
  ssh cat

Tos showcase a nice table you can use either of the commands

.. prompt:: bash, cm>
	    
  ssh table
  ssh list --format=table

  

Executing Commands
^^^^^^^^^^^^^^^^^^^

To execute a command on a remote host you simply can use the ssh
command eithe rin the shell or in cloudmesh client. 

.. prompt:: bash, cm>

  ssh ARGUMENTS

::
   
executes the ssh command with the given arguments

Example:

.. prompt:: bash, cm>
	    
	    ssh myhost

conducts an ssh login to myhost if it is defined in ~/.ssh/config file

.. comment:

    Register
    ^^^^^^^^^^^

    .. warning:: Not yet implemented

    .. prompt:: bash, cm>

	ssh register NAME PARAMETERS


    The register command registers a host into the ~/.ssh/config file. Parameters
    are attribute=value pairs Note: Note yet implemented
    
