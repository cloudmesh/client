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
- list: list the plugins available, installed, and loaded
- update: updates the named plugins (or all)


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

::

   repoadd [-f | --force] <name> <uri>


Addes the repository at ``uri`` as ``name``.


``reporm``
----------

::

   reporm [-f | --force] <name>


Removes the repository given by ``name``.
If the repo does not exists this will result in a non-zero exit code.
Specify ``-f`` to indicate that this should not be an error.


``fetch``
---------

::

   fetch [-f | --force]  <name> [...<name>]


Downloads the plugin named ``name``.
``name`` can either be the fully qualified name in the form ``repository.plugin`` or bare (eg ``plugin``).
If the bare form is used, the name must be unique.
If the ``name`` is not unique an error message will be displayed and exit with non-zero return code.

If the plugin has already been fetched, then this command will have no effect.
Specify the ``-f`` flag in order to force a download and replacement of any preexisting plugin.


``unfetch``
-----------

::

   unfetch <name> [...<name>]


Removes the plugin from the local system.
Has no effect if the plugin does not exist.


``install``
-----------

::

   install <name> [...<name>]


Ensures that the plugin is both ``fetch``\-ed and ``load``\-ed.


``uninstall``
-------------

::

   uninstall <name> [...<name>]


Ensures that the plugin is both ``unload``\-ed and ``unfetch``\-ed.


``load``
--------

::

   load <name> [...<name>]


Makes the plugin available for use.


``unload``
----------

::

   unload <name> [...<name>]


Removes the plugin from usage, but does not remove it from the system.


``list``
--------

::

   list [-f format] [-i] [-l] [-a]

   -f  --format  FORMAT    display format where FORMAT is one of "json", "yaml", "csv", "pretty"
   -i  --installed         list installed plugins
   -l  --loaded            list loaded plugins
   -a  --available         list available plugins


``update``
----------

::

   update [<name>...]


Updates the plugins to the most recent version by

#. updating the repository
#. refetching the pluging
#. reloading (if the plugin is already loaded)



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
