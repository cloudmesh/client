Quickstart
============

.. warning:: The quickstart guide has not bee written and tested yet.
   

Setup
------

THe setup of cloudmesh client is quite simple and can be done with::

  pip install cloudmesh_client

However, you may want to read carefully our setup guide and prepare
your machine as your OS may not have the required packages installed
by default.
	     
Shell
------

The cloudmesh shell contains a number of simple abstractions. This
includes defaults, variables and configuration flags.

To set a default use for example the cloud to kilo:

.. prompt:: cm, cm>

	     default cloud=kilo

To configure color output of the cloudmesh shell use:

.. prompt:: cm, cm>

	     color on

To conduct a life refresh in a cloud please use

.. prompt:: cm, cm>

	     refresh on

Clouds
-------

Naturally you want to get started with clouds. IN case you have a
username and project in futuresystems using cloudmesh is easy. Only
thing you need is an entry in the .ssh/config file with the machine
name india.

.. todo:: put a link here how to configure the .ssh/config file

Next you can register the cloud(s) with

.. prompt:: cm, cm>

	     register remote

To start a vm say	     

.. prompt:: cm, cm>

	     register remote

To login use

.. prompt:: cm, cm>

	     login

To delete the vm, log out of the vm in case you are in it and say
	     
.. prompt:: cm, cm>

	     delete <the last vm name>

Where the <last vm name> is the name of your vm. If you forgot the
name, look it up with

.. prompt:: cm, cm>

	     vm list

To find other flavors or images use	     

.. prompt:: cm, cm>

	     list images
	     list flavors

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

Help
-----

Naturally there are many more commands in cloudmesh, and you can find
out more about them while typing in

.. prompt::  cm, cm>

	     help
	     
