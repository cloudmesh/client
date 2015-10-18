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

Retrieving IP Address details
------------------------------

You can get the IP address details of a VM by the following command::

    $ cm vm ip_show testvm --cloud=india
    IP Addresses of instance testvm are as follows:-
    +---------+---------+----------------+
    | network | version | addr           |
    +---------+---------+----------------+
    | int-net | 4       | 10.23.2.253    |
    | int-net | 4       | 149.165.158.90 |
    +---------+---------+----------------+

Deleting a VM
--------------

You can delete a VM on the target cloud by using 'vm delete' command as below::

    $ cm vm delete testvm --cloud=india
    Machine testvm is being deleted on india Cloud...
