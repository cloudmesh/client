Developers Manual
=================

Editor
------

Use PyCharam.

We made bad experience with people using editors other than emacs, vi, and PyCharm. When working on Windows make sure your editor handles newlines properly with git.

Tags
----

Create a tag. Always use x.y.z

::

   make tag

Remove a tag
   
::

   make rmtag

Documentation
-------------

::

   make doc

View the documentation

OSX

::

   open docs/build/html/index.html

Other::

   firefox docs/build/html/index.html

Publish on Github
^^^^^^^^^^^^^^^^^

TBD with ghp-import
