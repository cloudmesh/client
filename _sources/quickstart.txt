Quickstart
============

.. warning:: This quickstart quide assumes that you have prepared your
	     system according to the steps documented in the Section
	     :ref:`preparation`.
		  

Setup
------

.. warning:: The instalation with pip is not yet working at this
	     time. Please use the instalation from source.
	     
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

When locationg a specific command you want to know more about, lets assume you want to know more about the command `color`, say

.. prompt::  cm, cm>

	     help color

	     

Understanding the cloudmesh shell
----------------------------------

The cloudmesh shell contains a number of simple abstractions. This
includes defaults, variables and configuration flags.

To set a default value, for example to set the default cloud to kilo use:

.. prompt:: cm, cm>

	     default cloud=kilo

To configure color output of the cloudmesh shell use:

.. prompt:: cm, cm>

	     color on

To conduct a live refresh in a cloud please use

.. prompt:: cm, cm>

	     refresh on

Getting started with the Cloud(s)
----------------------------------

Naturally you want to get started with clouds. In case you have a
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
and poplulate the cloudmesh.yaml file for you. At this time it will
create an entry for a cloud named kilo.


If you need to view the flavors and images in the cloud, use:

.. prompt:: cm, cm>

	     image refresh
	     flavor refresh

To list the images/flavors use the following:

.. prompt:: cm, cm>

	     list image
	     list flavor

To set default flavor and image use:

.. prompt:: cm, cm>

	     default image=Ubuntu 14.04
	     default flavor=m1.tiny

You also need to set your default group. If you already have a group
created you can use that or else you can specify a new group name.

.. prompt:: cm, cm>

	     default group=test-group

Next, you need to upload your ssh keys to the cloud. If you already
have a key-pair you can use it, or else you can generate ssh keys using::

    $ ssh-keygen -t rsa -C albert@albert-pc

This will generate id_rsa.pub (public key) and id_rsa (private key)
in the ~/.ssh/ directory.

First step (in the process of uploading key to cloud), is to add this key
to the key database. To do so, use:

.. prompt:: cm, cm>

	     key add --ssh --name=id_rsa

You can list the keys in the key database by using:

.. prompt:: cm, cm>

	     key list

The output would look something like::

    +--------+----------------+-------------------------------------+--------------+--------+
    | name   | comment        | uri                                 | fingerprint  | source |
    +--------+----------------+-------------------------------------+--------------+--------+
    | id_rsa | albert@mycompi | file:///home/albert/.ssh/id_rsa.pub | 64:aa: ....  | ssh    |
    +--------+----------------+-------------------------------------+--------------+--------+

Then, to upload this key to the cloud (your default cloud) use:

.. prompt:: cm, cm>

	     key upload albert_ssh_key

Starting up a new VM in the cloud
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

	     network associate floating ip --instance=albert-001

Listing VMs will now show you this floating ip:

.. prompt:: cm, cm>

	     vm list

::

	+----+--------------+------------+--------+-----------+--------------+----------+---------+--------+-------+
	| id | uuid         | label      | status | static_ip | floating_ip  | key_name | project | user   | cloud |
	+----+--------------+------------+--------+-----------+--------------+----------+---------+--------+-------+
	| 47 | 8af4177f-... | albert-001 | ACTIVE | 10.0.2.37 | 152.25.6.101 | id_rsa   | fg478   | albert | kilo  |
	+----+--------------+------------+--------+-----------+--------------+----------+---------+--------+-------+

Next, you need to set your login key to be able to ssh to the VM.
This will be the path to the private key (id_rsa) corresponding to
the public key we uploaded to the cloud:

.. prompt:: cm, cm>

	     default login_key=~/.ssh/id_rsa

Logging into the cloud is now as simple as:

.. prompt:: cm, cm>

	     vm login albert-001

This should get you through to the ssh session to the VM.
Congratulations! You have now learnt how to start a new VM and log into a VM.

To delete a VM, you use:

.. prompt:: cm, cm>

	     vm delete albert-001

HPC
-----

IN order to use the HPC experiment management functionality, you must
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

