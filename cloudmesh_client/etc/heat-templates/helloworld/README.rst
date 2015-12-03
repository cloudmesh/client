
OS Heat - Hello World Example
===============================================================================

The helloworld.yaml template provides a basic example of starting number of
instances using OpenStack Heat. Tested on FutureSystems Juno, not Kilo.


Run
-------------------------------------------------------------------------------

Start five VM instances with your registered key on india.futuresystems.org.

.. code::

  heat stack-create -u https://raw.githubusercontent.com/cloudmesh/client/master/cloudmesh_client/etc/heat-templates/helloworld/helloworld.yaml -P "key_name=$KEYNAME;cluster_size=5" hello-world-five

* ``-u`` option is a URL for a template. If you have a template file on your $HOME directory, you can use it with ``-f`` option like ``-f helloworld.yaml`` instead.
* ``-P`` option is a parameter option. You can change SSH key name or the number of cluster size with this option.
* ``key_name`` is a parameter defined in the ``helloworld.yaml`` template. The given key will be injected to VM.
* ``cluster_size`` is a number of cluster size to start. Default is 3 according to the ``helloworld.yaml``.
* ``hello-world-five`` is your stack name. You can use any name you like but it should be unique in your group.

The output looks like this, if it is requested successfully:

.. code::

   +--------------------------------------+------------------+--------------------+----------------------+
   | id                                   | stack_name       | stack_status       | creation_time        |
   +--------------------------------------+------------------+--------------------+----------------------+
   | 697cf284-b10d-40eb-8ae9-8ca7597c07d0 | hello-world-five | CREATE_IN_PROGRESS | 2015-12-03T19:57:24Z |
   +--------------------------------------+------------------+--------------------+----------------------+

Status
-------------------------------------------------------------------------------

The VMs launched can be found via ``nova`` command. For example:

.. code::

        +--------------------------------------+------------------------------------------------------+-----------+------------+-------------+--------------------------------------+
        | ID                                   | Name                                                 | Status    | Task State | Power State | Networks                             |
        +--------------------------------------+------------------------------------------------------+-----------+------------+-------------+--------------------------------------+
        | a0991ccb-4f29-4fd0-91d7-607462c4e8d5 | hello-world-five-scaling-omgvsvxurgio-0-vk5a2gewbnqn | BUILD     | spawning   | NOSTATE     | int-net=10.23.3.38                   |
        | f1fa6225-bb82-473a-99f6-1ff8bb793e8f | hello-world-five-scaling-omgvsvxurgio-1-qsu3wqjytq2m | BUILD     | spawning   | NOSTATE     | int-net=10.23.3.37                   |
        | 52d4a33c-838c-4c24-8956-e295b1ad9d6a | hello-world-five-scaling-omgvsvxurgio-2-qrtf4hv2ad27 | BUILD     | spawning   | NOSTATE     | int-net=10.23.3.4                    |
        | e12974ca-7806-48fd-9860-2c3dc74dcd5b | hello-world-five-scaling-omgvsvxurgio-3-fjeuc7mb5pgo | BUILD     | spawning   | NOSTATE     | int-net=10.23.3.39                   |
        | d6ed1c5f-f522-4fd5-a234-d6789b9177b0 | hello-world-five-scaling-omgvsvxurgio-4-kegampaijtfv | BUILD     | spawning   | NOSTATE     | int-net=10.23.3.40                   |
        +--------------------------------------+------------------------------------------------------+-----------+------------+-------------+--------------------------------------+

Access
-------------------------------------------------------------------------------

With your SSH key, each VM is accessible. The default user name is ``ec2-user``
so the ssh command looks like, for example:

.. code::

   ssh ec2-user@10.23.3.38

   Warning: Permanently added '10.23.3.38' (RSA) to the list of known hosts.


   Welcome to Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-63-generic x86_64)

    * Documentation:  https://help.ubuntu.com/

      System information as of Thu Dec  3 20:26:53 UTC 2015

      System load: 0.0               Memory usage: 2%   Processes:       52
      Usage of /:  56.9% of 1.32GB   Swap usage:   0%   Users logged in: 0

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

   $

Template
-------------------------------------------------------------------------------

Let's review the ``helloworld.yaml`` template briefly. Details are explained in
OpenStack Heat Documentation [1].

.. code::

  heat_template_version: 2013-05-23

This explains which Heat version will be used to interpret the
``helloworld.yaml`` template [2].  A later version provides more functionalites
but may not support backward-compatibility.

.. code::

  parameters:

A user input will be delivered by ``parameters`` in the template. We specified
``key_name`` and ``cluster_size`` in the example to change SSH key name or the
number of VM instances. Other parameters are also available i.e.
``instance_type`` (flavor), ``image_id`` (or image name). Note that if you use
a ``default`` value in the parameter, Heat uses the default value when it is
not present. In this example, ``m1.small`` is a default flavor and
``futuresystems/ubuntu-14.04`` is a default image to start the ``HelloWorld``
stack in OpenStack Heat.

.. code::

  resources:

A VM instance or a floating IP address is one of the OpenStack resources and
these are defined under ``resources:`` in a Heat template.


.. code::

  { get_param: PARAMETER_NAME }

``get_param`` is quite useful to replace a variable with a user input. In our
example, we replace a SSH key name and a number of VM instances.


[1] http://docs.openstack.org/developer/heat/template_guide/
[2] http://docs.openstack.org/developer/heat/template_guide/hot_spec.html#heat-template-version
