Command Ideas
=======================================================================

Summary of commands::

  [daniel] cm register india
  [daniel] cm register CLOUD CERT
  [daniel] cm register CLOUD DIR
  [daniel] cm test cloud CLOUD
  [daniel] cm test ssh HOST
  cm list cloud flavor
  cm update cloud



  cm nova list inactive
  cm nova list gregor*

NOT SURE HWY WE NEED NOVA HERE

This section includes some new ideas from cm commands.


Register
--------

Register futuresystems india cloud which includes openrc and cert::

  cm register india

The next command copies the CERT to the ~/.cloudmesh/clouds/CLOUD directory and
registers that cert in the coudmeh.yaml file::

   cm register CLOUD CERT

Finding the CACERT can be facilitated also while  looking at the
actual values copied. If we find a file specified, in the cert
variable for that cloud, the file is also fetched. The location will
be reset to be where we copy the cert e.g. ~/.cloudmesh/clouds/CLOUD.

In some cases we need more than a  single file and an entire directory
needs to be copied. For this we have the command::

  cm register CLOUD DIR

where DIR specifies the directory that need to be fetched.


Test after Registration
------------------------

To test if a cloud is properly registered and is functioning a test
can be performed::

  cm test cloud CLOUD

To test the ssh connection to a machine we can use::

  cm test ssh HOST

The host is specified in the .ssh/config file. The username and
hostname can be overwritten with user@host


List
----

List all virtual machines that are not active. ::

	cm list inactive


Lists all virtual machines that starts with a specific character or
sequence of characters. After the virtual machine name, a '*' can be
used as a regular expression. The following command lists all the
Virtual machines that has gregor as their prefix. ::

 	cm list gregor-*
	cm list gregor-[001-008]
	cm list gregor-[001-008,010]

The convenient specification to set multiple matches i applied
to all other commands and parameters where possible.

Q: is [01-02] the same as "01,02" or does it need to be
"[01-02]". Looks like from documentation it works without []

We need an extensive manual on this derived from hostlist
https://www.nsc.liu.se/~kent/python-hostlist/
but much better. Section will be called *Parameter Expansion*.

Hostlist is pip installable and listed at
https://pypi.python.org/pypi/python-hostlist/1.14

We may declare its own type nad use that in :type paramter: MultiStr.
This type would than internally use hostlist. The reason why we do not
want the name hostlist is that we use this not only with hosts.

.. note: not yet sure about the name MultiStr


Update
----

Updates information from clouds and stores them in the database::

	cm update india

Individual updates can be called as follows

	cm update india flavor
	cm update india vm
	cm update india image

Combinations are possible::

	cm update india,aws,azure image,vm


Delete
------

The following command deletes all machines that are not active. ::
 
	cm nova delete inactive



Flavor
------

Changes the flavor of either one or several virtual machines so that
they will become faster. In order to run the following command, an
index must be created. Each virtual machine will have an index
associated with it so that commands can be used in several machines at
the same time. Virtual machines from the index 1 to 10 have their
flavor changeded after the command below is run (is it possible to
change the flavor on the fly?) ::

	cm flavor-up [0:10]

Changes the flavor of either one or several virtual machines so that
they will become slower. The following command changes the flavor of
the virtual machines from 20 to 30 index. ::

	cm flavor-down [20:30]

Security
--------

The following command protects a set of virtual machine against
accidentally changes. Whenever the user wants to delete a virtual
machine, a password will be asked. ::

	cm lock --vm-name

Order
-----

Orders the virtual machines by flavor and displays them on the screen. ::

	cm order-flavor

Orders the virtual machines by status and displays them on the screen. ::
  
	cm order-status



Boot
-----
 
Run the following command to fix errors that occurred during the boot
process. If there is no resources available, it tries to change the
virtual machine flavor in order to boot them correctly. ::

	cm restart all-error


Creates a new virtual machine and adds a label to it. That label can
be used to identify what type of task a virtual machine is
running. Commands such as delete and flavor-up can be applied in
certain labels. ::

	cm boot --flavor --image --key-name --name [label]
 
With this command, several virtual machines can be created at the same time. ::

	cm boot --flavor --image --key-name --name [--quantity]

Deletes all machines that has a specific label. ::
	
	cm delete --label


MORE COMMANDS
-------------

	default active ATTRIBUTE=VALUE
	default list
	default [--cloud=CLOUD] ATTRIBUTE=VALUE


	pprint(arguments)
	if arguments[ATTRIBUTE=VALUE]:
		(a, v) = split("=", 1)

		if a = "activate"
::

	cm default --cloud=india format-table-header="name,id"
	cm default --cloud=india format-table-header=name,id
  	cm default --cloud=india format-table-order="name,id"
  	cm default active clouds=india,azure
  	cmd list clouds
  	cm default india image=abc
  	cm default india flavor=xyz

Nova Pass through
------------------

::

	cm nova ...

simple nova pass through command
