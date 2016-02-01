.. _comet_command:

Comet Command
======================================================================

The manual page of the group command can be found at:
`comet <../man/man.html#comet>`_

Cloudmesh has the ability to manage easily multiple clouds.
ONe such cloud is comet. comet cloud is special as it allows the management
of virtual clusters. It is intended for advanced users that can manage their
own cluster environment.


Configuration
--------------

Configure the comet section in ~/.cloudmesh/cloudmesh.yaml file first.
auth_provider could be userpass or apikey. When specified, the
corresponding credential is needed. Please communicate with comet
admins to get the username/password or api key and secret assigned.::

    comet:
        auth_provider: apikey
        userpass:
            username: TBD
            password: TBD
        apikey:
            api_key: KEYSTRING
            api_secret: SECRETSTRING


Reference Guide
----------------

Next, we include a small set of useful examples to manage comet
virtual cluster using cloudmesh client.

+-------------------------------------+-----------------------------------------------+
| Command                             | Description                                   |
+=====================================+===============================================+
| cm comet ll                         | | short list                                  |
+-------------------------------------+-----------------------------------------------+
| cm comet cluster                    | | List all clusters owned by the              |
|                                     | | authenticated identity (summarized format)  |
+-------------------------------------+-----------------------------------------------+
| cm comet cluster vc2                | | List a cluster by name                      |
+-------------------------------------+-----------------------------------------------+
| cm comet computeset                 | | List all defined compute sets               |
+-------------------------------------+-----------------------------------------------+
| cm comet computeset 63              | | List one compute set                        |
+-------------------------------------+-----------------------------------------------+
| cm comet power on vc4 vm-vc4-[0-3]  | | Power on a set of compute nodes in          |
|                                     | | cluster vc4                                 |
+-------------------------------------+-----------------------------------------------+
| cm comet power on vc4 vm-vc4-[7]    | | You can also power on one single node as a  |
|                                     | | compute set                                 |
+-------------------------------------+-----------------------------------------------+
| cm comet power on vc4               | | Power on the front end node of the          |
|                                     | | specified cluster                           |
+-------------------------------------+-----------------------------------------------+
| cm comet console vc4 vm-vc4-0       | | Get console of a running node               |
+-------------------------------------+-----------------------------------------------+
| cm comet console vc4                | | Get console of the front end                 |
+-------------------------------------+-----------------------------------------------+
| cm comet power off vc4 vm-vc4-[0-3] | | Power off a node or a set of nodes (if they | 
|                                     | | all belonging to one active compute set)    |
+-------------------------------------+-----------------------------------------------+

comet list
----------------------------------------------------------------------

All the current default values can by listed with --all option::

    $ comet ll
    +--------+-----------+-------+-------+
    | user   | cloud     | name  | value |
    +--------+-----------+-------+-------+
    | albert | chameleon | image | abc   |
    | albert | general   | cloud | azure |
    | albert | general   | image | zyx   |
    +--------+-----------+-------+-------+

You can also add a --cloud=CLOUD option to see the defaults set
for a cloud::

    $ comet list
    +--------+-----------+-------+-------+
    | user   | cloud     | name  | value |
    +--------+-----------+-------+-------+
    | albert | chameleon | image | abc   |
    +--------+-----------+-------+-------+

Options
------------

::

        --user=USER           user name
        --name=NAMES          Names of the vcluster
        --start=TIME_START    Start time of the vcluster, in
                              YYYY/MM/DD HH:MM:SS format.
                              [default: 1901-01-01]
        --end=TIME_END        End time of the vcluster, in YYYY/MM/DD
                              HH:MM:SS format. In addition a duratio
                              can be specified if the + sign is the
                              first sig The duration will than be
                              added to the start time.
                              [default: 2100-12-31]
        --project=PROJECT     project id
        --host=HOST           host name
        --description=DESCRIPTION  description summary of the vcluster
        --file=FILE           Adding multiple vclusters from one file
        --format=FORMAT       Format is either table, json, yaml,
                              csv, rest
                              [default: table]

Arguments
----------

::

        FILENAME  the file to open in the cwd if . is
                  specified. If file in in cwd
                  you must specify it with ./FILENAME

    Opens the given URL in a browser window.

comet tunnel
--------------

comet configuration
---------------------


comet logon
-------------


comet docs
------------

comet status
--------------

TBD

comet info
--------------

TBD::

       comet info [--user=USER]
                    [--project=PROJECT]
                    [--format=FORMAT]

comet_cluster
---------------

::

       comet cluster [ID][--name=NAMES]
                    [--user=USER]
                    [--project=PROJECT]
                    [--hosts=HOSTS]
                    [--start=TIME_START]
                    [--end=TIME_END]
                    [--hosts=HOSTS]
                    [--format=FORMAT]

comet computeset
--------------------

::

       comet computeset [COMPUTESETID]


comet start and stop
----------------------

::

       comet start ID

::

       comet stop ID


comet power
-------------------

::

       comet power (on|off|reboot|reset|shutdown) CLUSTERID PARAM

comet delete
-------------

::

       comet delete [all]
                      [--user=USER]
                      [--project=PROJECT]
                      [--name=NAMES]
                      [--hosts=HOSTS]
                      [--start=TIME_START]
                      [--end=TIME_END]
                      [--host=HOST]
       comet delete --file=FILE


comet update
-------------

::

       comet update [--name=NAMES]
                      [--hosts=HOSTS]
                      [--start=TIME_START]
                      [--end=TIME_END]

comet add
-----------

::

       comet add [--user=USER]
                   [--project=PROJECT]
                   [--host=HOST]
                   [--description=DESCRIPTION]
                   [--start=TIME_START]
                   [--end=TIME_END]
                   NAME
       comet add --file=FILENAME
