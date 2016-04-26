Quickstart
============

.. warning:: This quickstart quide assumes that you have prepared your
	     system according to the steps documented in the Section
	     :ref:`preparation`. We also strongly recommend you read
	     the sections :ref:`installation` and
	     :ref:`configuration`.
		  

Setup
------

.. warning:: At this time do not use the pip install as we have not
             yet uploaded the newest version to pypi. Instead, plase
             use the source install discussed in our manual

The setup of cloudmesh client is quite simple and can be done with::

    pip install cloudmesh_client

However, you may want to read carefully our setup guide and prepare
your machine as your OS may not have the required packages installed
by default (see: :ref:`preparation`).
	     
Help
-----

There are many commands in cloudmesh, and you can find
out more about them while typing in

.. prompt::  cm, cm>

	     help

When locationg a specific command you want to know more about, lets
assume you want to know more about the command `color`, say

.. prompt::  cm, cm>

	     help color

	     

Defaults and Variables
----------------------------------

The cloudmesh shell contains a number of useful concepts. This
includes defaults, variables and configuration flags.
While Variables are not saved between different instantiations of
cloudmesh, defaults are saved. Thus the values of defaults can be used
consistently between invocations.

To set a default value, for example to set the default cloud to kilo use:

.. prompt:: cm, cm>

	     default cloud=kilo

Some defaults are also set via special commands to make the use more prominent.
To configure color output of the cloudmesh shell use:

For example to set the refresh behavior to update a list command from
a cloud before display you can either use the command:

.. prompt:: cm, cm>

	     refresh on

or

.. prompt:: cm, cm>

	     default refresh=True

	     
Accessing Clouds
----------------------------------

Naturally, you want to get started with clouds. In case you have a
username and project in futuresystems using cloudmesh is easy. Only
thing you need is an entry in the .ssh/config file with the machine
name india, like follows::

    Host india
    Hostname india.futuresystems.org
    User albert

Next you can register the cloud(s) with:

.. prompt:: cm, cm>

	     register remote

This will fetch the necessary credentials from the cloud,
and populate the cloudmesh.yaml file for you. At this time it will
update an entry for a cloud named kilo.

In case you want to add other clouds such as chameleon you can use the
command

.. prompt:: cm, cm>

	     register chameleon

This command will than interactively ask you for information about
the cloud credentials and update the yaml file accordingly. To set the 
default cloud use the `default` command.

If you need to view the flavors and images in the cloud, use:

.. prompt:: cm, cm>

	     image refresh
	     flavor refresh

The refresh commands are not necessary if you use `refresh
on`. However in this case every time you invoke a list command the
cloud is contacted and the data is updated. IF you do not use refresh,
the data is read from an internal database.

To list the images, flavors, and vms use the following:

.. prompt:: cm, cm>

	     image list
	     flavor list
	     vm list

To se a selected number of important defaults for the clouds use the
command

.. prompt:: cm, cm>

	    cm info

To set default flavor and image use, inspect the results from the list
commands, decide which you want to use, and simply set them for the
current default cloud. Also make sure that the image size is
appropriate. Some images will not fit in a small flavor.
And as always, please assure proper spelling of the image name:

.. prompt:: cm, cm>

	     default image=Ubuntu-14.04-64
	     default flavor=m1.small

When starting vms the vms are added to a default group. The initial
default group name is simply 'default'. If you like to change it you
can set it with the following command:

.. prompt:: cm, cm>

	     default group=experiment_a

Next, you need to upload your ssh keys to the cloud. If you already
have a key-pair you can use it, or else you can generate ssh keys using:

.. prompt:: bash $

	    ssh-keygen -t rsa -C albert@gmail.com

This will generate a keypair id_rsa.pub (public key) and id_rsa (private key)
in the ~/.ssh/ directory. Next you need to add this key to cloudmesh
with:

.. prompt:: cm, cm>

	     key add --ssh


You can list the keys in the key database by using:

.. prompt:: cm, cm>

	     key list

The output would look something like::

    +--------+------------------+-------------------------------------+--------------+--------+
    | name   | comment          | uri                                 | fingerprint  | source |
    +--------+------------------+-------------------------------------+--------------+--------+
    | id_rsa | albert@gmail.com | file:///home/albert/.ssh/id_rsa.pub | 64:aa: ....  | ssh    |
    +--------+------------------+-------------------------------------+--------------+--------+

Next the key needs to be uploaded to the cloud. Here we take advantage
of the default cloud being automatically used:

