Comet Big Data Tutorial
=======================

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

.. code-block:: bash

   git clone --recursive git@github.com:cloudmesh/example-project-nist-fingerprint-matching.git

.. warning::

   Make sure to pass the ``--recursive`` flag else you will get errors
   further along in the process that will be hard to track down.


Next enter the repository and create a virtual environment

.. code-block:: bash

  cd example-project-nist-fingerprint-matching
  virtualenv venv
  source venv/bin/activate


Install the dependency next:

.. code-block:: bash

   pip install -r big-data-stack/requirements.txt


Deploy the Stack
----------------


Install the Dataset and Software
--------------------------------


Run the Analytics
-----------------


Find the Matches
----------------
