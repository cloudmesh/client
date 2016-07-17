Quick Start Microsoft Azure
===============================================================================

Starting an Microsoft Azure Virtual Machine is simple on Cloudmesh client with
a few steps. This instruction guides you how to register Azure account on
Cloudmesh client and get access to a machine once it's running. It may take 10 
minutes.

.. note:: If you need to install cloudmesh client, please visit :ref:`Quick
        Start <ref-quickstart>` guide.

This instruction contains:

- Azure Subscription ID Registration
- Azure management certificate
- Linux Instance Start
- SSH Login with Username and Password
- Instance Termination

Other functionalities and features will be discussed in the following Azure
section.

Azure Account Registration
-------------------------------------------------------------------------------

Microsoft Azure provides authentication via management certificates (X.509 v3)
along with a subscription ID. To obtain a subscription ID,

- Login `the classic Azure Portal <https://manage.windowsazure.com>`_
- Find 'Settings' at the bottome of the left tab
- You will find a subscription ID associated with your account in the
  'settings' page like:
  ``8b3df2b9-3ac1-4828-b6e0-8f8be62e6e6r``
- Keep the subscription ID when you register Azure cloud on Cloudmesh

Certificate by OpenSSL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next step, you need to create certificate files for the server (.cer) and for
the client (.pem). Follow the instructions below:

- Run ``openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout
  ~/.cloudmesh/azure-cert.pem -out ~/.cloudmesh/azure-cert.pem``

  To create a self-assigned certificiate, you provide your information
  interactively like::

    Generating a 2048 bit RSA private key
    ..........+++
    ........................+++
    writing new private key to 'azure-cert.pem'
    -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]: US
    State or Province Name (full name) [Some-State]: Indiana
    Locality Name (eg, city) []: Bloomington
    Organization Name (eg, company) [Internet Widgits Pty Ltd]: Indiana University
    Organizational Unit Name (eg, section) []:
    Common Name (e.g. server FQDN or YOUR name) []: Cloudmesh
    Email Address []:

You will find ``~/.cloudmesh/azure-cert.pem`` file on your account. Let's
create server certificate (.cer) from the client certificate (.pem).

- Run ``openssl x509 -inform pem -in ~/.cloudmesh/azure-cert.pem -outform der
  -out ~/.cloudmesh/azure-cert.cer``

Now you have ``azure-cert.pem`` and ``azure-cert.cer`` files in your
``~/.cloudmesh`` directory.

Upload Certificate to Azure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To authenticate Azure Services with your ``.pem`` file on Cloudmesh, you need
to upload your ``.cer`` certificate to Azure.

- Find ``Settings`` page at the bottom of the left tab in `the classic Azure Portal <https://manage.windowsazure.com/>`_
- Find ``Management Certificates`` tab on the top of the ``Settings`` page.
- Click ``Upload`` button at the bottom of the page to upload your ``.cer`` file, in this case ``~/.cloudmesh/azure-cert.pem``.

More about Azure Certificate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For more information about Azure service certificate, visit Azure Documentation
`here
<https://azure.microsoft.com/en-us/documentation/articles/cloud-services-certs-create/>`_
and `here
<https://azure.microsoft.com/en-us/documentation/articles/cloud-services-python-how-to-use-service-management/>`_.


Register Azure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Run ``register azure`` to type account information

  ::

          cm> register azure

          # ######################################################################
          # Register azure
          # ######################################################################
          Enter managementcertfile (TBD): **/home/ubuntu/.cloudmesh/azure-cert.pem**
          Enter servicecertfile (TBD):
          Enter subscriptionid (TBD): **8b3df2b9-3ac1-4828-b6e0-8f8be62e6e6r**
          Enter thumbprint (TBD):


You can skip servicecertfile and thumbprint at this stage.

Set Default Cloud
-------------------------------------------------------------------------------

You may want to set Azure as a default cloud before you start using Azure
cloud. Default cloud setting allows you to run your Cloudmesh commands towards
a selected cloud, in this case Azure, without additional parameters e.g.
``--cloud=``.  You can change default settings anytime while you are in
Cloudmesh shell.

- Run ``default cloud=azure``
  ::

    cm> default cloud=azure
    set default cloud=azure. ok.

Starting Azure Virtual Machine
-------------------------------------------------------------------------------

``vm boot`` starts a new Azure Virtual Machine under your account with default
settings.

