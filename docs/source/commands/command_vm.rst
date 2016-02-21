VM Command
======================================================================

VM Command is used to manage VM instances across clouds.
It is like a one stop interface that can be used to perform various VM
operations on various clouds available to Cloudmesh.

The manual page of the key command can be found at: `VM <../man/man.html#vm>`_

Listing Defaults
^^^^^^^^^^^^^^^^^

You can have a list of relevant default attributes required for VM operations::

    +-----------+--------------------------------------+
    | Attribute | Value                                |
    +-----------+--------------------------------------+
    | secgroup  |                                      |
    | login_key | /home/albert/key/id_rsa              |
    | flavor    | 2                                    |
    | image     | 619b8942-2355-4aa2-jaa5-74b8f1751911 |
    | cloud     | kilo                                 |
    | name      | albert-015                           |
    | key       | albertkey                            |
    | group     | test                                 |
    +-----------+--------------------------------------+

- secgroup - Security Group to be provided for VM boot.
- login_key - Path to private key required for VM login.
- flavor - Flavor ID required for VM boot.
- image - Image ID required for VM boot.
- cloud - Target Cloud.
- name - Name of the VM to be booted. This is in format <username>-<count>. Username retrieved from cloudmesh.yaml, count retrieved from a counter in database.
- key - Key name from db used for VM boot.
- group - Group for the VM to be booted.


Booting a VM instance
-----------------------

If you have all the required attributes (secgroup not mandatory) setup and listed in the vm defaults,
then you can simply run the following to boot a vm.::

    $ cm vm boot
    Machine albert-015 is being booted on kilo Cloud...
    Added ID [4a37b49a-9768-88cc-b988-01013701a8fb] to Group [test]
    info. OK.

Else you may explicitly specify the attribute values in the arguments to the vm boot command.::

    $ cm vm boot --name=testvm --cloud=kilo --image=619b8942-2355-4aa2-jaa5-74b8f1751911 --flavor=2
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

You can stop a VM by supplying it's label or UUID::

    $ cm vm stop testvm --cloud=kilo
    Machine testvm is being stopped on kilo Cloud...
    info. OK.

Start a VM
-----------

You can start a VM by supplying it's label or UUID::

    $ cm vm start testvm --cloud=kilo
    Machine testvm is being started on kilo Cloud...
    info. OK.

Assign Floating IP to VM
-------------------------

In order to access the vm from outside of the cloud private network, we need to assign a floating IP which can be
accessed publicly::

    $ cm vm floating_ip_assign testvm --cloud=kilo
    Floating IP assigned to testvm successfully and it is: 149.165.158.XX

Retrieving IP Address details
------------------------------

You can get the IP address details of a VM by the following command::

    $ cm vm ip_show testvm --cloud=kilo
    IP Addresses of instance testvm are as follows:-
    +---------+---------+----------------+
    | network | version | addr           |
    +---------+---------+----------------+
    | int-net | 4       | 10.23.2.XX     |
    | int-net | 4       | 149.165.158.XX |
    +---------+---------+----------------+

Login to VM
------------
You can login to a VM in your target cloud::

    $ cm vm login testvm --user=albert --key=/location/id_rsa --cloud=kilo
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


Running command on VM
----------------------

You can use the vm login to simply run a command on the target VM::

  $ cm vm login testvm --user=albert --key=/location/id_rsa --command="uname\ -a" --cloud=kilo
  Logging in into testvm machine...
  Determining IP Address to use with a ping test...
  Checking 10.23.2.XX...
  Cannot reach 10.23.2.XX.
  Checking 149.165.159.XX...
  IP to be used is: 149.165.159.XX
  Enter passphrase for key '/location/id_rsa':
  OS testvm <VERSION> #103-OS SMP Fri Aug 14 21:42:59 UTC 2015 <BIT_SPEC> OS

Deleting a VM
--------------

You can delete a VM on the target cloud by using 'vm delete' command as below::

    $ cm vm delete testvm --cloud=kilo
    Machine testvm is being deleted on kilo Cloud...


