Quick Start Amazon EC2
===============================================================================

Starting an AWS EC2 instance is easy on Cloudmesh client with a few steps. This
instruction guides you how to register AWS account on Cloudmesh client and
get access to a machine once it's running. It may take 5 minutes.

.. note:: If you need to install cloudmesh client, please visit :ref:`Quick
        Start <ref-quickstart>` guide.

This instruction contains:

- AWS Access Key & Secret Key Registration
- SSH Key Upload
- EC2 Linux Instance Start
- SSH Login
- Instance Termination

Other functionalities and features will be discussed in the following AWS section.

AWS Account Registration
-------------------------------------------------------------------------------

AWS Access Key ID and Secret Access Key can be obtained from `AWS Management
Console <https://console.aws.amazon.com/>`_.

- Login AWS Account at https://aws.amazon.com
- Find Security Credentials
- Continue to Security Credentials
- Choose 'Access Keys (Access Key ID and Secret Access Key)'
- Create New Access Key
- 20 bytes of Access Key ID
- 40 bytes of Secret Access Key ID
- Keep these two Key IDs to register on Cloudmesh client
- Run ``cm`` command to open Cloudmesh shell
- Run ``register aws`` to type account information

  ::

          cm> register aws

          # ######################################################################
          # Register aws
          # ######################################################################
          Enter EC2_ACCESS_KEY (TBD):
          Enter EC2_SECRET_KEY (TBD):
          Enter keyname (TBD):
          Enter userid (TBD):

You can update keyname and userid later, so please ignore at this time.

Set Default Cloud
-------------------------------------------------------------------------------

You may want to set AWS as a default cloud before you start using Amazon
cloud. Default cloud setting allows you to run your Cloudmesh commands towards
a selected cloud, in this case AWS, without additional parameters e.g.
``--cloud=``.  You can change default settings anytime while you are in
Cloudmesh shell.

- Run ``default cloud=aws``
  ::

    cm> default cloud=aws
    set default cloud=aws. ok.

Key Registration
-------------------------------------------------------------------------------

To confirm that your account is registered successfully in Cloudmesh, you may
want to upload your ssh key to your Amazon EC2 account.

- Check available keys in database by ``key list``
  ::

        +-------+------------------+-------------------------------------+------------------------------------------+--------+
        | name  | comment          | uri                                 | fingerprint                              | source |
        +-------+------------------+-------------------------------------+------------------------------------------+--------+
        | albert| ubuntu@cloudmesh | file:///home/ubuntu/.ssh/id_rsa.pub | f2:da:38:54:3c:84:e3:16:e8:75:22:ce:9c:f | ssh    |
        |       |                  |                                     | e:4e:7f                                  |        |
        +-------+------------------+-------------------------------------+------------------------------------------+--------+

- Run ``key upload``, to simply register your key to AWS
  ::

        cm> key upload
        upload key albert -> aws
        Adding key albert to cloud aws
        INFO: Initializing libcloud-ec2 for aws
        INFO: AWS INIT
        INFO: Uploading the key to libcloud. ok.

- Set your key as your default key by ``default key=albert``::

        cm> default key=albert
        set default key=albert. ok.

- ``key list --cloud=aws`` provides a list of registered SSH keys on your EC2
  account like::

.. include:: aws-keys.rst

Authentication Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your AWS account is invalid or registered incorrectly, you may encounter
authentication errors like::

        ERROR: problem uploading key albert to cloud aws:
        SignatureDoesNotMatch: The request signature we calculated does not
        match the signature you provided. Check your AWS Secret Access Key and
        signing method. Consult the service documentation for details.

Please make sure your Access Key ID and Secret Key ID are recorded in Cloudmesh
correctly. (Try ``register aws`` command again to confirm your input)
Also your IDs should be **active** on AWS Management Console.

Duplication Error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unique SSH key name is required on EC2, otherwise key upload will fail with
'InvalidKeyPair.Duplicate' error like::

    ERROR: problem uploading key albert to cloud aws: InvalidKeyPair.Duplicate:
    The keypair 'albert' already exists.

Starting EC2 Instance
-------------------------------------------------------------------------------

``vm boot`` starts a new EC2 instance under your account with default settings.

::

   cm> vm boot
   INFO: Initializing libcloud-ec2 for aws
   INFO: AWS INIT
   Machine TBD-001 is being booted on cloud aws ...
   +-----------+---------------------+
   | Attribute | Value               |
   +-----------+---------------------+
   | cloud     | aws                 |
   | flavor    | t1.micro            |
   | image     | ami-d85e75b0        |
   | key       | albert              |
   | meta      | +                   |
   |   -       | category: aws       |
   |   -       | kind: cloudmesh     |
   |   -       | group: default      |
   |   -       | image: ami-d85e75b0 |
   |   -       | key: albert         |
   |   -       | flavor: t1.micro    |
   | name      | TBD-001             |
   | nics      |                     |
   | secgroup  | +                   |
   |   -       | TBD-default         |
   +-----------+---------------------+
   ...

