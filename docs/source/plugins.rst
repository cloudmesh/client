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

- install / uninstall: modify the shell so that the plugin is visible
- repoadd / reporm: add a plugin repository
- update: updates the named plugins (or all)
- fetch / unfetch: download the plugin from a remote repository
- load / unload: make the plugin usable in the current shell
- list: list the plugins available, installed, and loaded


Use Cases
=========

Example A
---------

Say a git repository exists that provides a collection of plugins.
For example, this repository has the URI::

  git://github.com/example.git

This ``example.git`` repository consists of the following plugins:

- ``foo.bar``
- ``foo.baz``
- ``qux.wabbit``


Adding repositories
~~~~~~~~~~~~~~~~~~~

In order to make these plugins available, ``$USER`` can execute the following:

::

   $ cm plugin repoadd git://github.com/example.git


This names the repository as ``example``, and each plugin within
``example`` is uniquely identified as ``<reponame>.<module>``.


Getting info about repos and plugins
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At this point ``$USER`` may wish to list the available plugins in the
``example`` repository:

::

   $ cm plugin info example
   Name: example
   State: none
   Modules:

    example.foo.bar         -- runs bar in the foo context
    example.foo.baz         -- runs baz in the foo context
    example.qux.wabbit      -- shhhh...hunting wabbits



If ``$USER`` then wishes to lookup further information on a particular
module, they could execute:

::

   $ cm plugin info example.qux.wabbit
   * Module
     qux.wabbit

   * Repository
     name: example
     uri:  git://github.com/example.git

   * Description
     shhhh...hunting wabbits

     This engages the Elmer Fudd Engin (EFE), whose effect is to so
     sow chaos and search for points of failure.

   * Requirements
     - requirement 1
     - requirement 2
     - etc

   * Assumptions
     - assumption 1
     - assumption 2
     - etc

   * Examples

     Description of Example 1

     example 1


     Description of Example 2

     example 2



Installation
~~~~~~~~~~~

Desiring to use the ``qux.wabbit`` plugin, ``$USER`` can install it
like so:

::

   $ cm plugin install example.qux.wabbit


Using the plugin
~~~~~~~~~~~~~~~~

Now that the plugin is installed it is available for use.
There are two ways of referring to the module when calling it:

- unambiguously by providing the fully qualified name::

    $ cm example.qux.wabbit --help

- ambiguously by omiting parts of the fully qualified name.

  For example::

    $ cm wabbit --help

  Or::

    $ cm qux.wabbit --help


If ambiguity exists in the currently loaded plugins (e.g. other
plugins exists with similar names), this is considered and error and
``$USER`` will be notified.

::

   $ cm wabbit --help
   ERROR: ambiguous name `wabbit` may refer to one of:
     - example.qux.wabbit
     - other.hello.wabbit

   Please use a less ambiguous reference.
  



Specification
=============

Repository
----------

A REPOSITORY is identified by a NAME, URI pair.  The NAME identifies
the REPOSITORY to the local system and can be any string of
alphanumeric characters.

Valid URI schemes are:

- `git:// <https://www.iana.org/assignments/uri-schemes/prov/git>`_: references a git repository as clonable by ``git clone git://...``
- `file:// <https://tools.ietf.org/html/rfc1738>`_: references a directory on accessible on the local system
- `http:// <https://tools.ietf.org/html/rfc7230#section-2.7.1>`_,
  `https:// <https://tools.ietf.org/html/rfc7230#section-2.7.2>`_,
  `ftp:// <https://tools.ietf.org/html/rfc1738>`_: references remote
  directory structures than can be retrieved recursively using
  ``wget`` available over the HTTP, HTTPS, and FTP protocols
  (respecitvely).
- `ssh:// <https://www.iana.org/assignments/uri-schemes/prov/ssh>`_:
  references a directory structure that can be copied to the local
  machine using the ``scp`` command.



Structure
~~~~~~~~~

A REPOSITORY is a directory with PLUGINs as subdirectories.



Plugin
------


A PLUGIN is a directory that may be interpreted as a Python module.
There must be an ``__init__.py`` file that has the following top-level definitions:

- ``__doc__``: multiline string`
- ``Plugin``: class implementing the plugin


Defining ``__doc__``
~~~~~~~~~~~~~~~~~~~~

``__doc__``: a multiline string describing the plugin.
- The first line should be a brief summary, ideally less than 70
  characters.

- The second line is blank

- The third line and after provides the rest of the documentation


Defining ``Plugin``
~~~~~~~~~~~~~~~~~~~

``Plugin`` is a class implementing the plugin
functionality. The API for ``Plugin`` mandates fulfilling two requirements:

#. ``__init__(self, context)``: a single-argument
   constructor accepting the context in which the plugin is
   called. This include configuration, global state, etc.

#. ``__cm_plugin_main(self, args, arguments)``: the main entry point
   into the plugin. This method should be documented using
   docopts. ``args`` and ``arguments`` contained the arguments parsed
   according the the ``docopt``\-parsing of the ``__cm_plugin_main``
   method's ``__doc__`` attribute.






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
