Network Command
======================================================================

The Network command provides an API that allows users to set up
and define network connectivity and addressing in the cloud.
Network command handles the creation and management of a virtual networking infrastructure,
including networks, fixed & floating ips.

The manual page of the network command can be found at: `network <../man/man.html#network>`


..note:: We assume you have your default cloud set,
          via the default command::

            $ cm default cloud=juno


List Floating IP Pools
-----------------------

To list the floating ip pools in your cloud network use::

  $ cm network list floating pool
    +------------------+
    | floating_ip_pool |
    +------------------+
    | ext-net          |
    +------------------+


List Floating IP Addresses
---------------------------

To list the floating ip addresses in you cloud use::

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+


To view the floating ip details for a particular instance, use::

  $ cm network list floating ip --instance=albert-004
    +---------------+--------------------------------------+
    | name          | value                                |
    +---------------+--------------------------------------+
    | fixed_ip      | 10.0.2.10                            |
    | ip            | 100.165.123.111                      |
    | id            | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 |
    | instance_id   | a183b85f-2d4r-44b9-933f-64562380286f |
    | pool          | ext-net                              |
    | project       | fg478                                |
    | user          | albert                               |
    | instance_name | albert-004                           |
    | cloud         | kilo                                 |
    +---------------+--------------------------------------+


To view details of a particular floating ip address, use::

  $ cm network list floating ip 100.165.123.111
    +---------------+--------------------------------------+
    | name          | value                                |
    +---------------+--------------------------------------+
    | fixed_ip      | 10.0.2.10                            |
    | ip            | 100.165.123.111                      |
    | id            | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 |
    | instance_id   | a183b85f-2d4r-44b9-933f-64562380286f |
    | pool          | ext-net                              |
    | project       | fg478                                |
    | user          | albert                               |
    | instance_name | albert-004                           |
    | cloud         | kilo                                 |
    +---------------+--------------------------------------+


Create Floating IP Addresses
-----------------------------

To create a floating ip address under a floating pool, use::

  $ cm network create floating ip --pool=ext-net
    Created new floating IP [100.165.123.112]

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    |               | 100.165.123.112 | ext-net          |           | 2cd915a9-f191-762d-2456-24dcd2a0d97b |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+


Delete Floating IP Addresses
-----------------------------

To delete a floating ip address, use::

  $ cm network delete floating ip 100.165.123.112
    Floating IP [100.165.123.112] deleted successfully!

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+


Associate Floating IP Address with an Instance
-----------------------------------------------

To automatically generate a floating ip address
and associate it with an instance, use::

  $ cm network associate floating ip --instance=albert-009
    Created and assigned Floating IP [100.165.123.113] to instance [albert-009].

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    | albert-009    | 100.165.123.113 | ext-net          | 10.0.2.11 | 34fbeca5-aad3-4er5-ag21-34b8ac60dc85 | e433b85f-2d4r-44b9-933f-64562380285r |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+


Alternatively, you can also specify the floating ip address
that you want to associate with an instance::

  $ cm network associate floating ip --instance=albert-008 100.165.123.112
    Associated Floating IP [100.165.123.112] to instance [albert-008].

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    | albert-008    | 100.165.123.112 | ext-net          | 10.0.2.12 | c45beca5-cd34-4e3d-4r34-34b8ac64td42 | 2ds345f4-2d4r-44b9-933f-342432fd3fcc |
    | albert-009    | 100.165.123.113 | ext-net          | 10.0.2.11 | 34fbeca5-aad3-4er5-ag21-34b8ac60dc85 | e433b85f-2d4r-44b9-933f-64562380285r |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+


Disassociate Floating IP Address from an Instance
--------------------------------------------------

To automatically detect the floating ip address associated with an instance
& disassociate it from that instance, use::

  $ cm network disassociate floating ip --instance=albert-009
    Disassociated Floating IP [100.165.123.113] from instance [albert-009].

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    |               | 100.165.123.113 | ext-net          |           | 34fbeca5-aad3-4er5-ag21-34b8ac60dc85 |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    | albert-008    | 100.165.123.112 | ext-net          | 10.0.2.12 | c45beca5-cd34-4e3d-4r34-34b8ac64td42 | 2ds345f4-2d4r-44b9-933f-342432fd3fcc |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+

Alternatively, you could also specify the floating ip address to dissociate::

  $ cm network disassociate floating ip 100.165.123.113
    Disassociated Floating IP [100.165.123.113] from instance [albert-009].

  $ cm network list floating ip
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    | instance_name | floating_ip     | floating_ip_pool | fixed_ip  | floating_ip_id                       | instance_id                          |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+
    |               | 100.165.123.110 | ext-net          |           | 3e0915a9-f190-324d-8b56-4c2fd2a0d97b |                                      |
    |               | 100.165.123.113 | ext-net          |           | 34fbeca5-aad3-4er5-ag21-34b8ac60dc85 |                                      |
    | albert-004    | 100.165.123.111 | ext-net          | 10.0.2.10 | 58fbeca5-aad3-2f44-af23-0bb8ac60dc89 | a183b85f-2d4r-44b9-933f-64562380286f |
    | albert-008    | 100.165.123.112 | ext-net          | 10.0.2.12 | c45beca5-cd34-4e3d-4r34-34b8ac64td42 | 2ds345f4-2d4r-44b9-933f-342432fd3fcc |
    +---------------+-----------------+------------------+-----------+--------------------------------------+--------------------------------------+


.. note:: There are also a set of fixed-ip address operations you can perform,
          but you need to have admin privilidges in your account.

          Some of the commands include:

          Reserving a fixed ip address::

            $ cm network reserve fixed ip 10.1.1.3

          Unreserve a fixed ip address::

            $ cm network unreserve fixed ip 10.1.1.3

          Getting fixed ip address details::

            $ cm network get fixed ip 10.1.1.3

