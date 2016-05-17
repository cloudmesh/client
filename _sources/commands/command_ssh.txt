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

.. prompt:: bash, cm>

  ssh list

::
   
      lists the hostsnames  that are present in the
      ~/.ssh/config file

.. prompt:: bash, cm>
	    
  ssh cat

::
   
      prints the ~/.ssh/config file

.. prompt:: bash, cm>
	    
  ssh table

::
   
      prints contents of the ~/.ssh/config file in table format


Executing Command
^^^^^^^^^^^^^^^^^^^

.. prompt:: bash, cm>

  ssh ARGUMENTS

::
   
      executes the ssh command with the given arguments
      Example:
          ssh myhost

              conducts an ssh login to myhost if it is defined in
              ~/.ssh/config file


Register
^^^^^^^^^^^

.. warning: Not yet implemented

.. prompt:: bash, cm>

    ssh register NAME PARAMETERS

::
   
    registers a host i ~/.ssh/config file
    Parameters are attribute=value pairs
    Note: Note yet implemented
    
