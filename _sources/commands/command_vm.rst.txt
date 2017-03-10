VM Command
======================================================================

VM Command is used to manage VM instances across clouds.
It is like a one stop interface that can be used to perform various VM
operations on various clouds available to Cloudmesh.

The manual page of the `vm` command can be found at: `vm <../man/man.html#vm>`__

Listing Defaults
^^^^^^^^^^^^^^^^^

You can have a list of relevant default attributes required for VM operations::

    $cm register export kilo --format=table

    +-------------+-----------------+
    | Attribute   | Value           |
    +-------------+-----------------+
    | cloud       | kilo            |
    | key         | albert          |
    | user        | albert          |
    | vm          |                 |
    | group       | default         |
    | secgroup    | default         |
    | counter     | 1               |
    | image       | Ubuntu-14.04-64 |
    | flavor      | m1.small        |
    | refresh     | None            |
    | debug       | True            |
    | interactive | None            |
    | purge       | None            |
    +-------------+-----------------+
- cloud - Current active cloud
- key - Key name from db used for VM boot
- user - User name for the current active cloud
- group - Group for the VM to be booted
- secgroup - Security Group to be provided for VM boot
- counter - the count to be used in the VM name
- flavor - Flavor ID required for VM boot.
- image - Image ID required for VM boot.
- refresh - If refresh flag is set
- debug - if debug flag is set
- interactive - if interactive flag is set
- purge - if the purge flag is set. This determines if a 'delete' on the cloud
will also delete the records from the local db


Booting a VM instance
-----------------------

If you have all the required attributes (secgroup not mandatory) setup and listed in the vm defaults,
then you can simply run the following to boot a vm.:

.. prompt:: bash, cm>
	    
    vm boot

::
   
    Machine albert-001 is being booted on cloud cm ...
    +-----------+--------------------------------+
    | Attribute | Value                          |
    +-----------+--------------------------------+
    | cloud     | cm                             |
    | flavor    | m1.small                       |
    | image     | Ubuntu-Server-14.04-LTS        |
    | key       | albert                         |
    | meta      | +                              |
    |   -       | category: cm                   |
    |   -       | kind: cloudmesh                |
    |   -       | group: default                 |
    |   -       | image: Ubuntu-Server-14.04-LTS |
    |   -       | key: albert                    |
    |   -       | flavor: m1.small               |
    | name      | albert-001                     |
    | nics      |                                |
    | secgroup  | +                              |
    |   -       | default                        |
    +-----------+--------------------------------+
    info. OK.

Else you may explicitly specify the attribute values in the arguments to the vm boot command.:

.. prompt:: bash, cm>
	    
    vm boot --name=testvm --cloud=kilo --image=619b8942-2355-4aa2-jaa5-74b8f1751911 --flavor=2

::
    
    Machine testvm is being booted on kilo Cloud...

Listing a VM instances
-----------------------

You can list all the VM instances running on the cloud by 'vm list' command
like the one below::

    +----+--------------------------------------+------------------------------+-----------+-------------+-----------------+-------------------------+-----------+-----------+-------+
    | id | uuid                                 | label                        | status    | static_ip   | floating_ip     | key_name                | project   | user      | cloud |
    +----+--------------------------------------+------------------------------+-----------+-------------+-----------------+-------------------------+-----------+-----------+-------+
    | 10 | 21305503-2649-3664-8876-d825758c83f3 | albert-001                   | ACTIVE    | 10.20.99.xx | 140.123.44.xxx  | albert-key              | undefined | albert    | kilo  |
    | 9  | 94f01af3-ee2a-9887-b228-75627f358169 | albert-001                   | SHUTOFF   | 10.20.99.xx | 140.123.44.xxx  | albert-key              | undefined | albert    | kilo  |
    | 8  | 2f275d38-62af-1223-a04a-0456e0d6466f | albert-server-jzqc23pekfcu   | SUSPENDED | 10.20.99.xx | 140.123.44.xxx  | albert-india-key        | undefined | albert    | kilo  |
    | 7  | 6730c273-609f-9879-a481-313ff4200d82 | albert-server-ekbvvsmjyqlo   | ACTIVE    | 10.20.99.xx | 140.123.44.xxx  | albert-india-key        | undefined | albert    | kilo  |
    | 6  | fa3580f3-2dbd-d666-9178-326b39916c09 | albert-server-cdmelfaefggf   | ACTIVE    | 10.20.99.xx | 140.123.44.xxx  | albert-india-key        | undefined | albert    | kilo  |
    +----+--------------------------------------+------------------------------+-----------+-------------+-----------------+-------------------------+-----------+-----------+-------+


