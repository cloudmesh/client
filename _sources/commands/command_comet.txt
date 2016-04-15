.. _comet_command:

Comet Virtual Cluster
======================================================================

Introduction
-------------

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

Links
------------

Example CLI usage to manage comet virtual cluster using cloudmesh
client

* Comet Command: :ref:`comet_command` (this page)
* Comet Refernce Card :ref:`refcard_comet`
* Man page `comet <../man/man.html#comet>`_
* http://www.sdsc.edu/support/user_guides/comet.html
* https://portal.xsede.org/sdsc-comet
* Comet nucleus API Docs: https://comet-nucleus.sdsc.edu/nucleus/docs/

Teminology
-----------

We use in this section the following terminology:

computeset:
    A group of compute nodes started together and being in some state
    (submitted, started, finished, failed). Each compute node can only belong
    to 1 computesets in submitted or active state.

frontend:
    A node with limited computational resources used to manage a virtual
    cluster. Frontends run 24/7, have a public interface and a private
    interface. The public interface provides outside access to the virtual
    cluster while the private interface is used to manage/install the compute
    nodes.

image:
    A file containing the contents and structure (ISO9660) of a disk volume
    which can be attached as a cdrom to a node.

console:
    An interactive representation of the screen of a virtual cluster
    node (text or graphical) provided to assist with node installation
    and management.

virtual cluster:
    A virtual cluster is a loosely or tightly connected network of virtual
    computers managed together by a virtual cluster administrator.

node:
    The term node is used to refer to individual computers in a virtual cluster.

image attach:
    Attach is an action applied to a node / image pair whereby the contents
    of the image are made available to a node on the next power on.

image detach:
    Detach is an action applied to a node / image pair whereby the contents
    of the image are made unavailable to the node on the next power on.

Configuration
--------------

The configuration of the cloudmesh client is done semi automatically for you.
All you have to do after the installation is to call cloudmesh client once.

This is done best with the command::

    cm help

This will automatically generate a template configuration file at::

    ~/.cloudmesh/cloudmesh.yaml.

Next you can initiate the configuration file::

    cm comet init

Follow the prompt to configure and select endpoint, and initialize the
auth settings by provide your username and password. Once you are
successfully authenticated it will retrieve the api key and secret and
configure the cloudmesh.yaml with proper api auth information. Then you
will be able to use the commands to manage your comet virtual cluster.

Commands
---------

Next we list a number of important commands from the CLI that will help you
managing your comet virtual clusters.

Getting information of your cluster(s); nodes; computesets; etc.
~~~~
List all clusters owned by the authenticated identity (summarized
format):

.. prompt:: bash
  
  cm comet ll

List all clusters owned by the authenticated identity (detailed
list):

.. prompt:: bash
  
  cm comet cluster
    
List a cluster by name (we use here vc2 as example):

.. prompt:: bash
  
  cm comet cluster vc2

Cluster listing view also supports other output format, e.g. json, csv, etc.:

.. prompt:: bash

  cm comet cluster vc2 --format=csv

This can be useful for scripting.
    
List all defined computesets:

.. prompt:: bash

  cm comet computeset
    
List one computeset:

.. prompt:: bash
  
   cm comet computeset 63

Power management of frontend node:
~~~~
Power on the front end node of the specified cluster:

.. prompt:: bash

    cm comet power on vc2

To power if off:

.. prompt:: bash

    cm comet power off vc2

You can also reboot/reset/shutdown the fronend using the same 
syntax, e.g., to reboot:

.. prompt:: bash

    cm comet power reboot vc2

Please note running frontend node itself would not charge you any allocations.

Resource allocation and tear down:
~~~~
The requested cluster/VMs has to be started by requesting physical allocations. This
will charge your allocation based on nodes you requested and the walltime.

Start a set of compute nodes in cluster vc2:

.. prompt:: bash
  
    cm comet start vc2 vm-vc2-[0-3]
    
This will request the nodes for a default period of time and power on them

To request for a longer time period, use --walltime parameter. 
E.g., 100m (100 minutes), 6h (6 hours), 2d (2 days) , 1w (1 week):

.. prompt:: bash

    cm comet start vc2 vm-vc2-[0-3] --walltime=6h

The above will put the request under the one allocation associated with the cluster.
If your cluster have more than one allocations, use --allocation
parameter:

.. prompt:: bash

    cm comet start vc2 vm-vc2-[0-3] --allocation=YOUR_ALLOCATION

If you have more allocations, but does not specify via CLI, you will see a list of 
allocations to choose from to use.

You can also request a group of N nodes, if there is enough resource:

.. prompt:: bash

    cm comet start vc2 --count=4

The comet system will find 4 available nodes from the specified cluster and start them 
as one computeset.

You can also start a single-node computeset:

.. prompt:: bash

    cm comet start vc2 vm-vc2-[7]

or simply:

.. prompt:: bash

    cm comet start vc2 vm-vc2-7

To power down all running nodes from an active computeset and also free the allocated
resources:

.. prompt:: bash

    cm comet terminate 123

