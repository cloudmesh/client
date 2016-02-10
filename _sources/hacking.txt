Hacking
=========

Contributing
------------

.. include:: ../../CONTRIBUTING   

Editor
------

Use PyCharam.

We made bad experience with people using editors other than emacs, vi, and PyCharm.
When working on Windows make sure your editor handles newlines properly with git.

Documentation
-------------

Creating the documentation with sphinx is easy

.. prompt:: bash

    pip install -r requirements-doc.txt
    make doc

View the documentation

.. prompt:: bash

   make view

Git
----

Closing Issues via Commit Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To close an issue on github issues, you can use it in your commit messages as follows

.. prompt:: bash

git commit -m "Fix problem xyz, fixes #12"


SSH keys
^^^^^^^^^

You can get a list of public ssh keys in plain text format by visiting:

https://github.com/{user}.keys
  
Sheetsheet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* https://github.com/tiimgreen/github-cheat-sheet
* https://training.github.com/kit/downloads/github-git-cheat-sheet.pdf
* http://byte.kde.org/~zrusin/git/git-cheat-sheet.svg
* http://www.emoji-cheat-sheet.com

Empty Commits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Commits can be pushed with no code changes by adding --allow-empty:

.. prompt:: bash

    git commit -m "Big-ass commit" --allow-empty


Styled Git Log
^^^^^^^^^^^^^^^^^

.. prompt:: bash
   
   git log --all --graph --pretty=format:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative


Tags
^^^^^

Tags are only created by Gregor von Laszewski.

Create a tag. Always use x.y.z

.. prompt:: bash

   make tag

Remove a tag

.. prompt:: bash

   make rmtag


Publish on Github
^^^^^^^^^^^^^^^^^

The documentation is only pushed by  Gregor von
Laszewski.

.. prompt:: bash

    make publish

Logging
^^^^^^^^

::

    from cloudmesh_client.common.LogUtil import LogUtil

    log = LogUtil.get_logger()
    log.info("Cloud: " + cloud + ", Arguments: " + str(arguments))
