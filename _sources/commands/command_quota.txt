Quota Command
======================================================================

The manual page of the quota command can be found at: `Quota
<../man/man.html#quota>`_

Many clouds have some kind of quota limitations on how many ip
addresses one can obtain, or how many cores a user can have. To get an
overview of the quotas set for a user in a project we are providing a
quota command.

quota list
----------------------------------------------------------------------

To list the quota limit on a default project/tenant you can use::

  $ cm quota list
    +-----------------------------+-------+
    | Quota                       | Limit |
    +-----------------------------+-------+
    | fixed_ips                   | -1    |
    | floating_ips                | 10    |
    | instances                   | 10    |
    | security_groups             | 10    |
    | server_group_members        | 10    |
    | server_groups               | 10    |
    | key_pairs                   | 100   |
    | injected_file_content_bytes | 10240 |
    | metadata_items              | 128   |
    | cores                       | 20    |
    | security_group_rules        | 20    |
    | injected_file_path_bytes    | 255   |
    | injected_files              | 5     |
    | ram                         | 51200 |
    +-----------------------------+-------+

To export it in csv format, please use and specifically apply it to
the cloud india::

    $ cm quota list --cloud=india --format=csv
    Quota,Limit
    instances,10
    cores,20
    ram,51200
    floating_ips,10
    fixed_ips,-1
    metadata_items,128
    injected_files,5
    injected_file_content_bytes,10240
    injected_file_path_bytes,255
    key_pairs,100
    security_groups,10
    security_group_rules,20
    server_groups,10
    server_group_members,10

