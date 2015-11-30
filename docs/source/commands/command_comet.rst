Comet Command
======================================================================

The manual page of the group command can be found at: `default
<../man/man.html#default>`_

Cloudmesh has the ability to manage easily multiple clouds.
One of the key concepts to make the list of such clouds
easier is the introduction of defaults for each cloud or globally.
Hence it is possible to set default images, flavors for each cloud,
and also create the default cloud. The default command is used to
set and list the default values. These defaults are used in other
commands if they are not overwritten by a command parameter.

Upon start of cloudmesh, the default for cloud will be set to the first
cloud that is found in the yaml file and the default group is set to
`general`.

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

Conventions
------------


    Options::
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

    Arguments::
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
