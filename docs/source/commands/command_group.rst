Group Command
======================================================================


The manual page of the group command can be found at: `group <../man/man.html#group>`_


Group List
^^^^^^^^^^^

List the groups created in cloudmesh for a particular cloud::

  $ cm group list --cloud general --format table
    +-----------+---------+---------+---------------------------------------------+------+
    | user      | cloud   | name    | value                                       | type |
    +-----------+---------+---------+---------------------------------------------+------+
    | albert    | general | group01 | albert-001,albert-002                       | vm   |
    | albert    | general | group03 | albert-004,albert-001,albert-002,albert-003 | vm   |
    | albert    | general | group04 | albert-001,albert-002,albert-003,albert-004 | vm   |
    | albert    | general | group05 | albert-005                                  | vm   |
    +-----------+---------+---------+---------------------------------------------+------+

Group Info
^^^^^^^^^^^

Get details about a particular group with specific name::

  $ cm group info group01
    +-----------+---------+---------+-----------------------+------+
    | user      | cloud   | name    | value                 | type |
    +-----------+---------+---------+-----------------------+------+
    | albert    | general | group01 | albert-001,albert-002 | vm   |
    +-----------+---------+---------+-----------------------+------+

Group Add
^^^^^^^^^^

Add a resource (VM) with specified id to a group with given name::

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

Copy the VM(s) from one group to another::

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

Merge two groups to form a third group::

  $ cm group merge group01 groupB groupC
  Merge of group [group01] & [groupB] to group [groupC] successful!

  $ cm group info groupC
    +-----------+---------+--------+--------------------------------+------+
    | user      | cloud   | name   | value                          | type |
    +-----------+---------+--------+--------------------------------+------+
    | albert    | general | groupC | albert-001,albert-002,test-001 | vm   |
    +-----------+---------+--------+--------------------------------+------+

Group Delete
^^^^^^^^^^^^^

Delete a group with a given name::

  $ cm group delete --name groupC
  Deletion Successful!

  $ cm group info groupC
  ERROR: No group with name groupC found in the cloudmesh database!
