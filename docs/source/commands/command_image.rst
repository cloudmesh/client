Image Command
======================================================================

The manual page of the image command can be found at: `Image
<../man/man.html#image>`_

An image is a collection of files used to create or rebuild a server

Refresh
----------------------------------------------------------------------

The refresh command would update the local database with the latest images.
To refresh images of a cloud(in this example, juno), do the following::

    $cm image refresh --cloud=juno
    Refresh image for cloud juno. ok.

List
----------------------------------------------------------------------

To list the set of images of a cloud, do the following::

    $cm image list --cloud=juno
    +----+---------------+----------------------+------------------------------+---------+--------+-----------------------------------------+----------+--------+----------------------+
    | id | size          | created              | description                  | minDisk | minRam | name                                    | progress | status | updated              |
    +----+---------------+----------------------+------------------------------+---------+--------+-----------------------------------------+----------+--------+----------------------+
    | 1  | 158443520     | 2015-03-23T20:50:29Z |                              | 0       | 0      | XXX                                     | 100      | ACTIVE | 2015-03-23T20:50:33Z |
    | 2  | 1270546432    | 2015-03-26T18:15:47Z |                              | 20      | 0      | YYY                                     | 100      | ACTIVE | 2015-03-26T18:17:41Z |
    | 3  | 4845404160    | 2015-03-26T20:05:29Z |                              | 40      | 0      | mooc-backup                             | 100      | ACTIVE | 2015-03-27T20:57:02Z |
    +----+---------------+----------------------+------------------------------+---------+--------+-----------------------------------------+----------+--------+----------------------+

List Details
----------------------------------------------------------------------

To list the details of an image, give in the id, uuid or name of the image. In case latest information is needed,
the --refresh option can be used which would update the local database::


    $cm image list 12 --cloud=juno
    +--------------------------------------+--------------------------------------+
    | Attribute                            | Value                                |
    +--------------------------------------+--------------------------------------+
    | metadata__ramdisk_id                 | None                                 |
    | metadata__description                | None                                 |
    | metadata__kernel_id                  | None                                 |
    | id                                   | 12                                   |
    | metadata__instance_type_ephemeral_gb | 0                                    |
    | minRam                               | 0                                    |
    | metadata__instance_type_swap         | 0                                    |
    | metadata__instance_type_vcpus        | 1                                    |
    | metadata__instance_type_rxtx_factor  | 1.0                                  |
    | progress                             | 100                                  |
    | os_image_size                        | 1977483264                           |
    | metadata__instance_type_flavorid     | 2                                    |
    | metadata__instance_type_root_gb      | 20                                   |
    | minDisk                              | 20                                   |
    | created                              | 2015-05-23T20:45:51Z                 |
    | updated                              | 2015-05-23T20:51:12Z                 |
    | updated_at                           | 2015-11-11 00:29:55                  |
    | created_at                           | 2015-11-11 00:29:55                  |
    | metadata__instance_type_memory_mb    | 2048                                 |
    | metadata__instance_type_id           | 5                                    |
    | metadata__base_image_ref             | 6a6a3474-8194-44ac-9f56-70cb93207f21 |
    | status                               | ACTIVE                               |
    | metadata__network_allocated          | True                                 |
    | uuid                                 | a59833a2-60c9-47f0-b333-4e0bc071ac3a |
    | metadata__image_state                | available                            |
    | metadata__user_id                    | b13b62690e984c7586df1cdd2df07b5f     |
    | metadata__owner_id                   | c713809dee494dccac34fcd02e012acb     |
    | user                                 | albert                               |
    | metadata__instance_uuid              | f01633b1-76b0-47b5-915e-eaae4559ba60 |
    | label                                | ZZZ                                  |
    | name                                 | ZZZ                                  |
    | kind                                 | image                                |
    | cloud                                | juno                                 |
    | metadata__instance_type_name         | m1.small                             |
    | metadata__image_location             | snapshot                             |
    | metadata__image_type                 | snapshot                             |
    | project                              | undefined                            |
    +--------------------------------------+--------------------------------------+


