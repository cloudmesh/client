SecGroup Command
======================================================================

The manual page of the secgroup command can be found at: `secgroup <../man/man.html#secgroup>`_


Security Group Create
^^^^^^^^^^^^^^^^^^^^^^

Create a security group in cloudmesh for a cloud & tenant::

  PS> cm secgroup create --cloud india --tenant fg478 test-group02
  Created a new security group [test-group02] with UUID [bd9cb15e-5fcf-11e5-85fd-d8eb97bdb464]

Security Group List
^^^^^^^^^^^^^^^^^^^^

List Security Groups in cloudmesh for a cloud & tenant::

  PS> cm secgroup list --cloud india --tenant fg478
    +--------------------------------------+----------+-------+--------------+---------+
    | uuid                                 | user     | cloud | name         | project |
    +--------------------------------------+----------+-------+--------------+---------+
    | 7ee21121-5fcc-11e5-8497-d8eb97bdb464 | albert   | india | test-group   | fg478   |
    | bd9cb15e-5fcf-11e5-85fd-d8eb97bdb464 | albert   | india | test-group02 | fg478   |
    +--------------------------------------+----------+-------+--------------+---------+

Security Group Rule Add
^^^^^^^^^^^^^^^^^^^^^^^^

Adds a new rule to the security group::

  PS> cm secgroup rules-add --cloud india --tenant fg478 test-group 80 80 tcp  0.0.0.0/0
    Added rule [80 | 80 | tcp | 0.0.0.0/0] to secgroup [test-group]

  PS> cm secgroup rules-add --cloud india --tenant fg478 test-group 443 443 udp  0.0.0.0/0
    Added rule [443 | 443 | udp | 0.0.0.0/0] to secgroup [test-group]

Security Group Rules List
^^^^^^^^^^^^^^^^^^^^^^^^^^

Lists all the rules assigned to the security group::

  PS> cm secgroup rules-list --cloud india --tenant fg478 test-group
    +----------+-------+------------+----------+--------+----------+-----------+
    | user     | cloud | name       | fromPort | toPort | protocol | cidr      |
    +----------+-------+------------+----------+--------+----------+-----------+
    | albert   | india | test-group | 80       | 80     | tcp      | 0.0.0.0/0 |
    | albert   | india | test-group | 443      | 443    | udp      | 0.0.0.0/0 |
    +----------+-------+------------+----------+--------+----------+-----------+

Security Group Rule Delete
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Delete a specific rule within a security group::

  PS> cm secgroup rules-delete --cloud india --tenant fg478 test-group 80 80 tcp 0.0.0.0/0
    Rule [80 | 80 | tcp | 0.0.0.0/0] deleted

  PS> cm secgroup rules-list india fg478 test-group
    +----------+-------+--------------+----------+--------+----------+-----------+
    | user     | cloud | name         | fromPort | toPort | protocol | cidr      |
    +----------+-------+--------------+----------+--------+----------+-----------+
    | albert   | india | test-group   | 443      | 443    | udp      | 0.0.0.0/0 |
    +----------+-------+--------------+----------+--------+----------+-----------+

Security Group Delete
^^^^^^^^^^^^^^^^^^^^^^

Delete an entire security group::

  PS> cm secgroup delete --cloud india --tenant fg478 test-group
    Rule [443 | 443 | udp | 0.0.0.0/0] deleted
    Security Group [test-group] for cloud [india], & tenant [fg478] deleted

  PS> cm secgroup rules-list --cloud india --tenant fg478 test-group
    ERROR: Security Group with label [test-group], cloud [india], & tenant [fg478] not found!
