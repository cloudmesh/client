Hacking
=========

Contributing
------------

.. include:: ../../CONTRIBUTING   


Git
----

Closing Issues via Commit Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To close an issue on github issues, you can use it in your commit messages as follows::

  git commit -m "Fix problem xyz, fixes #12"


SSH keys
---------

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

$ git commit -m "Big-ass commit" --allow-empty


Styled Git Log
^^^^^^^^^^^^^^^^^

::
   
   git log --all --graph --pretty=format:'%Cred%h%Creset -%C(auto)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
