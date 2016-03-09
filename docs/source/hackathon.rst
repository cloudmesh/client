Using python 2 and 3 for development
====================================

Install python 3.5 and 2.7.11
-----------------------------


Then use virtualenv -p to do
~/ENV2 and ~/ENV3 create alias in bashrc for ENV2 and ENV3

OSX
^^^^

We assume that you have downloaded and installed both python packages for 2.7.11 and 3.5
while getting them from

http://python.org

Make sure you have both versions installed:

.. prompt:: bash

  $ ls /Library/Frameworks/Python.framework/Versions/3.5/bin
  $ ls /Library/Frameworks/Python.framework/Versions/2.7/bin


Next you may run outdated versions of pip that you need to update and install virtualenv::

.. prompt:: bash

    pip3.5 install pip -U
    pip3.5 install --user virtualenv
    pip2.7 install pip -U
    pip2.7 install --user virtualenv

Edit the  bash_profile with your prefered editor and append some useful aliasses:

.. prompt:: bash

  emacs ~/.bash_profile

Append the following aliasses::

    alias virtualenv3='~/Library/Python/3.5/bin/virtualenv'
    alias virtualenv2='~/Library/Python/2.7/bin/virtualenv'
    alias ENV2=`source ~/ENV2/bin/activate`
    alias ENV3=`source ~/ENV3/bin/activate`

Next source the bashrc file so you have accesss to the new commands

.. prompt:: bash

  source ~/.bash_profile

Next let us create two virtualenv's one for python 2, the other for
python 3 in the directories `~/ENV2` and `~/ENV3`.

.. prompt:: bash

  virtualenv3 ~/ENV3
  virtualenv2 ~/ENV2


Now we can use the ENV2 and ENV3 commands to activate selectively
which version of python we use:

.. prompt:: bash

  ENV2
  python --version

  ENV3
  python --version

The python versions should be 2.7.11 or 3.5.1 or greater. To do a check on pip, say

.. prompt:: bash

    pip --version

The pip version should be 8.0.2 or greater


Python Guidelines
=================

Exceptions
----------

::
   
   from cloudmesh_client.common.Error import Error
   Error.msg(“msg")
   Error.info(“msg”)
   Error.debug(“msg”)
   Error.warning(“msg”)
   Error.exit(“msg)


   try:
      ...
   except:
      Error.debug(“my debug msg”)

Developing Compatible Code
----------------------------

A good resource is the Python 2 and 3 compatibility cheat sheet:

http://python-future.org/compatible_idioms.html

We have adopted the following

print
^^^^^^

.. code-block:: python

    from __future__ import print_function

    print('Hello')

raise
^^^^^^

.. code-block:: python

    raise ValueError("dodgy value")


traceback
^^^^^^^^^^

.. code-block:: python

    from future.utils import raise_

    traceback = sys.exc_info()[2]
    raise_(ValueError, "dodgy value", traceback)

    # we will need to create function for that as we want to control
    # with flag in db

exception
^^^^^^^^^

.. code-block:: python

     except Exception as e:


integer division
^^^^^^^^^^^^^^^^

.. code-block:: python

    from __future__ import division

    assert 2 / 3 == 0

metaclass
^^^^^^^^^

.. code-block:: python

    from future.utils import with_metaclass

    class Form(with_metaclass(FormType, BaseForm)):
        pass

strings
^^^^^^^^

.. code-block:: python

    from __future__ import unicode_literals

    s1 = 'The Zen of Python'

import
^^^^^^

.. code-block:: python

    all files will need

    from __future__ import absolute_import
    from __future__ import print_function
    from __future__ import unicode_literals

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

Reading the file into an array

.. code-block:: python

   with open(filename, "r") as f:
      content = f.read()
   content = content.split("\n")

input
^^^^^

Getting raw input from keyboard:

.. code-block:: python

    name = raw_input('What is your name? ') NO!
    
    from builtins import input
    name = input('What is your name? ')
    YES!

bytechar
^^^^^^^^

.. code-block:: python

    from builtins import bytes

    for myint in bytes(b'byte-string with high-bit chars like'):
        bytechar = bytes([myint])
