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
* What expertise does the PI's team have for building and maintaining
  the VC?

Please visit https://portal.xsede.org/sdsc-comet for more details on
comet.

Links
------------

* Cloudmesh Comet CLI: :ref:`comet_command`
* Comet CLI Refernce Card :ref:`refcard_comet`
* Comet CLI Man page `comet <man/man.html#comet>`_
* https://portal.xsede.org/sdsc-comet
* http://www.sdsc.edu/support/user_guides/comet.html
* Comet nucleus API Docs: https://comet-nucleus.sdsc.edu/nucleus/docs/

Steps to get a virtual cluster on comet
------------------------------

1. Obtain an allocation via XSEDE as documented at
   https://www.xsede.org/allocations To get started quickly we
   recommend a trial allocation for comet as discussed here:
   https://portal.xsede.org/allocations/announcements#trial

2. Once your Comet virtual cluster allocation is approved, you will be
   contacted by a SDSC staff to ask you create a Comet Virtual Cluster
   (CVC) account on XSEDE user portal.

3. Our team members at IU will contact you to collect the necessary
   information for VC setup and administrative purposes. You need to
   provide a physical mailing address so a preconfigured YubiKey token
   could be sent to you, which is required to access your VC. You will
   need to fill out and return a YubiKey receipt acknowledgement form.

4. At this time the comet team will send you details about your virtual
   cluster, and how to use Cloudmesh client tool to access it. Once
   you have this information you can start a virtual cluster immediately.

5. You are expected to setup your cluster by yourself, starting with the
   frontend node, and then the compute nodes. We have provided a list of
   iso images that you may want to use. You can check what is available
   by running::

     cm comet iso list

   If a desired iso image is not in the list, you can upload your own.
   please refer to the :ref:`comet_command` section for more information.

6. Once you have a desired ISO image to install from, you need to attach
   an image to your node(s). As an example, if your cluster is called vc2,
   and you have 3 compute nodes called vm-vc2-0, vm-vc2-1, vm-vc2-2. To
   attach the iso to your frontend, or compute nodes::

     cm comet iso attach imagename.iso vc2
     cm comet iso attach imagename.iso vc2 vm-vc2-[0-3]

   Please note that the name of the cluster (vc2) will be different
   for you.

7. You need to install and configure your frontend first. To start the
   frontend node::

     cm comet power on vc2

   And to attach console of it::

     cm comet console vc2

   Now you can work on the installation and configuration as if you were
   doing that on a regular physical host you are managing.

   For any problem or questions regarding your VC setup, please contact
   our support team at IU.

8. Now you can just power on and boot the compute node(s) with::

     cm comet start vc2 vm-vc2-[0-3]

   To install it from ISO, or PXE-boot and install from the frontend node.

   The console access works the same way for individual compute node::

     cm comet console vc2 vm-vc2-0

FAQ
-----------------------------------------------

Why the nodes/computeset I requested to start was not started immediately?
~~~~~~~~~~~~

Comet virtual clusters are deployed on the same physical resources of
Comet cluster where the regular HPC jobs are running, thus the starting
of VC nodes are also subject to the availability of system resources at
the time when VC requests are being made.

Why the computeset I started shows as 'active' but the nodes of the computeset are not running?
~~~~~~~~~~~~

There are various cases that why this might happen.

1. The physical host(s) where the VM(s) are to be deployed is having memory
issue (fragmentation, not enough) which prevents the VM(s) to be running. We
are consistently working on improving the situation in similar cases, but if
you encounter this please submit a ticket for help.

2. In some case you might have a 'bad' ISO attached to the node to be started,
which caused it to be stuck in the booting process. You can verify this by
attaching to the console access. The fix for this is to detach the ISO, or
attach another proper one.

Why are the names of the nodes so complicated?
~~~~~~~~~~~~

And why do I also need to specify the name of the cluster? Can this
not be omitted?

Comet virtual cluster tools allow a user to manage multiple virtual
clusters at the same time and a node could be reassigned between
virtual clusters.  This makes it necessary that you must specify the
virtual cluster explicitly.  The names of the nodes are a default
provided by comet and we expect that for easier management you will at
one point rename them while using the comet rename command to a naming
scheme that you desire.

For example assume my virtual cluster is called osg than you may want to
rename your nodes such as::

    cm comet node rename osg vm-osg-0 osg-0
    cm comet node rename osg vm-osg-1 osg-1
    ...

This wil than result in a cluster where the frontend name is osg
(given to you by the comet team), but you have renamed the nodes to
osg-1, osg-2, ...

I have the Comet YubiKey mixed up with my other keys. How can I find which one is for Comet?
~~~~~~~~~~~~

Plug the key in and tap it into notepad or something similar. It will
generate a string similar to this:

     geffgefe........................................

 The beginning characters will help identify the key. All Comet VC keys
 should generate a string starting with these characters.

How do I get support?
~~~~~~~~~~~~

Please submit a ticket to XSEDE ticket system, while putting COMET VC
on the subject line.