Your first VM ``TBD-001`` started on AWS with default settings which are t1.micro (upto 2 EC2 compute units) flavor and ami-d85e75b0 (Ubuntu 14.04.2 LTS). Your ssh key (albert) is injected in the VM.

List of running EC2 Instances
-------------------------------------------------------------------------------

Simple ``vm list`` run provides a list of running VM instances including one
that you started above. For example::

  cm> vm list
  Listing VMs on Cloud: aws
  INFO: Initializing libcloud-ec2 for aws
  INFO: AWS INIT
  INFO: Initializing libcloud-ec2 for aws
  INFO: AWS INIT
  +----+------------+---------+------------+----------------+---------------+------------+-------+--------------+---------------+------+----------+---------------------+
  | id | uuid       | label   | status     | public_ips     | private_ips   | image_name | key   | availability | instance_type | user | category | updated_at          |
  +----+------------+---------+------------+----------------+---------------+------------+-------+--------------+---------------+------+----------+---------------------+
  |    | i-46e521d9 | TBD-001 | pending    | 54.158.117.249 | 10.235.175.78 |            | albert| us-east-1e   | t1.micro      | TBD  | aws      | 2016-07-16 01:19:55 |
  +----+------------+---------+------------+----------------+---------------+------------+-------+--------------+---------------+------+----------+---------------------+


``vm refresh`` command updates status of VMs.

.. note:: ``InvalidCredsError`` may appear if account information is invalid.
   For example, ``InvalidCredsError: 'SignatureDoesNotMatch: The request
   signature we calculated does not match the signature you provided. Check
   your AWS Secret Access Key and signing method. Consult the service
   documentation for details.'`` To fix this, confirm that your Access Key ID
   and Secret Key ID are correct on Cloudmesh ``register aws`` and your Keys
   are **active** on AWS Management Console.

SSH to EC2 Instance
-------------------------------------------------------------------------------

Once your EC2 Instance is up and running, you are able to get access to the
machine vis SSH.  In Cloudmesh, you run ``vm ssh <VM Name>`` to connect. For
example, run ``vm ssh TBD-001 --username=ubuntu`` with ``ubuntu`` username to get into Ubuntu VM instance.

:: 

  cm> vm ssh TBD-001 --username=ubuntu
  login aws:ubuntu@TBD-001
  +-------------+---------+
  | Attribute   | Value   |
  +-------------+---------+
  | cloud       | aws     |
  | command     |         |
  | floating_ip |         |
  | key         | albert  |
  | name        | TBD-001 |
  | username    | ubuntu  |
  +-------------+---------+
  INFO: Initializing libcloud-ec2 for aws
  INFO: AWS INIT
  Determining IP Address to use with a ping test.
  Checking 54.158.117.249...
  IP to be used is: 54.158.117.249
  INFO: Creating and adding security group for libcloud
  INFO: Initializing libcloud-ec2 for aws
  INFO: AWS INIT
  INFO: create_sec_group exception.InvalidGroup.Reserved: The 'default' security group is reserved, and cannot be deleted by a user. If creating a security group, specify a different name.
  INFO: Connecting to Instance at IP:54.158.117.249
  Welcome to Ubuntu 14.04.2 LTS (GNU/Linux 3.13.0-48-generic x86_64)

   * Documentation:  https://help.ubuntu.com/

     System information as of Sat Jul 16 01:41:51 UTC 2016

     System load: 0.52             Memory usage: 7%   Processes:       48
     Usage of /:  9.7% of 7.75GB   Swap usage:   0%   Users logged in: 0

     Graph this data and manage this system at:
       https://landscape.canonical.com/

     Get cloud support with Ubuntu Advantage Cloud Guest:
       http://www.ubuntu.com/business/services/cloud

     0 packages can be updated.
     0 updates are security updates.

     The programs included with the Ubuntu system are free software;
     the exact distribution terms for each program are described in the
     individual files in /usr/share/doc/*/copyright.

     Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
     applicable law.

     ubuntu@ip-10-235-175-78:~$

Congrats! you have launched an EC2 instance on Cloudmesh and it's ready to use.

Terminating EC2 Instance
-------------------------------------------------------------------------------

``vm delete`` terminates EC2 Instance like::

        cm> vm delete TBD-001
        INFO: Initializing libcloud-ec2 for aws
        INFO: AWS INIT
        'Delete VM for TBD-001'
        INFO: VM delete success.ok.
        VM record TBD-001 is being deleted from the local database...

That's all. Simply provide VM instance name to terminate.

List of Server Sizes (flavors)
-------------------------------------------------------------------------------

The server sizes that EC2 provides can be listed by ``flavor list``
Amazon EC2 provide more than 40 flavors like::

.. include:: aws-flavor.rst


``image list`` provides 30,000+ images available on EC2 and it takes several
minutes to display.

Other Commands
-------------------------------------------------------------------------------

For example, managing Security Groups will be discussed in the next AWS
section.

Notes
-------------------------------------------------------------------------------

AWS EC2 is implemented with `Apache Libcloud
<https://libcloud.readthedocs.io/en/latest/compute/drivers/ec2.html>`_ in
Cloudmesh.

