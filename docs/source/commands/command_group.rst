Group Command
======================================================================

Manual
--------
The manual page of the group command can be found at: `group <../man/man.html#group>`_


Examples
--------

Group List
^^^^^^^^^^^^^

List the groups created in cloudmesh for a particular cloud::

  PS> cm group list --cloud general --format table
    +-----------+---------+---------+---------------------------------------------+------+
    | user      | cloud   | name    | value                                       | type |
    +-----------+---------+---------+---------------------------------------------+------+
    | goshenoy  | general | group01 | gourav-001,gourav-002                       | vm   |
    | goshenoy  | general | group03 | gourav-004,gourav-001,gourav-002,gourav-003 | vm   |
    | goshenoy  | general | group04 | gourav-001,gourav-002,gourav-003,gourav-004 | vm   |
    | goshenoy  | general | group05 | gourav-005                                  | vm   |
    +-----------+---------+---------+---------------------------------------------+------+

Group Info
^^^^^^^^^^^^^

Get details about a particular group with specific name::

  PS> cm group info group01
    +-----------+---------+---------+-----------------------+------+
    | user      | cloud   | name    | value                 | type |
    +-----------+---------+---------+-----------------------+------+
    | goshenoy  | general | group01 | gourav-001,gourav-002 | vm   |
    +-----------+---------+---------+-----------------------+------+

Group Add
^^^^^^^^^^^^^

Add a resource (VM) with specified id to a group with given name::

  PS> cm group add --id test-001 --type vm --name groupA
  Created a new group [groupA] and added ID [test-001] to it

  PS> cm group info groupA
    +-----------+---------+--------+----------+------+
    | user      | cloud   | name   | value    | type |
    +-----------+---------+--------+----------+------+
    | goshenoy  | general | groupA | test-001 | vm   |
    +-----------+---------+--------+----------+------+

Group Copy
^^^^^^^^^^^^^^

Copy the VM(s) from one group to another::

  PS> cm group copy groupA groupB
  Created a new group [groupB] and added ID [test-001] to it

  PS> cm group info groupB
    +-----------+---------+--------+----------+------+
    | user      | cloud   | name   | value    | type |
    +-----------+---------+--------+----------+------+
    | goshenoy  | general | groupB | test-001 | vm   |
    +-----------+---------+--------+----------+------+

Group Merge
^^^^^^^^^^^^^^

Merge two groups to form a third group::

  PS> cm group merge group01 groupB groupC
  Merge of group [group01] & [groupB] to group [groupC] successful!

  PS> cm group info groupC
    +-----------+---------+--------+--------------------------------+------+
    | user      | cloud   | name   | value                          | type |
    +-----------+---------+--------+--------------------------------+------+
    | goshenoy  | general | groupC | gourav-001,gourav-002,test-001 | vm   |
    +-----------+---------+--------+--------------------------------+------+

Group Delete
^^^^^^^^^^^^^^

Delete a group with a given name::

  PS> cm group delete --name groupC
  Deletion Successful!

  PS> cm group info groupC
  ERROR: No group with name groupC found in the cloudmesh database!