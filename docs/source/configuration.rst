Configuration
=============

::

   cm setup_yaml


::

   cm plugins add cloudmesh_cloud


::

   cm help


cloudmesh.yaml
--------------

::
   
   ~/.cloudmesh/cloudmesh.yaml

Example
^^^^^^^


.. include: ../../cloudmesh_etc/cloudmesh.yaml


https://github.com/cloudmesh/client/blob/master/cloudmesh_etc/cloudmesh.yaml

Get Registration from India
----------------------------

::

   ./ssh/config

::

   Host india
       User: gregor
       Hostname: india.futuresystems.org

replace gregor with your portalname

this will be used by the register command

::

   cm register india

Will update your cloudmesh.yaml file with the information retrieved
from india. YOu must be able to loginto india before this command
works.

Check it with::

  ssh india uname -a

Location of file on india is::

  ~/.cloudmesh/clouds/india/juno/openrc.sh

Make sure you add a valid tennat to the file


Registration of clouds
-----------------------

See manual page ...

::

   cm register help

::

   register edit

::

   register list



