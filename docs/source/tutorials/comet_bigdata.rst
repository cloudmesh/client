Comet Big Data Tutorial
=======================

.. sidebar:: Page Contents

   .. contents::
      :local:


**Goal**: Deploy an analytics cluster and run spark examples.

**Time**: < 1 hour

Status of this Tutorial
-----------------------

Work-in-progress

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


Preparation
-----------

On your head node clone the Big Data Stack repository

::

   head $ git clone git://github.com/cloudmesh/xsede17
   head $ cd xsede17

Next create a virtualenvironment and install dependencies:

::

   head $ virtualenv ~/BDS
   head $ source ~/BDS/bin/activate
   (BDS) head $ pip install -r requirements.txt

Next you need to configure ansible to use the internal network interface.
Do so by setting the ``bds_internal_iface`` to ``ens3`` in ``group_vars/all.yml``

::

   (BDS) head $ nano group_vars/all.yml


You will also need to configure authentication. Edit ``ansible.cfg``
and ensure the following are set in the ``[defaults]`` section:

- ``remote_user=nbdraadmin``
- ``become_ask_pass=True``

::

   (BDS) head $ nano ansible.cfg

Finally, generate the ansible inventory file using your cluster IP
addresses. Note, your IP addresses may be different.

::

   (BDS) head $ python mk-inventory -n bds- 10.0.0.1 10.0.0.2 >inventory.txt


Sanity Check
------------

At this point you should be good to go, but make sure that Ansible is
correctly configured by pinging the cluster.

::

   (BDS) head $ ansible all -m ping
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

   (BDS) head $ ansible-playbook play-hadoop.yml addons/spark.yml


Usage
-----

Once the stack has been deployed you may log in to the first address
you passed to ``mk-inventory`` and switch to the ``hadoop`` user.

::

   (BDS) head $ ssh 10.0.0.1
   nbdraadmin@bds-0 $ sudo su - hadoop
   hadoop@bds-0 $


Word Count
---------

You can download the complete works for Shakespeare and upload it to
HDFS:

::

   hadoop@bds-0 $ curl https://ocw.mit.edu/ans7870/6/6.006/s08/lecturenotes/files/t8.shakespeare.txt >shakespeare.txt
   hadoop@bds-0 $ hadoop fs -put shakespeare.txt /

Next, you can use the following program (adapted from the `Spark
website <https://spark.apache.org/examples.html>_`) to analyze
Shakespeare's works. The analysis consists of the following steps:

#. split the text into words
#. reduce by counting each words
#. sort the result in descending order
#. save to results on HDFS

::

   from pyspark import sparkcontext

   sc = sparkcontext()

   txt = sc.textfile('hdfs:///shakespeare.txt')
   counts = txt.flatmap(lambda line: line.split(" ")) \
               .map(lambda word: (word, 1)) \
               .reducebykey(lambda a, b: a + b) \
               .sortBy(lambda t: t[1], ascending=False)
   counts.saveAsTextFile('hdfs:///shakespeare-wordcount.txt')


Save this as spark-shakespeare.py.

You can run the analysis locally with the following invocation:

::

   hadoop@bds-0 $ spark-submit spark-shakespeare.py


You can then view the top ten words by:

::

   hadoop@bds-0 $ hadoop fs -cat /shakespeare-wordcount.txt/part-00000 | head


Further Work
------------

We leave it as an exercise any further refinement of the analysis
method. Some suggestions include:

- removing ancillary text (eg "ACT", "SCENE", character or location names, etc)
- licensing information
- paragraph numbers
- effects of punctuation
