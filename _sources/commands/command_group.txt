Group Command
======================================================================

One of cloudmesh major functionality is to group cloud and other
resources into a named group. Such named groups can than be used to
perform actions on them.

.. warning:: at this time we have limited to groups to just hold ID
	     of vms.

The manual page of the group command can be found at: `group
<../man/man.html#group>`_



Group List
^^^^^^^^^^^

The named groups can be lited with the following command::

  $ cm group list --cloud india --format table
    +----------+-------+--------+----------+------+
    | user     | cloud | name   | value    | type |
    +----------+-------+--------+----------+------+
    | albert   | india | groupA | test-001 | vm   |
    | albert   | india | groupA | test-002 | vm   |
    | albert   | india | groupA | test-004 | vm   |
    | albert   | india | groupB | test-003 | vm   |
    | albert   | india | groupB | test-005 | vm   |
    +----------+-------+--------+----------+------+

Group Info
^^^^^^^^^^^

To get details about a particular group with specific name you can use
the info option::

  $ cm group info groupA
    +----------+-------+--------+----------+------+
    | user     | cloud | name   | value    | type |
    +----------+-------+--------+----------+------+
    | albert   | india | groupA | test-001 | vm   |
    | albert   | india | groupA | test-002 | vm   |
    | albert   | india | groupA | test-004 | vm   |
    +----------+-------+--------+----------+------+

Group Remove ID
^^^^^^^^^^^^^^^^

To remove a VM from a particular group, you can use
the remove option::

  $ cm group remove --name groupA --id test-002
    Successfully removed ID [test-002] from the group [groupA]

  $ cm group info groupA
    +----------+-------+--------+----------+------+
    | user     | cloud | name   | value    | type |
    +----------+-------+--------+----------+------+
    | albert   | india | groupA | test-001 | vm   |
    | albert   | india | groupA | test-004 | vm   |
    +----------+-------+--------+----------+------+

Group Add
^^^^^^^^^^

To add a vm resource with specified id to a group with given name::

  $ cm group add --id test-001 --type vm --name groupA
  Created a new group [groupA] and added ID [test-001] to it

  $ cm group info groupA
    +-----------+---------+--------+----------+------+
    | user      | cloud   | name   | value    | type |
    +-----------+---------+--------+----------+------+
    | albert    | general | groupA | test-001 | vm   |
    +-----------+---------+--------+----------+------+

Group Copy
^^^^^^^^^^^

To copy the VM(s) from one group to another use the command::

  $ cm group copy groupA groupB
  Created a new group [groupB] and added ID [test-001] to it

  $ cm group info groupB
    +-----------+---------+--------+----------+------+
    | user      | cloud   | name   | value    | type |
    +-----------+---------+--------+----------+------+
    | albert    | general | groupB | test-001 | vm   |
    +-----------+---------+--------+----------+------+

Group Merge
^^^^^^^^^^^^

Groups can be merged as follows::

  $ cm group merge group01 groupB groupC
  Merge of group [group01] & [groupB] to group [groupC] successful!

  $ cm group info groupC
    +-----------+---------+--------+------------+------+
    | user      | cloud   | name   | value      | type |
    +-----------+---------+--------+------------+------+
    | albert    | general | groupC | albert-001 | vm   |
    | albert    | general | groupC | albert-002 | vm   |
    | albert    | general | groupC | test-001   | vm   |
    +-----------+---------+--------+------------+------+

Group Delete
^^^^^^^^^^^^^

A named group can be easily deleted.::

  $ cm group delete --name groupC
  Request to delete server albert-001 has been accepted.
  Request to delete server albert-002 has been accepted.
  Request to delete server test-001 has been accepted.
  Deletion Successful!

  $ cm group info groupC
  ERROR: No group with name groupC found in the cloudmesh database!

.. warning:: When a group is deleted, all the instances (vms) are deleted,
            and a deletion request is submitted to the appropriate cloud.
	  
