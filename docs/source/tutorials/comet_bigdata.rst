Comet Big Data Tutorial
=======================

Goal: Run a fingerprint matching on a virtual cluster using Apache YARN, Spark, HBase and Drill.
Time: This will likely take several hours, though most will be spent waiting.

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
1. Deploy the stack (ansible)
1. Install the dataset and NBIS software (ansible)
1. Run the analytics (spark)
1. Find the matches (drill)


Start a Virtual Cluster
---------------

Before we begin, make sure you have a virtual cluster.

You need:

- An IP address for all nodes
- The ability to SSH into each node
- Python 2.7 installed on each node


Deploy the Stack
----------------


Install the Dataset and Software
--------------------------------


Run the Analytics
-----------------


Find the Matches
----------------
