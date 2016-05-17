Key Command
============

In clouds and distributed environments security keys are used for
authentication. We like to be able to register specific keys with
clouds or vms and easily use them. To do so we upload them into a key
registry in which each key is uniquely named. We use these named keys
when we start up virtual machines or log into remote machines.

The manual page of the `key` command can be found at: `key
<../man/man.html#key>`_


Key
---

It is imperative that users of clouds understand how to use ssh
keys. There are many great resources in the internet that describes
this topic in great deatail. We assume that you are familiare with ssh
keys. IF not you shoudl stop here and read up on them and understand
its use. To generate an id_rsa key, please use the command:

.. prompt:: bash
  
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

When prompted for the filename press enter. Next it is imporatnt that
you define a passphrase. **Do not** enter just return as this is an
unexeptable practice not tou use a password for accessing your vms.

.. warning:: It is important that you choes a password becuas eif your
	     machine were to be compromised attackers could login on
	     all machines you use this key. Please read the ssh
	     documentation about it.
	     As a comparision it is like putting a bank key of a door in
	     the window, so that a burglar can smash the window and
	     get the key to go to the bank and get your gold out of
	     the safe.

	 
	    


Adding a key to the database
-----------------------------

To add you ssh key to cloudmesh you can simply say:

.. prompt:: bash, cm>
	    
    key add --ssh


Adding the ket to the cloud
---------------------------

Naturally you ned to let the clouds also know about this key, so you
need to upload it. We assume that you have a unique name defined that
can be used across all clouds. If not make sure you do so.

Assume a cloud default is set than you can uploadthe key with:

.. prompt:: bash, cm>
	    
  key upload

To upload it to anotherc cloud you can set the cloud default to the
other cloud and repeat the upload command or you can explicitly
specify the cloud with:

.. prompt:: bash, cm>
	    
  key upload --cloud=mycloud

where mycloud is specified in the `~/.cludmesh/cloudmesh.yaml` file.


List Keys
----------

To list the keys in the registry you can use the command:

.. prompt:: bash, cm>
	    
      key list

::
   
        +---------+------------------+---------------------------------+-------------------------------------------------+--------+
        | name    | comment          | uri                             | fingerprint                                     | source |
        +---------+------------------+---------------------------------+-------------------------------------------------+--------+
        | albert  | albert@Zweistein | file:///home/albert/id_rsa.pub  | 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39 | ssh    |
        +---------+------------------+---------------------------------+-------------------------------------------------+--------+


To change the output format you can specify it with the --format
option:

.. prompt:: bash, cm>
	    
  key list --format=json

::
   
  "1": {
            "comment": "albert@Zweistein",
            "kind": "key",
            "name": "demokey",
            "created_at": "2015-09-23 15:58:32",
            "uri": "file:///home/key_expt/id_rsa.pub",
            "value": null,
            "updated_at": "2015-09-23 16:14:41",
            "project": "undefined",
            "source": "ssh",
            "user": "undefined",
            "fingerprint": "4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39",
            "label": "demokey",
            "id": 1,
            "cloud": "general"
        }
    }

.. note:: we do show an abbreviation of the key for illustration.    


Get Keys
---------

To get the fingerprint of a key you can obtain it with:

.. prompt:: bash, cm>
	    
 key get albert

::
   
 alber: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39


Default Keys
-------------

In many cases it is convenient to just use a default key that is
set. The add command sets the key automatically. If you need to set it
by hand you can use

To mark key as default by name you can use the command:

.. prompt:: bash, cm>
	    
    default key=albert


Interactive Selection
---------------------

In case you have many keys (which we do not recommend) we can set the default key also
interactively with the select option:

.. prompt:: bash, cm>
	    
    key default --select

::
   
    KEYS
    ====

        1 - albert: 4e:fc:e8:03:4e:c7:8e:ca:30:1a:54:43:8d:24:90:39
        2 - testkey: 2d:18:a8:03:1e:e1:7e:fe:b3:fa:59:49:c7:c2:cf:01
        q - quit


    Select between 1 - 2: 2
    choice 2 selected.
    Setting key: rsa as default.

    
Delete Keys
------------

A named key can be deleted from the registry with the command, where
'demokey' is the name of the key:

.. prompt:: bash, cm>
	    
    key delete albert

::
   
    Key demokey deleted successfully from database.

Alternatively you can also interactively select it:

.. prompt:: bash, cm>
	    
    $ cm key delete --select

To delete all keys from database use:

.. prompt:: bash, cm>
	    
    key delete --all

::
   
    All keys from the database deleted successfully.


