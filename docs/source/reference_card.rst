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

Comet
-------

+---------------------------------------+------------------------------------------------------------------------+
| | Command                             | | Description                                                          |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet ll                         | | Summary list of clusters owned by the authenticated identity         |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet cluster                    | | Detailed list of clusters owned by the authenticated identity        |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet cluster vc2                | | List a cluster by name                                               |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet computeset                 | | List all defined computesets                                         |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet computeset 63              | | List one computeset                                                  |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-[0-3]  | | Power on a set of compute nodes in cluster vc4                       |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-[0-3]  | | Power on a set of compute nodes in cluster vc4 for a given           |
| |    --walltime=6h                    | | walltime                                                             |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-[0-3]  | | Power on with allocation                                             |
| |    --allocation=YOUR_ALLOCATION     | |                                                                      |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power off vc4 vm-vc4-[0,1] | | You can power off and back on individual nodes of                    |
| |                                     | | an active computeset                                                 |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-0      | | Power on a compute set                                               |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power off vc4 123          | | Or power off the whole computeset by specifying the                  |
| |                                     | | computeset id                                                        |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4 vm-vc4-7      | | You can also power on one individual vm                              |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet power on vc4               | | Power on the front end node of the specified cluster                 |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet console vc4 vm-vc4-0       | | Get console of a running node                                        |
+---------------------------------------+------------------------------------------------------------------------+
| | cm comet console vc4                | | Get console of the front end                                         |
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



