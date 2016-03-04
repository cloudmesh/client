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

print::

    from __future__ import print_function

    print('Hello')

rasie::

    raise ValueError("dodgy value")


traceback::

    from future.utils import raise_

    traceback = sys.exc_info()[2]
    raise_(ValueError, "dodgy value", traceback)

    # we will need to create function for that as we want to control
    # with flag in db

exception::

     except Exception as e:

integre division::

    from __future__ import division

    assert 2 / 3 == 0

metaclass::

    from future.utils import with_metaclass

    class Form(with_metaclass(FormType, BaseForm)):
        pass

strings::

    from __future__ import unicode_literals

    s1 = 'The Zen of Python'

import::

    all files will need

    from __future__ import absolute_import
    from __future__ import print_function