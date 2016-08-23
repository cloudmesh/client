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

A plugin repository consists of two components:

#. a name (namespace separated by dots (``.``))
#. a uri


The repository must be a valid python module.


Implementation
==============


#. ``cloudmesh.yaml`` should be modified to have a ``plugins``
  key. Each entry under ``plugins`` will be:

  - ``repos``: a list of repositories with ``name`` and ``uri``
    attributes.

  - ``plugins``: set of plugins keyed by the name of the plugin.

    Each plugin will have:

    - ``path``: location on the location filesystem a plugin has been
      ``fetch``\-ed to

    - ``installed``: ``yes`` or ``no``
