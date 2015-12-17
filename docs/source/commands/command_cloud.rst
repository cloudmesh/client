Cloud Command
======================================================================

The cloud command provides an API that allows users to login to
a cloud, activate a cloud, deactivate a cloud & logout from a cloud.

The manual page of the network command can be found at: `cloud <../man/man.html#cloud>`



List status of all clouds
--------------------------

To list status of all clouds registered in the
cloudmesh.yaml file use::

  cm> cloud list
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | juno       | Logged Out |
    | kilo       | Logged Out |
    +------------+------------+


Login to a single/multiple clouds
----------------------------------

To logon to a cloud use::

  cm> cloud logon juno
    Logged into cloud: juno

You can logon to multiple clouds::

  cm> cloud logon kilo
    Logged into cloud: kilo

  cm> cloud list
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | juno       | Active     |
    | kilo       | Active     |
    +------------+------------+

Deactivate a cloud
-------------------

To deactivate a cloud use::

  cm> cloud deactivate kilo
    Deactivated cloud: kilo

  cm> cloud list
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | juno       | Active     |
    | kilo       | Inactive   |
    +------------+------------+

Activate a cloud
-----------------

To activate a cloud use::

  cm> cloud activate kilo
    Activated cloud: kilo

  cm> cloud list
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | juno       | Active     |
    | kilo       | Active     |
    +------------+------------+

Log out from a cloud
---------------------

To log out from a cloud use::

  cm> cloud logout juno
    Logged out of cloud: juno

  cm> cloud logout kilo
    Logged out of cloud: kilo

  cm> cloud list
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | juno       | Logged Out |
    | kilo       | Logged Out |
    +------------+------------+