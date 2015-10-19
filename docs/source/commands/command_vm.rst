VM Command
======================================================================

VM Command is used to manage VM instances across clouds.
It is like a one stop interface that can be used to perform various VM
operations on various clouds available to Cloudmesh.

The manual page of the key command can be found at: `VM <../man/man.html#vm>`_

Starting a VM instance
-----------------------

You can start a VM on any target cloud like 'india' by using the 'vm start'
like the one provided below::

    $ cm vm start --name=testvm --cloud=india --image=619b8942-2355-4aa2-bae3-74b8f1751911 --flavor=2
    Machine testvm is being booted on india Cloud...

Listing a VM instances
-----------------------

You can list all the VM instances running on the cloud by 'vm list' command
like the one below::

    $ cm vm list --cloud=india
    +--------------------------------------+--------------+--------+
    | id                                   | name         | status |
    +--------------------------------------+--------------+--------+
    | 21305503-2649-4338-8876-d825758c83f3 | albert-001   | ACTIVE |
    | 6437e054-b761-4408-890a-ced65cc848e2 | albert-002   | ACTIVE |
    | 94f01af3-ee2a-44c9-b228-75627f358169 | albert-003   | ACTIVE |
    | d0f923f9-b4c0-411a-87dc-99870b49ae6e | testvm       | ACTIVE |
    +--------------------------------------+--------------+--------+

Assign Floating IP to VM
-------------------------

In order to access the vm from outside of the cloud private network, we need to assign a floating IP which can be
accessed publicly::

    $ cm vm floating_ip_assign testvm
    Floating IP assigned to testvm successfully and it is: 149.165.158.XX

Retrieving IP Address details
------------------------------

You can get the IP address details of a VM by the following command::

    $ cm vm ip_show testvm --cloud=india
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

    $ cm vm login testvm --user=albert --key=/location/id_rsa
    Determining IP Address to use with a ping test...
    Checking 10.23.2.XX...
    Cannot reach 10.23.2.XX.
    Checking 149.165.158.XX...
    IP to be used is: 149.165.158.XX
    Warning: Permanently added '149.165.158.XX' (ECDSA) to the list of known hosts.
    Enter passphrase for key '/location/id_rsa':
    Welcome to Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-63-generic x86_64)

      * Documentation:  https://help.ubuntu.com/

      System information as of Mon Oct 19 04:17:48 UTC 2015

      System load: 0.0               Memory usage: 2%   Processes:       52
      Usage of /:  56.9% of 1.32GB   Swap usage:   0%   Users logged in: 0

      Graph this data and manage this system at:
        https://landscape.canonical.com/

      Get cloud support with Ubuntu Advantage Cloud Guest:
        http://www.ubuntu.com/business/services/cloud

    0 packages can be updated.
    0 updates are security updates.



    The programs included with the Ubuntu system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
    applicable law.

    albert@testvm:~$

Deleting a VM
--------------

You can delete a VM on the target cloud by using 'vm delete' command as below::

    $ cm vm delete testvm --cloud=india
    Machine testvm is being deleted on india Cloud...


