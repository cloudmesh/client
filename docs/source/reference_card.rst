Reference Card
============


Shell
------

.. list-table:: Shell
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Description
   * - cm help
     - help
   * - cm man
     - manual pages
   * - cm script.cm
     - execute cm commands in script

Shell commands that expire after a session
------------------------------------------

.. list-table:: Shell
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Description
   * - cm color on
     - sets the shell color
   * - cm color off
     - switches off the color
   * - cm refresh on
     - automatic refresh from the clouds
   * - cm refresh off
     - data is only read from the database. Useful for managing thousands of VMs or limit your access to the cloud.
   * - var a=xyx
     - declares a variable
   * - var username=cloudmesh.profile.username
     - reads the variable from the cloudmesh.yaml file
   * - var time=now
     - gets the time and store it in the variable time


Clouds
-------

.. list-table:: Cloud
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Description
   * - cm image list
     - list images
   * - cm flavor list
     - list flavors
   * - cm vm list
     - list vms
   * - cm vm boot
     - boot vm
   * - cm vm boot --cloud=kilo
     - boot vm on cloud kilo
   * - cm default cloud=kilo
     - set default cloud to kilo
   * - cm select image
     - select interactively the default image (not implemented yet).
   * - cm select flavor
     - select interactively the default flavor (not implemented yet).
   * - cm select cloud
     - select interactively the default cloud (not implemented yet).

.. _refcard_comet:

Comet
-------

+---------------------------------------+------------------------------------------------------------------------+
| | Command                             | | Description                                                          |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet ll                         | | Summary list of clusters owned by the authenticated                  |
| |                                     | | identity                                                             |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet cluster                    | | Detailed list of clusters owned by the authenticated                 |
| |                                     | | identity                                                             |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet cluster vc2                | | List a cluster by name (vc2)                                         |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet computeset                 | | List all defined computesets                                         |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet computeset 63              | | Display one computeset by specifying the computeset                  |
| |                                     | | id (63)                                                              |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4               | | Power on the frontend node of the specified cluster                  |
| |                                     | | (vc4)                                                                |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power off vc4              | | Power off the frontend node of the specified cluster                 |
| |                                     | | (vc4)                                                                |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-[0-3]  | | Power on a set of compute nodes in one cluster (vc4)                 |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 --count=4     | | Power on N (4) arbitrary node in one cluster (vc4)                   |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-[0-3]  | | Power on a set of compute nodes in a cluster (vc4)                   |
| |    --walltime=6h                    | | for a givenwalltime (30m, 3h, 2d, 1w, for 30 minutes,                |
| |                                     | | 3 hours, 2 days, 1 week, respectively)                               |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-[0-3]  | | Power on with allocation                                             |
| |    --allocation=YOUR_ALLOCATION     | |                                                                      |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power off vc4 vm-vc4-[0,1] | | You can power off and back on individual nodes of                    |
| | cm comet power on vc4 vm-vc4-0      | | an active computeset without impacting other nodes                   |
| |                                     | | in the same computeset                                               |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-7      | | Power on one node as a compute set                                   |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power off vc4 123          | | power off the whole computeset by specifying the                     |
| |                                     | | cluster name (vc4) and computeset id (123)                           |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power off vc4 vm-vc4-[0-3] | | power off the whole computeset by specifying all nodes               |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet console vc4                | | Get console of the frontend                                          |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet console vc4 vm-vc4-0       | | Get console of a running node                                        |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image list                 | | Get list of images available to you                                  |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image upload               | | Upload an image to the shared public directory on                    |
| |    /path/to/your/image.iso          | | nucleus server                                                       |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image upload               | | Upload an image to the shared public directory on                    |
| |    /path/to/your/image.iso          | | nucleus server with a new image name                                 |
| |    --imagename=newimagename.iso     | |                                                                      |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image attach               | | Attach an image (newimagename.iso) to frontend of                    |
| |    newimagename.iso vc2             | | a cluster (vc2)                                                      |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image attach               | | Attach an image to a compute node (vm-vc2-0) for a                   |
| |    newimagename.iso vc2 vm-vc2-0    | | cluster (vc2)                                                        |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image detach vc2           | | Detach the attached iso image from frontend of a                     |
| |                                     | | cluster (vc2)                                                        |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image detach vc2 vm-vc2-0  | | Detach the attached iso image from a compute node                    |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image attach               | | Attach an image to a set of compute node, specified in               |
| |    imagename.iso vc2 vm-vc2-[0-3]   | | hostlist format (vm-vc2-[0-3]) for a cluster (vc2)                   |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet image detach               | | Detach also works in bulk                                            |
| |    vc2 vm-vc2-[0-3]                 | |                                                                      |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet node rename vc2            | | Rename a compute node (vm-vc2-0) from a cluster (vc2)                |
| |    vm-vc2-0 mynode0                 | | to a new name (mynode0)                                              |
+---------------------------------------+------------------------------------------------------------------------+


HPC
-------

.. list-table:: HPC
   :widths: 25 75
   :header-rows: 1

   * - Command
     - Description
   * - cm help
     - Help
   * - cm hpc queue <batch>
     - info about the queue <batch>
   * - cm hpc info
     - information about the queues on the HPC resource
   * - cm hpc run uname -a
     - runs the command uname
   * - cm hpc run list
     - prints the ids of previously run jobs
   * - cm hpc run list
     - prints the ids of previously run jobs
   * - cm hpc run list 11
     - prints the information regarding the job with the id 11



