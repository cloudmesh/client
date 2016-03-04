Hackathon
==========


Install python 3.5 and 2.7.11
-----------------------------


Install 2.7.11
--------------

We have this documented elsewhere


Install 3.5
------------

Make sure you do an alternate install. Then use virtualenv -p to do ~/ENV2
and ~/ENV3
create alias in bashrc for ENV2 and ENV3

OSX
^^^^

Prerequisites:
^^^^^^^^^^^^^

Install python 3.5 package from:
    https://www.python.org/downloads/release/python-350/

Make sure it is installed in /Library/Frameworks/Python.framework/Versions/3
.5/bin


Steps to follow after making sure of the prerequisites:

.. prompt:: bash

  pip3 install --user virtualenv


Go to bash_profile and append the new path:


.. prompt:: bash

  vim ~/.bash_profile


Append String: `alias virtualenv3='~/Library/Python/3.4/bin/virtualenv'`

Change the alias of ENV to ENV2 in your bash_profile and update the current
terminal window

.. prompt:: bash

  source ~/.bash_profile


Usage:

create a directory with ENV3 and work on it.

.. prompt:: bash

  virtualenv3 ~/ENV3
  source ~/ENV3/bin/activate
  cd ENV3/


Windows
^^^^^^^^


Conversion
----------



Conversion
----------

Python 2 and 3 compatibility cheat sheet:

http://python-future.org/compatible_idioms.html

