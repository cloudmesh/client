
=====
Stack
=====

.. sidebar:: Page Contents

   .. contents:: :local:
   

Questions
==========

do we need a yaml file where we add location of different repos that
integrate into cm/stack/....?

stack:
   hadoop:
     repo: ....
     branch: ...
     version: ...
     icon: ...
     parameters:
        ... see old launcher ...
   pig:
     repo: ....
     branch: ...
     version: ...
     icon: ...
   ...
   
About BDS
=========

BDS is a collection of Ansible playbooks to deploy a stack of data
analytics software. The current development version of BDS can be fond
online here:
https://github.com/futuresystems/big-data-stack/tree/unstable



BDS Requirements
----------------

- Python 2.7
- Virtualenv
- Pip
- Git
- ssh client
- ssh-keys in github (currently a bug and needs to be fixed)
- IP address of nodes to be controlled with privileged ssh user


Using BDS
---------

BDS is not a Python library or program and therefore cannot be
installed using pip or other tools. It currently works by:

#. ``git clone`` the bds repository
#. ``./mk-inventory`` with the IP address to create the inventory file
#. ``ansible-playbook play-hadoop.yml addons/...`` to install hadoop and any addons



Integrating BDS with Cloudmesh Client
=====================================


Proposed CM commands
--------------------

#. ``cm stack install``
#. ``cm stack``
#. ``cm hadoop``


``cm stack install``
~~~~~~~~~~~~~~~~~~~~

Will install BDS into cloudmesh so it is conveniently accessible.

   
   
``cm stack``
~~~~~~~~~~~~

``cm stack`` provides the low-level tools to manage the BDS. This include:

- check: sanity-checking to ensure the all requirements are complete
- cloning and updating the local cache of BDS
- creating and setting up a clone of BDS for the current project/deployment
- deploying software onto pre-configured nodes


``cm hadoop``
~~~~~~~~~~~~~

``cm hadoop`` wrap several steps in order to deploy a virtual cluster. This includes:

#. starting the machines on various providers (EC2, Chameleon, FutureSystems, etc)
#. using ``cm stack`` to initialize, sanity check, and configure current project
#. deploy software using ``cm stack``


Use Case: Hadoop with Spark, HBase, Drill
-----------------------------------------

This should be achievable with a single line::

  $ cm hadoop \
      --nodes 5 \
      --on chameleon \
      --with spark hbase drill \
      --define spark_version=1.7.0 spark_package_type=src


This will:

- start 5 nodes (``--nodes 5``) on the chameleon cloud (``--on chameleon``)
- install and hadoop
- install and configure the apache spark, hbase, and drill packages
- override ansible variables ``spark_version`` and ``spark_package_type`` (NOTE: the values passed must be supported by BDS).



Implementation Overview
=======================

This section describes possible implementation approaches


Sanity Check ``cm stack sanity-check``
----------------------------------

Example success::

  $ cm stack check
  python.......OK
  virtualenv...OK
  pip..........OK
  ansible......OK
  git..........OK
  ssh..........OK
  github.......OK


Example failure::

  $ cm stack check
  python.......OK
  virtualenv...OK
  pip..........FAILED
  ansible......FAILED
  git..........OK
  ssh..........OK
  github.......FAILED

  The following errors were detected:

  * Pip is not installed correctly
    > `pip` not found in $PATH
  * Ansbile is not installed correctly
    > `ansible` related commands not found in $PATH
  * Authentication to github.com failed
    > did you add your public key to https://github.com/settings/ssh?


``cm stack check`` MUST:

- verify that the python ecosystem and ansbile are installed. Do this
  by ensuring that the the following commands are in the ``$PATH`` and
  checking versions if applicable:

  - ``python`` (must be 2.7)
  - ``virtualenv``
  - ``pip``
  - ``ansible``
  - ``ansible-playbook``
  - ``ansible-vault``
  - ``git``
  - ``ssh``

- verify that keys are added to github. Do this by ensuring that the following command exits with 1::

    $ ssh -T git@github.com
    Hi badi! You've successfully authenticated, but GitHub does not provide shell access.
    $ echo $?
    1