::

   cm> vm boot
   Machine TBD-002 is being booted on cloud azure ...
   +-----------+----------------------------------------------------------------------------------------------+
   | Attribute | Value                                                                                        |
   +-----------+----------------------------------------------------------------------------------------------+
   | cloud     | azure                                                                                        |
   | flavor    | Basic_A1                                                                                     |
   | image     | b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_5-LTS-amd64-server-20160315-en-us-30GB        |
   | key       | albert                                                                                       |
   | meta      | +                                                                                            |
   |   -       | category: azure                                                                              |
   |   -       | kind: cloudmesh                                                                              |
   |   -       | group: default                                                                               |
   |   -       | image: b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_5-LTS-amd64-server-20160315-en-us-30GB |
   |   -       | key: albert                                                                                  |
   |   -       | flavor: Basic_A1                                                                             |
   | name      | TBD-002                                                                                      |
   | nics      |                                                                                              |
   | secgroup  | +                                                                                            |
   |   -       | TBD-default                                                                                  |
   +-----------+----------------------------------------------------------------------------------------------+
   INFO: service name: TBD-002
   INFO: location name: Central US

   INFO: cloudmesh storage found
   INFO: Username: azure
   INFO: password: jxETwEsQ28147712
   INFO: blob storage location: https://cloudmesh.blob.core.windows.net/vhds/TBD-002.vhd
   ....
   INFO: TBD-002 created successfully
   info. OK.


Your first VM ``TBD-002`` started on AWS with default settings which are Basic_A1 (1 core) flavor and Ubuntu 12.04.5 LTS image. 
Random password is generated for your ssh access, SSH Key is not used.

List of running Azure Instances
-------------------------------------------------------------------------------

Simple ``vm list`` run provides a list of running VM instances including one
that you started above. For example::

  cm> vm list
  Listing VMs on Cloud: azure
  +----+----------------------------------+---------+---------+-------------+-------------+------------+-------+--------------+---------------+------+----------+---------------------+
  | id | uuid                             | label   | status  | public_ips  | private_ips | image_name | key   | availability | instance_type | user | category | updated_at          |
  +----+----------------------------------+---------+---------+-------------+-------------+------------+-------+--------------+---------------+------+----------+---------------------+
  |    | 2f0adf4eff464eb5baf226f4abca44b8 | TBD-005 | Running | 40.77.21.75 |             |            | albert|              |               | TBD  | azure    | 2016-07-16 22:32:04 |
  +----+----------------------------------+---------+---------+-------------+-------------+------------+-------+--------------+---------------+------+----------+---------------------+

``vm refresh`` command updates status of VMs.

SSH to Azure Virtual Machine
-------------------------------------------------------------------------------

Once your Azure VM is up and running, you are able to get access to the
machine vis SSH.  In Cloudmesh, you run ``vm ssh <VM Name>`` to connect. For
example, run ``vm ssh TBD-002 --username=azure`` with ``azure`` username to get
into the VM.

:: 

  cm> vm ssh TBD-002 --username=azure
  login aazure:azure@TBD-002
  +-------------+---------+
  | Attribute   | Value   |
  +-------------+---------+
  | cloud       | aazure  |
  | command     |         |
  | floating_ip |         |
  | key         | albert  |
  | name        | TBD-002 |
  | username    | azure   |
  +-------------+---------+
  Determining IP Address to use with a ping test.
  Checking 40.77.21.75...
  IP to be used is: 40.77.21.75
  INFO: Connecting to Instance at IP:40.77.21.75
  Welcome to Ubuntu 12.04.5 LTS (GNU/Linux 3.13.0-83:-generic x86_64)

   * Documentation:  https://help.ubuntu.com/

     System information as of Sat Jul 16 22:48:37 UTC 2016

     System load:  0.04              Processes:           218
     Usage of /:   3.3% of 28.80GB   Users logged in:     0
     Memory usage: 6%                IP address for eth0: 100.111.16.36
     Swap usage:   0%

     Graph this data and manage this system at:
       https://landscape.canonical.com/

     Get cloud support with Ubuntu Advantage Cloud Guest:
       http://www.ubuntu.com/business/services/cloud

     0 packages can be updated.
     0 updates are security updates.


     New release '14.04.4 LTS' available.
     Run 'do-release-upgrade' to upgrade to it.


     Your Hardware Enablement Stack (HWE) is supported until April 2017.


     The programs included with the Ubuntu system are free software;
     the exact distribution terms for each program are described in the
     individual files in /usr/share/doc/*/copyright.

     Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
     applicable law.

     To run a command as administrator (user "root"), use "sudo <command>".
     See "man sudo_root" for details.

     azure@TBD-002:~$

Congrats! you have launched an Azure Virtual Machine on Cloudmesh and it's
ready to use.

Terminating Azure Virtual Machine
-------------------------------------------------------------------------------

``vm delete`` terminates Azure Virtual Machine like::

        cm> vm delete TBD-002
        INFO: TBD-005 deleted
        VM record TBD-002 is being deleted from the local database...

That's all. Simply provide VM instance name to terminate.

List of Server Sizes (flavors)
-------------------------------------------------------------------------------

The server sizes that Azure provides can be listed by ``flavor list``
Amazon EC2 provide more than 40 flavors like::

.. include:: azure-flavor.rst

Notes
-------------------------------------------------------------------------------

Azure Virtual Machine is implemented with `Azure SDK for Python 
<https://github.com/Azure/azure-sdk-for-python>`_ in Cloudmesh.

