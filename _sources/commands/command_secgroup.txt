SecGroup Command
======================================================================

A security group is a named collection of network access rules
that are use to limit the types of traffic that have access to instances.
When you launch an instance, you can assign one or more security groups to it.
If you do not create security groups, new instances are automatically assigned to the default security group,
unless you explicitly specify a different security group.

The associated rules in each security group control the traffic to instances in the group.
Any incoming traffic that is not matched by a rule is denied access by default.
You can add rules to or remove rules from a security group,
and you can modify rules for the default and any other security group.

The manual page of the secgroup command can be found at: `secgroup
<../man/man.html#secgroup>`_


Security Group Create
----------------------

To create a security group in cloudmesh for a cloud and tenant use::

  $ cm secgroup create --cloud india --tenant fg478 test-group02
  Created a new security group [test-group02] with UUID [bd9cb15e-5fcf-11e5-85fd-d8eb97bdb464]

Security Group List
--------------------

To list Security Groups in cloudmesh for a cloud and tenant use::

  $ cm secgroup list --cloud india --tenant fg478
    +--------------------------------------+--------------------------------------+----------------------------------------------------+
    | Id                                   | Name                                 | Description                                        |
    +--------------------------------------+--------------------------------------+----------------------------------------------------+
    | 7ee21121-5fcc-11e5-8497-d8eb97bdb464 | albert-security_group-q5ukqwab4odq   | SSL(443), Web(5000), Celery-Flower(8888)           |
    | 4bc8bbb1-014d-4a84-a62c-f216d620c2bc | albert-security_group-r2qpv3kefysi   | SSL(443), Web(5000), Celery-Flower(8888)           |
    | 68c31654-7f5f-4944-a295-b9ff29a7e170 | albert-security_group-ayzancofltyf   | SSL(443), Web(5000), Celery-Flower(8888)           |
    +--------------------------------------+--------------------------------------+----------------------------------------------------+


Security Group Rule Add
------------------------

To add a new rule to the security group use::

  $ cm secgroup rules-add --cloud india --tenant fg478 test-group 80 80 tcp  0.0.0.0/0
    Added rule [80 | 80 | tcp | 0.0.0.0/0] to secgroup [test-group]

  $ cm secgroup rules-add --cloud india --tenant fg478 test-group 443 443 udp  0.0.0.0/0
    Added rule [443 | 443 | udp | 0.0.0.0/0] to secgroup [test-group]

Security Group Rules List
--------------------------

To list all the rules assigned to the security group use::

  $ cm secgroup rules-list --cloud india --tenant fg478 test-group
    +----------+-------+------------+----------+--------+----------+-----------+
    | user     | cloud | name       | fromPort | toPort | protocol | cidr      |
    +----------+-------+------------+----------+--------+----------+-----------+
    | albert   | india | test-group | 80       | 80     | tcp      | 0.0.0.0/0 |
    | albert   | india | test-group | 443      | 443    | udp      | 0.0.0.0/0 |
    +----------+-------+------------+----------+--------+----------+-----------+

Security Group Rule Delete
---------------------------

To delete a specific rule within a security group use::

  $ cm secgroup rules-delete --cloud india --tenant fg478 test-group 80 80 tcp 0.0.0.0/0
    Rule [80 | 80 | tcp | 0.0.0.0/0] deleted

  $ cm secgroup rules-list india fg478 test-group
    +----------+-------+--------------+----------+--------+----------+-----------+
    | user     | cloud | name         | fromPort | toPort | protocol | cidr      |
    +----------+-------+--------------+----------+--------+----------+-----------+
    | albert   | india | test-group   | 443      | 443    | udp      | 0.0.0.0/0 |
    +----------+-------+--------------+----------+--------+----------+-----------+

Security Group Delete
----------------------

To delete an entire security group use::

  $ cm secgroup delete --cloud india --tenant fg478 test-group
    Rule [443 | 443 | udp | 0.0.0.0/0] deleted
    Security Group [test-group] for cloud [india], & tenant [fg478] deleted

  $ cm secgroup rules-list --cloud india --tenant fg478 test-group
    ERROR: Security Group with label [test-group], cloud [india], & tenant [fg478] not found!