Stop a VM
----------

You can stop a VM by supplying it's label or UUID:

.. prompt:: bash, cm>
	    
    vm stop testvm --cloud=kilo

::
   
    Machine testvm is being stopped on kilo Cloud...
    info. OK.

.. warning:: ERROR: Problem stopping instances


Start a VM
-----------

You can start a VM by supplying it's label or UUID:

.. prompt:: bash, cm>
	    
    vm start testvm --cloud=kilo

::
   
    Machine testvm is being started on kilo Cloud...
    info. OK.

Assign Floating IP to VM
-------------------------

In order to access the vm from outside of the cloud private network, we need to assign a floating IP which can be
accessed publicly:

.. prompt:: bash, cm>
	    
    vm ip assign testvm

::
   
    Floating IP assigned to testvm successfully and it is: 149.165.158.XX

.. warning:: seems working, bug to 'non unique match' error, while 'cm vm list --refresh'
does not indicate so. The problem might be in 'cm vm list' and/or 'refresh'

Retrieving IP Address details
------------------------------

You can get the IP address details of a VM by the following command:

.. prompt:: bash, cm>
	    
    vm ip show testvm

::
   
    +--------------+--------------+-----------------+
    | name         | static_ip    | floating_ip     |
    +--------------+--------------+-----------------+
    | albert-001   | 192.168.0.74 | 12x.11x.11x.12x |
    +--------------+--------------+-----------------+

..note:: The real floating IP has been masked in this example, while the command
shows the true IPs.

Login to VM
------------
You can login to a VM in your target cloud:

.. prompt:: bash, cm>
	    
    vm login testvm --user=albert --key=/location/id_rsa --cloud=kilo

::
   
    Logging in into testvm machine...
    Determining IP Address to use with a ping test...
    Checking 10.23.2.XX...
    Cannot reach 10.23.2.XX.
    Checking 149.165.158.XX...
    IP to be used is: 149.165.158.XX
    Warning: Permanently added '149.165.158.XX' (ECDSA) to the list of known hosts.
    Enter passphrase for key '/location/id_rsa':
    Welcome to <OS> <VERSION>.3 LTS (GNU/Linux <VERSION> <BIT_SPEC>)

      * Documentation:  https://help.os.com/

      System information as of Mon Oct 19 04:17:48 UTC 2015

      System load: 0.0               Memory list: 2%   Processes:       52
      Usage of /:  56.9% of 1.32GB   Swap list:   0%   Users logged in: 0

      Graph this data and manage this system at:
        https://landscape.canonical.com/

      Get cloud support with OS Advantage Cloud Guest:
        http://www.OS.com/business/services/cloud

    0 packages can be updated.
    0 updates are security updates.



    The programs included with the OS system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    OS comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
    applicable law.

    albert@testvm:~$

.. warning:: login not working anymore

Running command on VM
----------------------

You can use the vm login to simply run a command on the target VM:

.. prompt:: bash, cm>
	    
  vm login testvm --user=albert --key=/location/id_rsa --command="uname\ -a" --cloud=kilo

::
   
  Logging in into testvm machine...
  Determining IP Address to use with a ping test...
  Checking 10.23.2.XX...
  Cannot reach 10.23.2.XX.
  Checking 149.165.159.XX...
  IP to be used is: 149.165.159.XX
  Enter passphrase for key '/location/id_rsa':
  OS testvm <VERSION> #103-OS SMP Fri Aug 14 21:42:59 UTC 2015 <BIT_SPEC> OS

.. warning:: depends on the login being working

Deleting a VM
--------------

You can delete a VM on the target cloud by using 'vm delete' command as below:

.. prompt:: bash, cm>
	    
    vm delete testvm --cloud=kilo

::
   
   Machine testvm is being deleted on kilo Cloud...

Renaming a VM
--------------

You can rename a VM on the target cloud by using 'vm rename' command as below:

.. prompt:: bash, cm>
	    
    vm rename testvm --new=testvm_renamed --cloud=kilo

::
   
    Renaming VM (testvm) : 5bd7911e2b-xxxx-xxxx-xxxx-xxxxxxx
    Machine testvm renamed to testvm_renamed on kilo Cloud...

.. warning:: renamed on the remote cloud; but the local db shows two copies of the records.
One for the old name, and one for the new name.

