Quota Command
======================================================================

The manual page of the quota command can be found at: `Quota <../man/man.html#quota>`_

quota list
^^^^^^^^^^^^^

Prints quota limit on a current project/tenant::

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

Another example with csv output::

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

