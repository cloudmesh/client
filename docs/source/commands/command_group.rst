Group Command
======================================================================

Cloudmesh allows to group objects such as virtual machines
into a named group. Such groups can be used to
perform actions on them. Groups may contain objects from different
clouds. Most often groups are used to aggregate virtual machines in
groups and than manage these groups of virtual machines.
A  group named default is defined if no other group is specified.

The manual page of the group command can be found at:
`group <../man/man.html#group>`_


Group List
^^^^^^^^^^^

Named groups can be listed with the following command::

  $ cm group list
    +--------+----------+----------+----------+------+
    | name   | member   | user     | category | type |
    +--------+----------+----------+----------+------+
    | groupA | test-001 | albert   | kilo     | vm   |
    | groupA | test-002 | albert   | kilo     | vm   |
    | groupA | test-003 | albert   | kilo     | vm   |
    | groupB | test-004 | albert   | kilo     | vm   |
    | groupB | test-005 | albert   | kilo     | vm   |
    +--------+----------+----------+----------+------+


To get details about a particular group with specific name you can use
the info option::

  $ cm group list groupA
    +--------+----------+----------+----------+------+
    | name   | member   | user     | category | type |
    +--------+----------+----------+----------+------+
    | groupA | test-001 | albert   | kilo     | vm   |
    | groupA | test-002 | albert   | kilo     | vm   |
    | groupA | test-003 | albert   | kilo     | vm   |
    +--------+----------+----------+----------+------+

Group Remove Member
^^^^^^^^^^^^^^^^^^^^

To remove a member such as a VM from a particular group, you can use
the remove option::

  $ cm group remove test-002 --group=groupA
    Successfully removed ID [test-002] from the group [groupA]

  $ cm group list groupA
    +--------+----------+----------+----------+------+
    | name   | member   | user     | category | type |
    +--------+----------+----------+----------+------+
    | groupA | test-001 | albert   | kilo     | vm   |
    | groupA | test-003 | albert   | kilo     | vm   |
    +--------+----------+----------+----------+------+

Group Add
^^^^^^^^^^

To add a vm to a group use::

  $ cm group add test-002 --group=groupA
  Created a new group [groupA] and added ID [test-001] to it

  $ cm group list groupA
    +--------+----------+----------+----------+------+
    | name   | member   | user     | category | type |
    +--------+----------+----------+----------+------+
    | groupA | test-001 | albert   | kilo     | vm   |
    | groupA | test-002 | albert   | kilo     | vm   |
    | groupA | test-003 | albert   | kilo     | vm   |
    +--------+----------+----------+----------+------+

Group Copy
^^^^^^^^^^^

To copy a group use the command::

  $ cm group copy groupA groupB
  Created a new group [groupB] and added ID [test-001] to it

  $ cm group list groupC
    +--------+----------+----------+----------+------+
    | name   | member   | user     | category | type |
    +--------+----------+----------+----------+------+
    | groupC | test-001 | albert   | kilo     | vm   |
    | groupC | test-002 | albert   | kilo     | vm   |
    | groupC | test-003 | albert   | kilo     | vm   |
    +--------+----------+----------+----------+------+


Group Merge
^^^^^^^^^^^^

Groups can be merged as follows::

  $ cm group merge groupA groupB groupC
  Merge of group [group01] & [groupB] to group [groupC] ok.

  $ cm group list groupC
    +--------+----------+----------+----------+------+
    | name   | member   | user     | category | type |
    +--------+----------+----------+----------+------+
    | groupC | test-001 | albert   | kilo     | vm   |
    | groupC | test-002 | albert   | kilo     | vm   |
    | groupC | test-003 | albert   | kilo     | vm   |
    | groupC | test-004 | albert   | kilo     | vm   |
    | groupC | test-005 | albert   | kilo     | vm   |
    +--------+----------+----------+----------+------+

Group Delete
^^^^^^^^^^^^^

A named group can be easily deleted.::

  $ cm group delete groupC
  Deleting test-001.
  Deleting test-002.
  Deleting test-003.
  Deleting test-004.
  Deleting test-005.

  $ cm group list groupC
  ERROR: No group with name groupC found in the cloudmesh database!

.. warning:: When a group is deleted, all the instances (vms) are deleted,
            and a deletion request is submitted to the appropriate cloud.
	  