Initialization ``cm stack init``
--------------------------------


Example::

  $ cm stack init --branch unstable --user ubuntu 10.0.0.10 10.0.0.11 10.0.0.12


``cm stack init`` MUST:

- accept ``--branch <branchname>`` to specify the branch name of the repository (eg ``master`` [default], ``unstable``)

- accept ``--user <username`` to specify the ssh-login username on the nodes. This user MUST have privileges to manage the node.

- accept a list of IP addresses as the nodes to control

- accept ``--name <project name>`` to specify the name of this project. It not given, a default one must be chosen or generated. This project name is referred to below as ``$PROJ``

.. note::

   ``.cloudmesh`` refers to ``$HOME/.cloudmesh`` or
   ``$PWD/.cloudmesh``, or wherever the ``.cloudmesh`` directory is
   found.

.. note::

   ``$BDS`` below refers to ``.cloudmesh/stack/bds``

- clone BDS from github to a local cache directory. This should be in ``$DBS/cache/bds.git``.

- clone ``$BDS/cache/bds.git`` to ``$BDS/projects/$PROJ`` and checkout the branch that ``$BDS/cache/bds.git`` was on (default) or switch to the branch specified by ``--branch``.

- within ``$BDS/projects/$PROJ`` run ``./mk-inventory -n $USER-$PROJ $IP1 $IP2 ... >inventory.txt`` where ``$IPN...``  is the list of ip addresses and ``$USER`` is the username of the owner of the local machine.

- write the following information to ``$BDS/projects/$PROJ/.cloudmesh.yml``:

  - the parameter of ``--user``
  - the list of ip addresses

  This will allow other programs to inspect properties about this specific project
    

Listing Stacks ``cm stack list``
--------------------------------

Example::

  $ cm stack list
  Deployment Stacks
  - BDS (<version or branchname>)  ~/.cloudmesh/stack/bds/cache/bds.git

  Projects
  - > foo    [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/foo
  -   test-1 [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/test-1
  -   p1     [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/p1
  -   p2     [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/p2


``cm stack list`` provides an interface to list the deployment stacks (eg BDS or others) and all the projcts using a stack.

``cm stack list`` MUST:

- accept ``--sort <field>`` where ``field`` can be ``date``, or ``stack``, or ``name`` (default: ``date``

- accept ``--list <field,...>`` to list a subset of (``stack``, ``project``)

- accept ``--json`` which will cause the output to be rendered using json so that other programs may easity parse the output


Switching Projects ``cm stack project``
---------------------------------------

Example::

  $ cm stack list --list project
  Projects
  -   test-1 [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/test-1
  - > p1     [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/p1
  

  $ tm stack project
  p1

  $ cm stack project test-1
  Switched to project `test-1``

  $ cm stack project
  test-1

  $ cm stack list --list project
  Projects
  - > test-1 [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/test-1
  -   p1     [<stack name eg BDS>]  [<date created>]     ~/.cloudmesh/stack/projects/p1





Deploying Onto Nodes ``cm stack deploy``
----------------------------------------


Example::

  $ cm stack project
  p1

  $ cm stack deploy bds \
      --plays play-hadoop.yml addons/spark.yml addons/hbase.yml \
      --define spark_version=1.7.0 
  Verifying that nodes are reachable...........OK
  Deploying play-hadoop.yml....................OK
  Deploying addons/spark.yml...................OK
  Deploying addons/hbase.yml...................OK

  Done.



#. ``os.chdir($BDS/project/$PROJ)``
#. Verify nodes are reachable: ``until ansible all -m ping -u <username>; do sleep 5; done``
#. Deploy hadoop: ``ansible-playbook play-hadoop.yml -e spark_version=1.7.0``
#. Deploy spark: ``ansible-playbook addons/spark.yml -e spark_version=1.7.0``
#. Deploy hbase: ``ansible-playbook addons/hbase.yml -e spark_version=1.7.0``


Deploying Hadoop with Addons ``cm hadoop``
------------------------------------------


Example::

  $ cm hadoop --nodes 5 --on chameleon --with spark hbase drill
