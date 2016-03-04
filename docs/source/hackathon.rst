Hackathon
==========


Install python 3.5 and 2.7.11
-----------------------------


Install 2.7.11
--------------

We have this documented elsewhere


Install 3.5
------------

Make sure you do an alternate install. Then use virtualenv -p to do
~/ENV2 and ~/ENV3 create alias in bashrc for ENV2 and ENV3

OSX
^^^^

Prerequisites:
^^^^^^^^^^^^^

Install python 3.5 package from:

* https://www.python.org/downloads/release/python-350/

Make sure it is installed in::

  /Library/Frameworks/Python.framework/Versions/3.5/bin

Steps to follow after making sure of the prerequisites:

.. prompt:: bash

  pip3.5 install --user virtualenv


Go to bash_profile and append the new path:


.. prompt:: bash

  vim ~/.bash_profile


Append String: `alias virtualenv3='~/Library/Python/3.5/bin/virtualenv'`

Change the alias of ENV to ENV2 in your bash_profile and update the
current terminal window

.. prompt:: bash

  source ~/.bash_profile


Usage:

create a directory with ENV3 and work on it.

.. prompt:: bash

  virtualenv3 ~/ENV3
  source ~/ENV3/bin/activate
  which python


This should display /Users/<username>/ENV3/bin/python


Windows
^^^^^^^^


Conversion
----------

Python 2 and 3 compatibility cheat sheet:

http://python-future.org/compatible_idioms.html


print:

.. code-block:: python

    from __future__ import print_function

    print('Hello')

raise:

.. code-block:: python

    raise ValueError("dodgy value")


traceback:

.. code-block:: python

    from future.utils import raise_

    traceback = sys.exc_info()[2]
    raise_(ValueError, "dodgy value", traceback)

    # we will need to create function for that as we want to control
    # with flag in db

exception:

.. code-block:: python

     except Exception as e:

integre division:

.. code-block:: python

    from __future__ import division

    assert 2 / 3 == 0

metaclass:

.. code-block:: python

    from future.utils import with_metaclass

    class Form(with_metaclass(FormType, BaseForm)):
        pass

strings:

.. code-block:: python

    from __future__ import unicode_literals

    s1 = 'The Zen of Python'

import:

.. code-block:: python

    all files will need

    from __future__ import absolute_import
    from __future__ import print_function


Dict
^^^^
Using dict heights = {'Fred': 175, 'Anne': 166, 'Joe': 192}
as an example

Iterable dict keys:

.. code-block:: python

    for key in heights:
        ...

Iterable dict values:

.. code-block:: python

    from builtins import itervalues
    for key in itervalues(heights):
        ...

Iterable dict items:

.. code-block:: python

    from future.utils import iteritems
    for (key, value) in iteritems(heights):
        ...

dict keys as a list:

.. code-block:: python

    keylist = heights.keys() NO!
    keylist = list(heights) YES!

dict values as a list:

.. code-block:: python

    from future.utils import itervalues
    valuelist = list(itervalues(heights))

dict items as a list:

.. code-block:: python

    from future.utils import iteritems
    itemlist = list(iteritems(heights))

dict comparison not supported any more!:

.. code-block:: python

    a = {"key":"value1"}
    b = {"key":"value2"}
    if a > b:     # NOT WORKING!!!
        DO SOMETHING!

File
^^^^
Open file to read:

.. code-block:: python

    f = file(pathname) NO!
    f = open(pathname) YES!

raw_input
^^^^

Getting raw input from keyboard:

.. code-block:: python

    name = raw_input('What is your name? ') NO!
    
    from builtins import input
    name = input('What is your name? ')
    YES!
