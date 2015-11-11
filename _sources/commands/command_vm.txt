VM Command
======================================================================

VM Command is used to manage VM instances across clouds.
It is like a one stop interface that can be used to perform various VM
operations on various clouds available to Cloudmesh.

The manual page of the key command can be found at: `VM <../man/man.html#vm>`_

Booting a VM instance
-----------------------

You can start a VM on any target cloud like 'juno' by using the 'vm start'
like the one provided below::

    $ cm vm boot --name=testvm --cloud=juno --image=619b8942-2355-4aa2-bae3-74b8f1751911 --flavor=2
    Machine testvm is being booted on juno Cloud...

Listing a VM instances
-----------------------

You can list all the VM instances running on the cloud by 'vm list' command
like the one below::

    $ cm vm list --cloud=juno
    +----+--------------------------------------+------------------------------+---------+-----------+-----------+-------+
    | id | uuid                                 | label                        | status  | project   | user      | cloud |
    +----+--------------------------------------+------------------------------+---------+-----------+-----------+-------+
    | 1  | 6d2b8e67-a296-45f0-9132-b65aeddff8ff | testvm                       | ACTIVE  | undefined | albert    | juno  |
    | 2  | 390792c3-66a0-4c83-a0d7-c81e1c787710 | albert_vm002                 | ACTIVE  | undefined | albert    | juno  |
    | 3  | fa3580f3-2dbd-4d67-9178-326b39916c09 | albert_vm003                 | ACTIVE  | undefined | albert    | juno  |
    | 4  | 6730c273-609f-426d-a481-313ff4200d82 | albert_vm004                 | ACTIVE  | undefined | albert    | juno  |
    | 5  | 2f275d38-62af-4f71-a04a-0456e0d6466f | albert_vm005                 | ACTIVE  | undefined | albert    | juno  |
    | 6  | 94f01af3-ee2a-44c9-b228-75627f358169 | albert_vm006                 | SHUTOFF | undefined | albert    | juno  |
    | 7  | 21305503-2649-4338-8876-d825758c83f3 | albert_vm007                 | ACTIVE  | undefined | albert    | juno  |
    +----+--------------------------------------+------------------------------+---------+-----------+-----------+-------+


Stop a VM
----------

You can stop a VM by supplying it's label or UUID::

    $ cm vm stop testvm --cloud=juno
    Machine testvm is being stopped on juno Cloud...
    info. OK.

Start a VM
-----------

You can start a VM by supplying it's label or UUID::

    $ cm vm start testvm --cloud=juno
    Machine testvm is being started on juno Cloud...
    info. OK.

Assign Floating IP to VM
-------------------------

In order to access the vm from outside of the cloud private network, we need to assign a floating IP which can be
accessed publicly::

    $ cm vm floating_ip_assign testvm --cloud=juno
    Floating IP assigned to testvm successfully and it is: 149.165.158.XX

Retrieving IP Address details
------------------------------

You can get the IP address details of a VM by the following command::

    $ cm vm ip_show testvm --cloud=juno
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

    $ cm vm login testvm --user=albert --key=/location/id_rsa --cloud=juno
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

  $ cm vm login testvm --user=albert --key=/location/id_rsa --command="uname\ -a" --cloud=juno
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

    $ cm vm delete testvm --cloud=juno
    Machine testvm is being deleted on juno Cloud...


