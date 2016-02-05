Select Command
======================================================================

Select Command is used to interactively set a default image/ flavor/ cloud/ key.

The manual page of the key command can be found at: `SELECT <../man/man.html#select>`_

Setting default image
^^^^^^^^^^^^^^^^^^^^^^

You can select the default image with the following simple command::

    $ cm select image

    Select an Image
    ===============

        1 - image-1
        2 - fedora
        3 - CentOS7
        4 - ubuntu-custom
        5 - Ubuntu-15.10-64
        6 - Ubuntu-14.04-64
        7 - cirros
        q - quit


    Select between 1 - 7: 5
    choice 5 selected.
    Selected image Ubuntu-15.10-64

Setting default flavor
^^^^^^^^^^^^^^^^^^^^^^^

You can select the default flavor with the following simple command::

    $ cm select flavor

    Select a Flavor
    ===============

        1 - tiny
        2 - small
        3 - medium
        4 - large
        5 - xlarge
        q - quit


    Select between 1 - 5: 3
    choice 3 selected.
    Selected flavor medium

Setting default cloud
^^^^^^^^^^^^^^^^^^^^^^^

You can select the default cloud with the following simple command::

    $ cm select cloud

    Select a cloud
    ==============

        1 - kilo
        2 - chameleon
        3 - cybera-c
        4 - cybera-e
        5 - aws
        6 - chameleon-ec2
        7 - azure
        q - quit



    Select between 1 - 7: 2
    choice 2 selected.
    Selected cloud chameleon

Setting default key
^^^^^^^^^^^^^^^^^^^^

You can select the default key with the following simple command::

    $ cm select key

    Select a Key
    ============

        1 - albert-key
        2 - customkey
        q - quit


    Select between 1 - 2: 1
    choice 1 selected.
    Selected key albert-key

