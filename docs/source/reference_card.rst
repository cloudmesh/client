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



