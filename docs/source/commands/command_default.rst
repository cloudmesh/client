Default Command
======================================================================

The manual page of the group command can be found at: `default
<../man/man.html#default>`_

Cloudmesh has the ability to manage easily multiple clouds.
One of the key concepts to make the list of such clouds
easier is the introduction of defaults for each cloud or globally.
Hence it is possible to set default images, flavors for each cloud,
and also create the default cloud. The default command is used to
set and list the default values. These defaults are used in other
commands if they are not overwritten by a command parameter.

default list
----------------------------------------------------------------------

All the current default values can by listed with --all option::

    $ default list --all
    +--------+-----------+-------+-------+
    | user   | cloud     | name  | value |
    +--------+-----------+-------+-------+
    | albert | chameleon | image | abc   |
    | albert | general   | cloud | azure |
    | albert | general   | image | zyx   |
    +--------+-----------+-------+-------+

You can also add a --cloud=CLOUD option to see the defaults set
for a cloud::

    $ default list --cloud=chameleon
    +--------+-----------+-------+-------+
    | user   | cloud     | name  | value |
    +--------+-----------+-------+-------+
    | albert | chameleon | image | abc   |
    +--------+-----------+-------+-------+

set default values
----------------------------------------------------------------------
To add a default value, type in a key=value pair. If no --cloud is specified,
it adds the value to the general/global cloud::

    $ default image=xyz
    Successfully added value: xyz for key: image

With the --cloud=CLOUD option, defaults can be set for a particular
cloud::

    $ default image=xyz --cloud=chameleon
    Successfully added value: xyz for key: image

looking up default values
----------------------------------------------------------------------
To loop up a default value set, type in the key. If no --cloud option is
specified, it returns the value of the general/global cloud::

    $ cm default image
    Default value for image is xyz

With the --cloud=CLOUD option, defaults can be looked up for a particular
cloud::

    $ default image --cloud=chameleon
    Default value for image is xyz

deleting default values
----------------------------------------------------------------------
To delete a default value, type in delete followed by the key. If no --cloud
option is specified, it deletes the value of the general/global cloud::

    $ default delete image
    Deleted key image for cloud general

With the --cloud=CLOUD option, defaults can be deleted for a particular
cloud::

    $ default delete image --cloud=chameleon
    Deleted key image for cloud chameleon

