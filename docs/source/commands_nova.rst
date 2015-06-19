Command Ideas
=======================================================================


List
----

List all virtual machines that are not active. ::

	cm nova list inactive


Lists all virtual machines that starts with a specific character or
sequence of characters. After the virtual machine name, a '*' can be
used as a regular expression. The following command lists all the
Virtual machines that has dasilva as their prefix. ::

 	cm nova list dasilva* 

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

	cm nova flavor-up [0:10] 

Changes the flavor of either one or several virtual machines so that
they will become slower. The following command changes the flavor of
the virtual machines from 20 to 30 index. ::

	cm nova flavor-down [20:30] 

Security
--------

The following command protects a set of virtual machine against
accidentally changes. Whenever the user wants to delete a virtual
machine, a password will be asked. ::

	cm nova lock --vm-name 

Order
-----

Orders the virtual machines by flavor and displays them on the screen. ::

	cm nova order-flavor

Orders the virtual machines by status and displays them on the screen. ::
  
	cm nova order-status



Boot
-----
 
Run the following command to fix errors that occurred during the boot
process. If there is no resources available, it tries to change the
virtual machine flavor in order to boot them correctly. ::

	cm nova restart all-error


Creates a new virtual machine and adds a label to it. That label can
be used to identify what type of task a virtual machine is
running. Commands such as delete and flavor-up can be applied in
certain labels. ::

	cm nova boot --flavor --image --key-name --name [label] 
 
With this command, several virtual machines can be created at the same time. ::

	cm nova boot --flavor --image --key-name --name [--quantity]

Deletes all machines that has a specific label. ::
	
	cm nova delete --label

