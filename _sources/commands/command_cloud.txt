Cloud Command
======================================================================

The cloud command provides an API that allows users to login to
a cloud, activate a cloud, deactivate a cloud & logout from a cloud.

The manual page of the `sync` command can be found at: 
`cloud <../man/man.html#cloud>`_


List status of all clouds
--------------------------

To list status of all clouds registered in the
cloudmesh.yaml file use:

.. prompt:: bash, cm>  

	    cloud list

::
   
    +----+---------------+---------+--------+------------+--------+
    | id | Cloud         | Default | Active | Status     | Key    |
    +----+---------------+---------+--------+------------+--------+
    | 0  | cm            |         | *      | Logged Out | albert |
    | 1  | kilo          | *       | *      | Logged Out | albert |
    | 2  | chameleon     |         |        | Logged Out | albert |
    | 3  | cybera-c      |         |        | Logged Out | albert |
    | 4  | cybera-e      |         |        | Logged Out | albert |
    | 5  | aws           |         |        | Logged Out | albert |
    | 6  | chameleon-ec2 |         |        | Logged Out | albert |
    | 7  | azure         |         |        | Logged Out | albert |
    +----+---------------+---------+--------+------------+--------+


Login to a single/multiple clouds
----------------------------------

To logon to a cloud use:

.. prompt:: bash, cm>  
  
  cloud logon kilo

::
   
    Logged into cloud: kilo

You can logon to multiple clouds:

.. prompt:: bash, cm>
	    
   cloud logon kilo

::

   Logged into cloud: kilo

.. prompt:: bash, cm>

  cloud list

::
   
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | kilo       | Active     |
    +------------+------------+

.. warning:: logon does not give error but after that the status in
'cloud list' does not show the cloud as 'Active'. Maybe a duplication
when we have a new column 'Active' in addition to 'Status'?

Deactivate a cloud
-------------------

To deactivate a cloud use:

.. prompt:: bash, cm>
	    
  cloud deactivate kilo

::
   
  Deactivated cloud: kilo

.. prompt:: bash, cm>
	    
  cloud list

::
   
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | kilo       | Inactive   |
    +------------+------------+

Activate a cloud
-----------------

To activate a cloud use:

.. prompt:: bash, cm>
	    
  cloud activate kilo

::
   
  Activated cloud: kilo

.. warning:: KeyError: 'kilo' when trying to deactivate kilo

.. prompt:: bash, cm>
	    
  cloud list

::

    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | kilo       | Active     |
    +------------+------------+

Log out from a cloud
---------------------

To log out from a cloud use:

.. prompt:: bash, cm>
	    
  cloud logout kilo

::
   
  Logged out of cloud: kilo

.. prompt:: bash, cm>
	    
  cloud logout kilo

::
   
  Logged out of cloud: kilo

.. prompt:: bash, cm>  
  
  cloud list

::
      
    +------------+------------+
    | cloud name | status     |
    +------------+------------+
    | aws        | Logged Out |
    | azure      | Logged Out |
    | chameleon  | Logged Out |
    | kilo       | Logged Out |
    +------------+------------+

.. warning:: Logged out in 'Status' column and the 'Active' column may
be duplicated and conflicting with each other.
