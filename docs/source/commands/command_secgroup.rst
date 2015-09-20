SecGroup Command
======================================================================

Manual
--------
The manual page of the secgroup command can be found at: `secgroup <../man/man.html#secgroup>`_


Examples
--------

Security Group Create
^^^^^^^^^^^^^

Create a security group in cloudmesh for a cloud & tenant::

  PS> cm secgroup create india fg478 test-group02
  Created a new security group [test-group02] with UUID [bd9cb15e-5fcf-11e5-85fd-d8eb97bdb464]

Security Group List
^^^^^^^^^^^^^

List Security Groups in cloudmesh for a cloud & tenant::

  PS> cm secgroup list india fg478
    +--------------------------------------+----------+-------+--------------+---------+
    | uuid                                 | user     | cloud | name         | project |
    +--------------------------------------+----------+-------+--------------+---------+
    | 7ee21121-5fcc-11e5-8497-d8eb97bdb464 | goshenoy | india | test-group   | fg478   |
    | bd9cb15e-5fcf-11e5-85fd-d8eb97bdb464 | goshenoy | india | test-group02 | fg478   |
    +--------------------------------------+----------+-------+--------------+---------+

Security Group Rule Add
^^^^^^^^^^^^^

Adds a new rule to the security group::

  PS> cm secgroup rules-add india fg478 test-group 80 80 tcp  0.0.0.0/0
    Added rule [80 | 80 | tcp | 0.0.0.0/0] to secgroup [test-group]

  PS> cm secgroup rules-add india fg478 test-group 443 443 udp  0.0.0.0/0
    Added rule [443 | 443 | udp | 0.0.0.0/0] to secgroup [test-group]

Security Group Rules List
^^^^^^^^^^^^^

Lists all the rules assigned to the security group::

  PS> cm secgroup rules-list india fg478 test-group
    +----------+-------+------------+----------+--------+----------+-----------+
    | user     | cloud | name       | fromPort | toPort | protocol | cidr      |
    +----------+-------+------------+----------+--------+----------+-----------+
    | goshenoy | india | test-group | 80       | 80     | tcp      | 0.0.0.0/0 |
    | goshenoy | india | test-group | 443      | 443    | udp      | 0.0.0.0/0 |
    +----------+-------+------------+----------+--------+----------+-----------+
