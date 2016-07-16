Comet Big Data Tutorial
=======================

.. sidebar:: Page Contents

   .. contents::
      :local:


**Goal**: Run a fingerprint matching on a virtual cluster using Apache YARN, Spark, HBase and Drill.

**Time**: This will likely take several hours, though most will be spent waiting.

Status of this Tutorial
-----------------------

Work-in-progress

Problem Description
-------------------

Given a set of fingerprint images, partition them into two sets: "probe", and "gallery".
We want to compare each image in "probe" to those in "gallery" and compute a matching score.
We'll then need to query the results to select the matches with the highest score.

Stack
-----

The dataset provided by NIST is a collection of png images and
associated metadata.  Additionally, the Nist Biometric Image Software
(NBIS) provides the core components for processing the images: MINDTCT
for finding ridges and BOZORTH3 which does the actual matching.

Images and processing results will be stored in HBase.
Spark will be used as the computational engine.
Drill be use to query HBase using SQL.

Process Overview
----------------

1. Start a virtual cluster
2. Deploy the stack (ansible)
3. Install the dataset and NBIS software (ansible)
4. Run the analytics (spark)
5. Find the matches (drill)


Start a Virtual Cluster
---------------

Before we begin, make sure you have a virtual cluster.

You need:

- An IP address for all nodes
- The ability to SSH into each node
- Python 2.7 installed on each node


Requirements
------------

You will need on your local system:

- Python 2.7
- Pip
- Virtualenv
- GCC
- Git
- SSH Client

Setup
-----

First you'll need to download the deployment scripts. To do so you
will need an account on GitHub.com and an SSH public key associated
with your account. While ideally this should not be required, it is
currently an artifact of the repository organization: git submodules
are used in which git authenticates through SSH.

This may be fixed in a future version of this tutorial.

Start by navigating to some workspace and cloning the repository. 

.. code-block:: sh

   $ git clone --recursive git@github.com:cloudmesh/example-project-nist-fingerprint-matching.git

.. warning::

   Make sure to pass the ``--recursive`` flag else you will get errors
   further along in the process that will be hard to track down.


Next enter the repository and create a virtual environment

.. code-block:: sh

  $ cd example-project-nist-fingerprint-matching
  $ virtualenv venv
  $ source venv/bin/activate


Install the dependencies next:

.. code-block:: sh

   $ pip install -r big-data-stack/requirements.txt


Deploy the Stack
----------------

At this point you should have your virtual cluster up and running.
Make sure you can ssh into each node.

For reference, ``$VC_USER`` stands for the username that may ssh into
the nodes (this has to be the same for each node).  If you want to
avoid passing in ``-u $VC_USER`` to ansible each time, edit the
``ansible.cfg`` file and set ``remote_user``. The default is
``ubuntu``.

Now we need to generate the Ansible inventory and host_vars so we can
deploy the stack.  The deployment code is provided in the
``big-data-stack`` submodule, so change directories in there.  Use the
``mk-inventory`` script to generate the inventory.


You will need to give a name to your virtual cluster and pass in the
ip addresses.  In the example below, the name is ``myvc`` and the
nodes are running on 192.168.1.100 through .102.


.. code-block:: sh

   $ python mk-inventory -n myvc 192.168.1.100 192.168.1.101 192.168.1.102 >inventory.txt


You'll see something like::

  WARNING   Creating directory ./host_vars
  INFO      Writing host_vars to ./host_vars
  INFO      Writing ./host_vars/myvc0
  INFO      Writing ./host_vars/myvc1
  INFO      Writing ./host_vars/myvc2


You should inspect the ``inventory.txt``, which should look like this::

  [namenodes]
  myvc0
  myvc1

  [resourcemanagernodes]
  myvc0
  myvc1

  [datanodes]
  myvc0
  myvc1
  myvc2

  [zookeepernodes]
  myvc0
  myvc1
  myvc2

  [hadoopnodes]
  myvc0
  myvc1
  myvc2

  [historyservernodes]
  myvc2

  [journalnodes]
  myvc2
  myvc1
  myvc0

  [frontendnodes]
  myvc2



To make sure that ansible can execute properly, you should have ansible ping the nodes:


.. code-block:: sh

   $ ansible all -o -m ping -u $VC_USER


You should see something like this::

  myvc2 | SUCCESS => {"changed": false, "ping": "pong"}
  myvc1 | SUCCESS => {"changed": false, "ping": "pong"}
  myvc0 | SUCCESS => {"changed": false, "ping": "pong"}


.. tip::

   Depending on the network, the nodes, and other factors, it may take
   a bit before this succedes. I usually execute the following in the
   shell while waiting::

     until ansible all -o -m ping; do echo date; sleep 5; done


At this point you should be ready to deploy the stack. As a sanity check, make sure:

- ``ansible all -m ping -u $VC_USER`` works
- you should have monotonically increasing integers as values for
  ``zookeeper_id`` in ``host_vars/myvcN`` (where ``N`` is the node id).
- make sure you cloned originally with ``--recursive``. Only pain and
  misery await if you forgot.  A symptom that you forgot is that the
  subdirectories of the ``roles`` directory are empty. They should not
  be empty.  Do an ``ls roles/*`` and if any of the role directories
  are empty, you forgot ``--recursive``.


If your sanity checks succeeded you run the following.  This will
deploy hadoop (HDFS and YARN with automatic failover), and Apache
Spark, Apache HBase, and Apache Drill.


.. code-block:: sh

   $ time ansible-playbook -u $VC_USER play-hadoop.yml addons/spark.yml addons/hbase.yml addons/drill.yml


.. tip::

   This will take about 45 minutes.


Install the Dataset and Software
--------------------------------

If all went well, you should see OK's in green and no red in the output of ``ansible-playbook``.

Next you can deploy the fingerprint images and analysis software to the cluster:

.. code-block:: sh

   $ time ansible-playbook -u $VC_USER ../dataset.yml ../software.yml


.. tip::

   Wait a while longer


Run the Analytics
-----------------


Find the Matches
----------------
