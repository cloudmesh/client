===================
 Cloudmesh Plugins
===================

About
=====

This document describes the plugin mechanism.


Status
======

DRAFT


Plugins
=======

A plugin extends the Cloudmesh shell by providing additional commands
to accomplish specific tasks. For example, managing clouds, networks,
etc are implemented as plugins which are called from the main
cloudmesh shell.

The plugin mechanism provides for these operations:

- fetch / unfetch: download the plugin from a remote repository
- install / uninstall: modify the shell so that the plugin is visible
- load / unload: make the plugin usable in the current shell
- repoadd / reporm: add a plugin repository


Repository
==========

A repository allows a collection of plugins to be accessed under an
namespace. Conceptually, a repository is a directory where the plugins
are the python modules contained therin.

A plugin repository is defined by two components:

#. a name (namespace separated by dots (``.``))
#. a uri


Implementation
==============

#. ``cloudmesh.yaml`` should be modified to have a ``plugins``
  key. Each entry under ``plugins`` will be:

  - ``prefix``: path on the local machine wherein the plugins are installed.

  - ``repos``: a list of repositories with ``name`` and ``uri``
    attributes.

  - ``plugins``: a list of plugins keyed by the name of the plugin.

    Each plugin will have:

    - ``repo``: the name of the repository containing this plugin


Semantics
=========


``repoadd``
-----------


``reporm``
----------


``fetch``
---------


``unfetch``
-----------


``install``
-----------


``uninstall``
-------------


``load``
--------


``unload``
----------



Examples
========


In ``cloudmesh.yaml``
--------------------------------


.. code-block:: yaml

   plugins:
     prefix: ~/.cloudmesh/plugins
     repos:
       - name: cloudmesh
         uri: git://github.com/cloudmesh
       - name: badi
         uri: git://github.com/badi
       - local:
         uri: file://.src/cloudmesh_plugins
     plugins:
       - foo:
           repo: cloudmesh
       - bar:
           repo: badi
       - bar:
           repo: local
