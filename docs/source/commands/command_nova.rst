Nova Command
======================================================================

This is a wrapper nova command provided by cloudmesh which in turn calls the
openstack nova command on the target cloud. This also provides you with the
capability of setting the target cloud. However, we recommend not using
the command and instead use the cloudmesh command sas they allow for
information caching

The manual page of the key command can be found at: `Nova <../man/man.html#nova>`_


Setting the Target Cloud
----------------------------------------------------------------------

You may set the target cloud on which the nova command should run as follows::

    $ cm nova set india
    india is set

Note that if you do not set a target cloud, default cloud considered is 'india'.

Getting the Cloud Info
----------------------------------------------------------------------

You may get the cloud info in the following manner::

    $ cm nova info
    WARNING: OS environment variable OS_REGION not found
    +----------------+--------------------------------------------------------+
    | Variable       | Value                                                  |
    +----------------+--------------------------------------------------------+
    | OS_REGION      | None                                                   |
    | OS_USERNAME    | albert                                                 |
    | OS_CACERT      | /home/albert/.cloudmesh/clouds/india/kilo/cacert.pem   |
    | OS_TENANT_NAME | fg478                                                  |
    | OS_AUTH_URL    | https://i5r.idp.iu.futuregrid.org:5000/v2.0            |
    | OS_PASSWORD    | ********                                               |
    +----------------+--------------------------------------------------------+

By default it gives the 'india' cloud info. To check for specific cloud, here is an example for kilo cloud::

    $ cm nova info kilo
    +----------------+------------------------------------------------+
    | Variable       | Value                                          |
    +----------------+------------------------------------------------+
    | OS_REGION      | None                                           |
    | OS_USERNAME    | TBD                                            |
    | OS_CACERT      | TBD                                            |
    | OS_TENANT_NAME | TBD                                            |
    | OS_AUTH_URL    | https://i5r.idp.iu.futuresystems.org:5000/v2.0 |
    | OS_PASSWORD    | ********                                       |
    +----------------+------------------------------------------------+

Running openstack nova commands
----------------------------------------------------------------------

The syntax is  the same as what is used for openstack nova.
Following are couple of examples::

Listing images::

    $ cm nova image-list
    Cloud = india
    +--------------------------------------+-----------------------------------------+--------+--------------------------------------+
    | ID                                   | Name                                    | Status | Server                               |
    +--------------------------------------+-----------------------------------------+--------+--------------------------------------+
    | 619b8942-2355-4aa2-bae3-74b8f1751911 | CentOS-7                                | ACTIVE |                                      |
    | f63a996c-ea69-4a56-830e-c190bca2f828 | VM with Cloudmesh Configured Completely | ACTIVE | 8b7ce3bf-f797-4e8e-903c-6a0de81b063c |
    | 7ddc3366-73bf-453a-a813-43514030bf2e | badi/centos-7-2015-06-01                | ACTIVE |                                      |
    | c3c5b676-be53-4237-a40f-451d4c6e572e | badi/ubuntu-14.04-2015-06-01            | ACTIVE |                                      |
    | f2c2bbda-8bc1-4f02-a2e8-60014da66689 | cloudmesh/ipynb-n-java                  | ACTIVE |                                      |
    | 186592ce-eed5-4631-bc0c-7022eccd8508 | fg464/hadoop-b649                       | ACTIVE | 63a2cf03-a6cf-4d8a-95c1-250eb71f1ebc |
    | 364bd53b-87d3-4ac6-8e41-af540301f0cd | futuresystems/centos-7                  | ACTIVE |                                      |
    | 58e5d678-79ec-4a4d-9aa8-37975b7f40ac | futuresystems/fedora-21                 | ACTIVE |                                      |
    | a59833a2-60c9-47f0-b333-4e0bc071ac3a | futuresystems/hadoop-v2                 | ACTIVE | f01633b1-76b0-47b5-915e-eaae4559ba60 |
    | 367de5c7-3a30-4bad-b316-1a2afa17d794 | futuresystems/ubuntu-12.04              | ACTIVE |                                      |
    | 66708636-5ed6-4908-b36a-f5a69f8ac7ee | futuresystems/ubuntu-14.04              | ACTIVE |                                      |
    | 0f787e59-6ff9-466c-aaf6-cd3f3c9350d0 | kilitbilgi/ubuntu_14_10_desktop         | ACTIVE |                                      |
    | 5337a50d-4418-4c1f-9741-5c31bf03e267 | lee212/CoreOS                           | ACTIVE |                                      |
    | 132c961f-bca8-4942-a2c5-a8f60f84aea9 | lee212/CoreOS-Alpha                     | ACTIVE |                                      |
    | e8acb8e0-fbc9-44e4-9b31-3c38fc9c25ae | lee212/boot2docker                      | ACTIVE |                                      |
    | b073ddce-747d-4c66-8152-70118a4e5781 | mooc-backup                             | ACTIVE | 805da4cb-a14f-4465-841f-124346cf3bde |
    | 85fdb68e-8bd3-4e5e-bb4e-f286298f4fe6 | said/ubuntu15                           | ACTIVE |                                      |
    | e3d5fcf5-1b40-48df-9098-3c03a682421e | slaves_ubuntu_14_04                     | ACTIVE |                                      |
    | 58c9552c-8d93-42c0-9dea-5f48d90a3188 | ubuntu12-cometworker1                   | ACTIVE | 55458942-1d8f-4a54-af10-8e01c47953ea |
    +--------------------------------------+-----------------------------------------+--------+--------------------------------------+

Listing flavors::

    $ cm nova flavor-list
    Cloud = india
    +----+----------------+-----------+------+-----------+------+-------+-------------+-----------+
    | ID | Name           | Memory_MB | Disk | Ephemeral | Swap | VCPUs | RXTX_Factor | Is_Public |
    +----+----------------+-----------+------+-----------+------+-------+-------------+-----------+
    | 1  | m1.tiny        | 512       | 0    | 0         |      | 1     | 1.0         | True      |
    | 2  | m1.small       | 2048      | 20   | 0         |      | 1     | 1.0         | True      |
    | 3  | m1.medium      | 4096      | 40   | 0         |      | 2     | 1.0         | True      |
    | 4  | m1.large       | 8192      | 80   | 0         |      | 4     | 1.0         | True      |
    | 5  | m1.xlarge      | 16384     | 160  | 0         |      | 8     | 1.0         | True      |
    | 6  | m1.small_e30   | 2048      | 20   | 30        |      | 1     | 1.0         | True      |
    | 7  | m1.medium_e60  | 4096      | 40   | 60        |      | 2     | 1.0         | True      |
    | 8  | m1.large_e100  | 8192      | 80   | 100       |      | 4     | 1.0         | True      |
    | 9  | m1.xlarge_e200 | 16384     | 160  | 200       |      | 8     | 1.0         | True      |
    +----+----------------+-----------+------+-----------+------+-------+-------------+-----------+

Following is the link for openstack nova command manual:-

`Openstack nova command manual <http://docs.openstack.org/cli-reference/content/novaclient_commands.html>`_
