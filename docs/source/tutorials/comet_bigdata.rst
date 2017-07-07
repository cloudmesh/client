Comet Big Data Tutorial
=======================

.. sidebar:: Page Contents

   .. contents::
      :local:


**Goal**: Deploy an analytics cluster and run spark examples.

**Time**: ~ 15 min

Status of this Tutorial
-----------------------

Released for PEARC17 Comet VC Tutorial

Overview
--------

In this tutorial you will deploy an analytics stack consisting of
Hadoop and Spark and run some toy analyses on the cluster.


Requirements
------------

- Basic knowledge of git, shell scripting, and Python.
- A Comet cluster

  - ip addresses of the nodes
  - ssh-reachable user with admin privileges


.. note:: This tutorial used `vct01` as an example. Please change to your cluster name.

Preparation
-----------

On your VC front-end node clone the Big Data Stack repository:

::

   FE $ git clone --recursive --branch pearc17 git://github.com/futuresystems/big-data-stack
   FE $ cd big-data-stack

Next create a virtualenvironment and install dependencies:

::

   FE $ virtualenv ~/BDS
   FE $ source ~/BDS/bin/activate
   (BDS) FE $ pip install -r requirements.txt

The proper interla network interface has been set for this tutorial. For general
case, you may need to configure ansible to use the internal network interface.
Do so by setting the ``bds_internal_iface`` to ``ens3`` in ``group_vars/all.yml``

The ansible remote_user has been set properly for this tutorial assuming you
followed all the previous steps to setup the VC. For general use, please make
sure to configure the authentication. Edit ``ansible.cfg``
and ensure the following are set in the ``[defaults]`` section:

- ``remote_user=YOUR_COMPUTE_USERNAME``
- ``become_ask_pass=True``

Finally, generate the ansible inventory file using your cluster IP
addresses. Note, your IP addresses may be different.

::

   (BDS) FE $ python mk-inventory -n bds- 10.0.0.1 10.0.0.2 >inventory.txt


Sanity Check
------------

At this point you should be good to go, but make sure that Ansible is
correctly configured by pinging the cluster.

::

   (BDS) FE $ ansible all -m ping
   bds-0 | SUCCESS => {
     "changed": false, 
     "ping": "pong"
   }
   bds-1 | SUCCESS => {
     "changed": false, 
     "ping": "pong"
   }


Deploy the Stack
----------------

Once you've prepared your head node and generated the inventory you
can deploy Hadoop, Spark, and optionally other addons. The addons are
available in the ``addons`` directory, and include packages such as
Apache Drill, HBase, and others. For this tutorial we will only need
Spark.

The following command will deploy Hadoop and Spark using Ansible. This
will take several minutes.

::

   (BDS) FE $ ansible-playbook -K pearc17.yml


Usage
-----

Once the stack has been deployed you may log in to the first address
you passed to ``mk-inventory`` and switch to the ``hadoop`` user.

::

   (BDS) FE $ ssh vm-vct01-00
   comet@vm-vct01-00 $ sudo su - hadoop
   hadoop@vm-vct01-00 $


Word Count
---------

You can download the complete works for Shakespeare and upload it to
HDFS:

::

   hadoop@vm-vct01-00 $ wget https://raw.githubusercontent.com/cloudmesh/cloudmesh.comet.vcdeploy/master/examples/shakespeare.txt
   hadoop@vm-vct01-00 $ hadoop fs -put shakespeare.txt /

Next, you can use the following program (adapted from the `Spark
website <https://spark.apache.org/examples.html>`_) to analyze
Shakespeare's works. The analysis consists of the following steps:

#. split the text into words
#. reduce by counting each words
#. sort the result in descending order
#. save to results on HDFS

::

   from pyspark import SparkContext

   sc = SparkContext()

   txt = sc.textFile('hdfs:///shakespeare.txt')
   counts = txt.flatMap(lambda line: line.split(" ")) \
               .map(lambda word: (word, 1)) \
               .reduceByKey(lambda a, b: a + b) \
               .sortBy(lambda t: t[1], ascending=False)
   counts.saveAsTextFile('hdfs:///shakespeare-wordcount.txt')

You can download this example by running this:

::

   hadoop@vm-vct01-00 $ wget https://raw.githubusercontent.com/cloudmesh/cloudmesh.comet.vcdeploy/master/examples/spark-shakespeare.py

You can run the analysis locally with the following invocation:

::

   hadoop@vm-vct01-00 $ spark-submit spark-shakespeare.py


Or you can submit to the cluster by invoking:

::

   hadoop@vm-vct01-00 $ spark-submit --master yarn --deploy-mode cluster spark-shakespeare.py


**Make sure to cleanup** before rerunning otherwise the task will fail:

::

   hadoop@vm-vct01-00 $ hadoop fs -rm -r /shakespeare-wordcount.txt


You can then view the top ten words by:

::

   hadoop@vm-vct01-00 $ hadoop fs -cat /shakespeare-wordcount.txt/part-00000 | head


What's next?
------------

- Try with a larger data set and compare the performance between local run and cluster run
- Try with more sophisticated textual analytics
- Deploy other components. This tutorial is tailored specially for the PEARC17 Comet VC tutorial to minimize user intervention and customization while showing the essence of the big data stack deployment. For the general use, please refer to the `main repo <https://github.com/futuresystems/big-data-stack>`_.

