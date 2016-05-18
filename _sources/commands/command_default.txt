Default Command
======================================================================

The manual page of the `default` command can be found at: `default
<../man/man.html#default>`_

Cloudmesh has the ability to manage easily multiple clouds.
One of the key concepts to make the list of such clouds
easier is the introduction of defaults for each cloud or globally.
Hence it is possible to set default images, flavors for each cloud,
and also create the default cloud. The default command is used to
set and list the default values. These defaults are used in other
commands if they are not overwritten by a command parameter.

Upon start of cloudmesh, the default for cloud will be set to the first
cloud that is found in the yaml file and the default group is set to
`general`.

default list
----------------------------------------------------------------------

All the current default values can by listed with --all option:

.. prompt:: bash, cm>
	    
    default list --all

::
   
    +--------+-----------+-------+-------+
    | user   | cloud     | name  | value |
    +--------+-----------+-------+-------+
    | albert | chameleon | image | abc   |
    | albert | general   | cloud | azure |
    | albert | general   | image | zyx   |
    +--------+-----------+-------+-------+

You can also add a --cloud=CLOUD option to see the defaults set
for a cloud:

.. prompt:: bash, cm>
	    
    default list --cloud=chameleon

::
   
    +--------+-----------+-------+-------+
    | user   | cloud     | name  | value |
    +--------+-----------+-------+-------+
    | albert | chameleon | image | abc   |
    +--------+-----------+-------+-------+

set default values
----------------------------------------------------------------------
To add a default value, type in a key=value pair. If no --cloud is specified,
it adds the value to the general/global cloud:

.. prompt:: bash, cm>
	    
    default image=xyz

::
   
    Successfully added value: xyz for key: image

With the --cloud=CLOUD option, defaults can be set for a particular
cloud:

.. prompt:: bash, cm>
	    
    default image=xyz --cloud=chameleon

::
   
    Successfully added value: xyz for key: image

looking up default values
----------------------------------------------------------------------
To loop up a default value set, type in the key. If no --cloud option is
specified, it returns the value of the general/global cloud:

.. prompt:: bash, cm>
	    
    default image

::
   
    Default value for image is xyz

With the --cloud=CLOUD option, defaults can be looked up for a particular
cloud:

.. prompt:: bash, cm>
	    
    default image --cloud=chameleon

::
   
    Default value for image is xyz

deleting default values
----------------------------------------------------------------------
To delete a default value, type in delete followed by the key. If no --cloud
option is specified, it deletes the value of the general/global cloud:

.. prompt:: bash, cm>
	    
    default delete image

::
   
    Deleted key image for cloud general

With the --cloud=CLOUD option, defaults can be deleted for a particular
cloud:

.. prompt:: bash, cm>
	    
    default delete image --cloud=chameleon

::
   
    Deleted key image for cloud chameleon

set a default cloud
--------------------

The default cloud can be set with the command

.. prompt:: bash, cm>
	    
    default cloud=kilo

where kilo is the name of the cloud that you have specifie din your
cloudmesh yam file. Switching to a different cloud will aslo  switch
the default image and flavor.

Use the info command to confirm your settings to make sure they are as
you expect.

.. prompt:: bash, cm>
	    
    info

Thus it is obvious that you can conveniently switch between the use of
clouds by just adjusting the defaukt cloud so booting across
heterogeneous clouds becomes easy:

.. prompt:: bash, cm>

    default cloud=kilo
    vm boot

    default cloud=chameleon
    vm boot

You have now two vms's one on kilo and one on chameleon.


distributing defaults
---------------------

Naturally the use of defaults allows you to create your own customized
cloudmesh.yaml files that includes a suitable set of default
parameters for your use. This is especially useful in class settings
where students may need a similar set to conduct their activities.

In such cases you could host the customized yaml file on a web server
or e-mail them to the students (under the assumption that you have not
included any passwords which you should not do).

Once done so the students can just copy the yaml file into the
~/.cloudmesh directory and start their project. All they need to do
is to prepare the environment with some very easy steps.

.. prompt:: bash

	    ssh-keygen -C yourname@example.com
	    mkdir -p ~/.cloudmesh
	    cp cloudmesh.yaml ~/.cloudmesh/cloudmesh.yaml
	    cm register profile
	    cm register remote    # only if you have an india account
	    cm key add --ssh
	    cm key upload

To configure a cloud you can simply edit them. The perosn distributing
the yaml file will let you know which clouds you should use

.. prompt:: bash

	    cm register kilo
	    cm register chameleon
	    cm default cloud=kilo

From that point on managing a vm is simple
	    
	    cm vm boot
	    cm vm ip assign
	    
To register new clouds (on which you have accounts) you can say

.. prompt:: bash

	    cm register chameleon

To upload keys to other clouds such as chameleon use

.. prompt:: bash

	    cm key add —ssh —cloud=chameleon





