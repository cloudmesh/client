Upgrade
=======

Once in a while we will be upgrading the cloudmesh client. Such upgrade may require the replacement of the cloudmesh yaml file and the database. Thus an upgrade is only recommended after you have shut down all your VMs.

.. note:: However an upgarde is also possible while you have vms running, but you may loose information
          about groups and anything that is stored in the database such as variables and defaults.
	  As you see from this comment we strongly suggest to complete your current experiments and
	  start fresh so you do not lose some information

To conduct an upgrade we recommend that you make a backup of the following files while at the same time moving them out of the way::

  mv ~/.cloudmesh.yaml ~/.cloudmesh.yaml.bak.1
  mv ~/.cloudmesh.db ~/.cloudmesh.db.bak.1

Now you can get a new version of cloudmesh from either source, or pypi as described in the setup section.
After that starting cloudmesh with the `cm` command you can than copy the relevant portions into the new cloudmesh.yaml file. Please make sure that the indentation is done properly. For the database file you do not have to do anything. It will be created for you. However backwards compatibility to previous versions of the database is not maintained. 



	  
