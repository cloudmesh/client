Flavor Command
======================================================================

The manual page of the flavor command can be found at: `Flavor
<../man/man.html#flavor>`_

Flavors define the compute, memory, and storage capacity of nova computing instances.
To put it simply, a flavor is an available hardware configuration for a server. It
defines the “size” of a virtual server that can be launched

Refresh
----------------------------------------------------------------------

The refresh command would update the local database with the latest flavors.
To refresh flavors of a cloud, do the following::

    $cm flavor refresh --cloud=juno
    Refresh flavor for cloud juno. ok

List
----------------------------------------------------------------------

To list the set of flavors of a cloud, do the following::

    $cm flavor list --cloud=juno
    +----+----------------+--------+-------+----------+-------+------+--------+-------------+-----------------+------+-------+------+
    | Id | Name           | User   | RAM   | Disabled | vCPUs | Swap | Access | rxtx_factor | os_flv_ext_data | Disk | Cloud | UUID |
    +----+----------------+--------+-------+----------+-------+------+--------+-------------+-----------------+------+-------+------+
    | 1  | m1.tiny        | albert | 512   | 0        | 1     |      | 1      | 1.0         | 0               | 0    | juno  | 1    |
    | 5  | m1.xlarge      | albert | 16384 | 0        | 8     |      | 1      | 1.0         | 0               | 160  | juno  | 5    |
    | 9  | m1.xlarge_e200 | albert | 16384 | 0        | 8     |      | 1      | 1.0         | 200             | 160  | juno  | 9    |
    | 2  | m1.small       | albert | 2048  | 0        | 1     |      | 1      | 1.0         | 0               | 20   | juno  | 2    |
    | 6  | m1.small_e30   | albert | 2048  | 0        | 1     |      | 1      | 1.0         | 30              | 20   | juno  | 6    |
    | 3  | m1.medium      | albert | 4096  | 0        | 2     |      | 1      | 1.0         | 0               | 40   | juno  | 3    |
    | 7  | m1.medium_e60  | albert | 4096  | 0        | 2     |      | 1      | 1.0         | 60              | 40   | juno  | 7    |
    | 4  | m1.large       | albert | 8192  | 0        | 4     |      | 1      | 1.0         | 0               | 80   | juno  | 4    |
    | 8  | m1.large_e100  | albert | 8192  | 0        | 4     |      | 1      | 1.0         | 100             | 80   | juno  | 8    |
    +----+----------------+--------+-------+----------+-------+------+--------+-------------+-----------------+------+-------+------+

List Details
----------------------------------------------------------------------

To list the details of a flavor, give in the id, uuid or name of the flavor. In case latest information is needed,
the --refresh option can be used which would update the local database::

    $cm flavor list 1 --cloud=juno
    +-----------------+---------------------+
    | Attribute       | Value               |
    +-----------------+---------------------+
    | id              | 1                   |
    | swap            |                     |
    | os_flv_disabled | 0                   |
    | os_flv_ext_data | 0                   |
    | disk            | 0                   |
    | os_flavor_acces | 1                   |
    | vcpus           | 1                   |
    | uuid            | 1                   |
    | rxtx_factor     | 1.0                 |
    | created_at      | 2015-11-11 13:38:31 |
    | updated_at      | 2015-11-11 13:38:31 |
    | ram             | 512                 |
    | user            | albert               |
    | kind            | flavor              |
    | cloud           | juno                |
    | name            | m1.tiny             |
    | label           | m1.tiny             |
    | project         | undefined           |
    +-----------------+---------------------+