.. prompt:: cm, cm>

	     key upload

in case you want to upload it to another cloud you can set the default
cloud and repeat this command, or simply specify the cloud as a
parameter:

.. prompt:: cm, cm>

	     key upload --cloud=chameleon

Virtual Machines
----------------------------------

If you have followed this document till this point, you are all set
to start a new VM in the cloud. This section explains how to do that.

First, make sure all defaults are correctly set.
	     
.. prompt:: cm, cm>

	     vm default

The output will look somewhat similar to the following::

	+-----------+---------------+
	| Attribute | Value         |
	+-----------+---------------+
	| secgroup  |               |
	| name      | albert-001    |
	| image     | Ubuntu 14.04  |
	| cloud     | kilo          |
	| group     | test-group    |
	| key       | id_rsa        |
	| flavor    | m1.tiny       |
	| login_key |               |
	+-----------+---------------+
	info. OK.


Starting a VM now is as simple as executing a single command.

.. prompt:: cm, cm>

	     vm boot

This will start up a new VM in your default cloud.
You need to refresh the database before listing VMs.

.. prompt:: cm, cm>

	     vm refresh
	     vm list

The output will look something like follows::

	+----+--------------+------------+--------+-----------+-------------+----------+---------+--------+-------+
	| id | uuid         | label      | status | static_ip | floating_ip | key_name | project | user   | cloud |
	+----+--------------+------------+--------+-----------+-------------+----------+---------+--------+-------+
	| 47 | 8af4177f-... | albert-001 | ACTIVE | 10.0.2.37 |             | id_rsa   | fg478   | albert | kilo  |
	+----+--------------+------------+--------+-----------+-------------+----------+---------+--------+-------+


Congratulations! you have now learnt how to set up cloudmesh, and use it to start a VM.
Next step naturally is to login to the virtual machine. To do so, we need to assign it
a public IP (also called floating IP).

To associate a floating ip to an instance (albert-001) in our case, use:

.. prompt:: cm, cm>

	     vm ip assign albert-001

Listing VMs will now show you this floating ip:

.. prompt:: cm, cm>

	     vm list

::

	+----+--------------+------------+--------+-----------+--------------+----------+---------+--------+-------+
	| id | uuid         | label      | status | static_ip | floating_ip  | key_name | project | user   | cloud |
	+----+--------------+------------+--------+-----------+--------------+----------+---------+--------+-------+
	| 47 | 8af4177f-... | albert-001 | ACTIVE | 10.0.2.37 | 152.25.6.101 | id_rsa   | fg478   | albert | kilo  |
	+----+--------------+------------+--------+-----------+--------------+----------+---------+--------+-------+

Logging into the cloud is now as simple as:

.. prompt:: cm, cm>

	     vm login albert-001

This should get you through to the ssh session to the VM.The user name
to be used at login is either automatically detected and added to the
vm information. If you like to change the username for the login you can use the
username parameter

.. prompt:: cm, cm>

	     vm login albert-001 --username=ubuntu

To change the default username for a vm you can use the command

.. prompt:: cm, cm>


	    vm username ubuntu albert-001

This will set the username for the vm `albert-001` to `ubuntu`


To delete a VM, you use the vm name:

.. prompt:: cm, cm>

	     vm delete albert-001

VM Quickstart
-------------

To summarize the steps to start a working cloudmesh client and prepare
a simple default while using the `futuresystems.org` cloud use the commands:



.. prompt:: cm, cm>

	    cm add key --ssh
	    cm register remote
	    cm default cloud=kilo
	    cm refresh on
	    cm info

Inspect the info and see if the settings satisfy your needs. Change
them accordingly with the cloudmesh commands.

Now booting and managing a vm is real simple

.. prompt:: cm, cm>

	    cm boot
	    cm ip assign
	    cm login

And to delete the vm

.. prompt:: cm, cm>

	    cm delete --force

	 
	     
HPC
-----

In order to use the HPC experiment management functionality, you must
register the queuing system in the yaml file and register the login
node in the .ssh/config file. If you are using india and have used the
clouds before, you may have already done this.

To start a command such as uname and execute a command you can say:

.. prompt:: cm, cm>

	     run uname

	     
It will print a job number that you may use to interact with the
system further to for example list the output

.. prompt:: cm, cm>

	     run list 101

(We assume here 101 is your job id)
	     
To see the status and the output you can say

.. prompt:: cm, cm>

	     run status 101
	     run output 101	     

