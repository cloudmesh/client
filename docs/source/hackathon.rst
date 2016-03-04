Hackathon
==========


Install python 3.5 and 2.7.11
-----------------------------


Install 2.7.11
--------------

We ahve this documented elsewhere


Install 3.5
------------

Make sure you do an alternate install. THan use virtualenv -p to do ~/ENV2 and ~/ENV3
create alias in bashrc for ENV2 and ENV3

OSX
^^^^


Windows
^^^^^^^^


Conversion
----------

Python 2 and 3 compatibility cheat sheet:

http://python-future.org/compatible_idioms.html

Dict
^^^^
Using dict heights = {'Fred': 175, 'Anne': 166, 'Joe': 192}
as an example

Iterable dict keys::

.. code-block:: python

for key in heights:
    ...

Iterable dict values::

.. code-block:: python

from builtins import itervalues
for key in itervalues(heights):
    ...

Iterable dict items::

.. code-block:: python

from future.utils import iteritems
for (key, value) in iteritems(heights):
    ...

dict keys as a list::

.. code-block:: python

keylist = heights.keys() NO!
keylist = list(heights) YES!

dict values as a list::

.. code-block:: python

from future.utils import itervalues
valuelist = list(itervalues(heights))

dict items as a list::

.. code-block:: python

from future.utils import iteritems
itemlist = list(iteritems(heights))
