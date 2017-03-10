Info Command
======================================================================

The manual page of the `info` command can be found at: `info
<../man/man.html#info>`_

Cloudmesh has a number of important defaults. They are a subset of all
default commands and can be listed with the command `info. To view all
default values you can use the ` default list` command can be found at: `info
<../man/man.html#info>`_. Here is the info command in action:

.. prompt:: bash, cm>

    info

::
   
    +-------------+------------------+
    | Attribute   | Value            |
    +-------------+------------------+
    | cloud       | cm               |
    | key         | albert           |
    | user        | albert           |
    | vm          | albert-002       |
    | group       | default          |
    | secgroup    | albert-default   |
    | counter     | 3                |
    | image       | CC-CentOS7       |
    | flavor      | m1.small         |
    | refresh     | True             |
    | debug       | True             |
    | interactive | None             |
    | purge       | None             |
    +-------------+------------------+


 
+-------------+----------------------------------------------------------+
| *Attribute* | *Description*                                            |    
+-------------+----------------------------------------------------------+
| cloud       | the default cloud                                        |
+-------------+----------------------------------------------------------+
| key         | the defualt keyname as used in the clouds                |
+-------------+----------------------------------------------------------+
| user        | a default username as used to define vms                 |
+-------------+----------------------------------------------------------+
| vm          | the name of the last created vm                          |
+-------------+----------------------------------------------------------+
| group       | the default group                                        |
+-------------+----------------------------------------------------------+
| secgroup    | the default security group                               |
+-------------+----------------------------------------------------------+
| counter     | the index of the next vm                                 |
+-------------+----------------------------------------------------------+
| image       | name of the default image                                |
+-------------+----------------------------------------------------------+
| flavor      | name of the default flavor                               |
+-------------+----------------------------------------------------------+
| refresh     | should images, vms, flavore refreshed when invoking list |
+-------------+----------------------------------------------------------+
| debug       | set the debug mode                                       |
+-------------+----------------------------------------------------------+
| interactive | not used at this time                                    |
+-------------+----------------------------------------------------------+
| purge       | not used at this time                                    |
+-------------+----------------------------------------------------------+
