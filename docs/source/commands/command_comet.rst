.. _comet_command:

Comet Virtual Cluster
======================================================================

Via XSEDE comet allows users to request high-performance virtual
clusters (VCs) as part of their Comet allocation. The VC front-end
associated with this award will be available 24/7 on the virtual
machine hosting nodes, but VC compute nodes are transitory and
allocated through the batch scheduler. The front end can be thought of
as the point of entry for the VC and is used to manage VC resources
and launch jobs. The justification for compute time is the same as for
a standard allocations request. Projects that are awarded a VC can use
their compute time through either the batch queue or the VC, but the
expectation is that the latter will account for a substantial fraction
of the usage.

In comet VCs are not meant to replace the standard HPC batch queuing
system, which is well suited for most scientific and technical
workloads. In addition, a VC should not be simply thought of as a VM
(virtual machine). Other XSEDE resources, such as Indiana
University's Jetstream address this need. Comets VCs are primarily
intended for those users who require both fine-grained control over
their software stack and access to multiple nodes. With regards to the
software stack, this may include access to operating systems different
from the default version of CentOS available on Comet or to low-level
libraries that are closely integrated with the Linux
distribution. Science Gateways serving large research communities and
that require a flexible software environment are encouraged to
consider applying for a VC, as are current users of commercial clouds
who want to make the transition for performance or cost reasons.

Maintaining and configuring a virtual cluster requires a certain level
of technical expertise. We expect that each project will have at least
one person possessing strong systems administration experience with
the relevant OS since the owner of the VC will be provided with "bare
metal" root level access. SDSC staff will be available primarily to
address performance issues that may be related to problems with the
Comet hardware and not to help users build their system images.

All VC requests must include a brief justification that addresses the
following:

* Why is a VC required for this project?
* What expertise does the PI's team have for building and maintaining the VC?

Please visit https://portal.xsede.org/sdsc-comet for more details on comet.

Comet Client
------------

Example CLI usage to manage comet virtual cluster using cloudmesh
client

* Comet Command: :ref:`comet_command` (this page)
* Comet Refernce Card :ref:`refcard_comet`
* Man page `comet <../man/man.html#comet>`_
* http://www.sdsc.edu/support/user_guides/comet.html
* https://portal.xsede.org/sdsc-comet

Teminology
^^^^^^^^^^^

We use in this section the following terminology:

computeset:
    TBD

frontend:
    TBD

image:
    TBD

console:
    TBD

virtual cluster:
    TBD

individual nodes:
    TBD

image attach:
    TBD

image detach:
    TBD

Configuration
^^^^^^^^^^^^^^^

The configuration of the cloudmesh client is done semi automatically for you.
All you have to do after the installation is to call cloudmesh client once.

This is done best with the command::

    cm help

This will automatically generate a configuration file at::

    ~/.cloudmesh/cloudmesh.yaml.

This file you can now modify with your favourite editor. It will contain a
default section similar to::


    comet:
        auth_provider: apikey
        userpass:
            username: TBD
            password: TBD
        apikey:
            api_key: KEYSTRING
            api_secret: SECRETSTRING


Two authentication mechanisms are supported. You will only need one. Please
get in contact with the comet administrators to let you know which one is best
suited for you. If you have username and password you can get started with
that. Otherwise the comet admins will assign you an api_key and secret.

List all clusters owned by the authenticated identity (summarized
format):

.. prompt:: bash
  
  cm comet ll

List all clusters owned by the authenticated identity (detailed
list):

.. prompt:: bash
  
  cm comet cluster
    
List a cluster by name:

.. prompt:: bash
  
  cm comet cluster vc2
    
List all defined computesets:

.. prompt:: bash

  cm comet computeset
    
List one computeset:

.. prompt:: bash
  
   cm comet computeset 63
    
Power on a set of compute nodes in cluster vc4:

.. prompt:: bash
  
    cm comet power on vc4 vm-vc4-[0-3]
    
This will request the nodes for a default period of time - 2 hours.

To request for a longer time period, use --walltime parameter. 
E.g., 100m (100 minutes), 6h (6 hours), 2d (2 days) , 1w (1 week):

.. prompt:: bash

    cm comet power on vc4 vm-vc4-[0-3] --walltime=6h

The above will put the request under the one allocation associated with the cluster.
If your cluster have more than one allocations, use --allocation
parameter:

.. prompt:: bash

    cm comet power on vc4 vm-vc4-[0-3] --allocation=YOUR_ALLOCATION

If you have more allocations, but does not specify via CLI, you will see a list of 
allocations to choose from to use.

You can also power on N arbitrary nodes, if there is enough resource:

.. prompt:: bash

    cm comet power on vc4 --count=4

The comet system will find 4 available nodes from the specified cluster and start them 
as one computeset.

You can power off and back on individual nodes of an active
computeset. E.g.:

.. prompt:: bash

    cm comet power off vc4 vm-vc4-[0,1]

and then:

.. prompt:: bash

    cm comet power on vc4 vm-vc4-0

Or power off the whole computeset by specifying the computeset id:

.. prompt:: bash

    cm comet power off vc4 123

or by specifying the hosts:

.. prompt:: bash

    cm comet power off vc4 vm-vc4-[0-3]

Please note if you powered off all nodes from an active computeset, the computeset 
itself will be removed as well (changed to 'completed' status)

You can also power on one single node as a computeset:

.. prompt:: bash
  
    cm comet power on vc4 vm-vc4-[7]

or simply:

.. prompt:: bash

    cm comet power on vc4 vm-vc4-7

Power on the front end node of the specified cluster:

.. prompt:: bash
  
    cm comet power on vc4
    
Get console of a running node:

.. prompt:: bash
  
    cm comet console vc4 vm-vc4-0

Get console of the front end:

.. prompt:: bash
  
    cm comet console vc4

Get the list of images that are available to you:

.. prompt:: bash

    cm comet image list

Upload an image to the public shared folder:

.. prompt:: bash

    cm comet image upload /path/to/your/image.iso

Or with a specified new image name:

.. prompt:: bash

    cm comet image upload /path/to/your/image.iso --imagename=newimagename.iso

Attach an image to a compute node:

.. prompt:: bash

    cm comet image attach newimagename.iso vc4 vm-vc4-0

Or to the front end:

.. prompt:: bash

    cm comet image attach newimagename.iso vc4

To detach an iso:

.. prompt:: bash

    cm comet image detach vc4 vm-vc4-0

Please note image attaching/detaching will only take effect after you hard reboot 
the node (power off and then power on).

You can also rename a compute node:

.. prompt:: bash

    cm comet node rename vc4 vm-vc4-0 mynode0