This will gracefully shutdown the nodes in the group identified by computeset 123,
and also free the unused allocations. A computeset will be teared down automatically
when it reaches its requested walltime

Power management of compute nodes:
~~~~

You can power off and back on individual nodes from a cluster, 
without affecting other running nodes in the computesets. E.g.:

.. prompt:: bash

    cm comet power off vc2 vm-vc2-[0-7]

and then:

.. prompt:: bash

    cm comet power on vc2 vm-vc2-[0-7]

or shutdown gracefully a group of nodes:

.. prompt:: bash

    cm comet power shutdown vc2 vm-vc2-[0-3]

Please note even if you powered off all nodes from an active computeset, the computeset 
itself, and the associated physical resource, is still active and can only be accessed
exclusively by you till the requested walltime is reached. During this time you can freely
power the nodes back on and off.

Getting Console access
~~~~
Get console of the frontend:

.. prompt:: bash
  
    cm comet console vc2

Get console of a running compute node:

.. prompt:: bash
  
    cm comet console vc2 vm-vc2-0

This will open a browser window using the system default browser 
to display the console (in Mac OS X); or a firefox window (in Linux).
If no compatible browser found, it will print out a URL so you can 
access it via other means.

System image management
~~~~
Get the list of images that are available to you:

.. prompt:: bash

    cm comet iso list

Upload an image to the public shared folder:

.. prompt:: bash

    cm comet iso upload /path/to/your/image.iso

Or with a specified new image name:

.. prompt:: bash

    cm comet iso upload /path/to/your/image.iso --imagename=newimagename.iso

Attach an image to the frontend:

.. prompt:: bash

    cm comet iso attach newimagename.iso vc2

Or to a compute node:

.. prompt:: bash

    cm comet iso attach newimagename.iso vc2 vm-vc2-0

To detach the attached iso image from frontend node:

.. prompt:: bash

    cm comet iso detach vc2

Or from a compute node:

.. prompt:: bash

    cm comet iso detach vc2 vm-vc2-0

Image attaching/detaching also works on compute nodes in bulk:

.. prompt:: bash

    cm comet iso attach newimagename.iso vc2 vm-vc2-[0-4]

.. prompt:: bash

    cm comet iso detach vc2 vm-vc2-[0-4]

Please note image attaching/detaching will only take effect after you hard reboot 
the node (power off and then power on).

Other commands:
~~~~
You can also rename a compute node, or a list of nodes in batch:

.. prompt:: bash

    cm comet node rename vc2 vm-vc2-0 mynode0

.. prompt:: bash

    cm comet node rename vc2 vm-vc2-[0-7] newname-[0-7]

Please use hostlist format to specify the list of OLDNAMES AND NEWNAMES


How to get a virtual cluster?
------------------------------

1. Obtain an allocation via XSEDE as documented at https://www.xsede.org/allocations
   To get started quickly we recommend a trial allocation for comet as
   discussed here: https://portal.xsede.org/allocations/announcements#trial

2. Once you have aan allocation and added your virtuall cluster admins to
   your allocation. Get in contact with XSEDE to identify the scope of your
   project and allocation size (This may already be specified in the
   allocation request).

        At this time send e-mail to laszewski AT gmail DOT com and
        kevinwangfg AT gmail DOT com

        In future we will be using the XSEDE ticket system once it is set up
        for us

3. At this time the comet team will send you details about the name of your
   virtual cluster, how many nodes you can use. Once you have this information
   you can start a virtual cluster immediately.


4. Please note that it will be up to you to provide an apropriate iso image.
   A small number of sample images are provided and you can list tehm with ::

     cm comet iso list

5. Next you need to attach an image to your compute nodes (we assume you
   have 3 nodes called vm-vc2-0, vm-vc2-1, vm-vc2-2 ::

        cm comet iso attach imagename.iso vc2 vm-vc2-[0-3]

   Please note that the name of the cluster (vc2) will be different for you

6. Now you can just power on and boot the node with::

    cm comet start vc2 vm-vc2-[0-3]

7. To see the console of a node you can use for an individual node (here the
 node 0)::

     cm comet console vc2 vm-vc2-0

Why are the names of the nodes so complicated?
-----------------------------------------------

And why do i also need to specify the name of the cluster? Can this not be
omitted?

Comet virtual cluster tools allow a user to manage multiple virtual clusters
at the same time and a node could be reassigned between virtual clusters.
This makes it necessary that you must specify the virtual cluster explicitly.
The names of the nodes are a default provided by comet and we expect that
for easier management you will at one point rename them while using the
comet rename command to a naming scheme that you desire.

For example assume my virtual cluster is called osg than you may want to
rename your nodes such as::

    cm comet node rename osg vm-osg-0 osg-0
    cm comet node rename osg vm-osg-1 osg-1
    ...

This wil than result in a cluster where the frontend name is osg (given to
you by the comet team), but you have renamed the nodes to osg-1, osg-2, ...

How do I get support?
----------------------

At this time simply send mail to laszewski AT gmail DOT com and kevinwangfg AT gmail DOT com.
We will get back to you ASAP hopefully within one business day.
