Inventory Command
======================================================================

The manual page of the key command can be found at: `Nova <../man/man.html#inventory>`_

.. todo:: reformat the inventory section to be a real manual.

Examples::
  
    cm inventory add x[0-3] --service=openstack

        adds hosts x0, x1, x2, x3 and puts the string
        openstack into the service column

    cm lists

        lists the repository

    cm x[3-4] set temperature to 32

        sets for the resources x3, x4 the value of the
        temperature to 32

    cm x[7-8] set ip 128.0.0.[0-1]

        sets the value of x7 to 128.0.0.0
        sets the value of x8 to 128.0.0.1

    cm clone x[5-6] from x3

        clones the values for x5, x6 from x3


