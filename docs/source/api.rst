API
===

The complete API for cloudmesh is available through:


.. toctree::
   :maxdepth: 2

   modules

* :ref:`genindex`
* :ref:`modindex`



Cloud Database
---------------

Cloudmesh contains a convenient Cloud database to store its
objects. It also contains simple functions to synchronize the database
with objects that are found in clouds. This includes images, flavors,
and virtual machines.

The clouds are defined in ~/.cloudmesh/cloudmesh.yaml

All you need to do is to create a cm object::

    cm = CloudmeshDatabase(cm_user="gregor")

To update a specific set of cloud object such as the flavors on the
cloud india you simply can say::

    cm.update("flavor", "india")

Other examples include

    cm.update("image", "india")
    cm.update("vm", "india")

Multiple updates and clouds can be introduced with a parametrized call::

    cm.update("vm,flavor,image", "india,aws,azure")

In our example all clouds specified update the virtual machines,
images, and flavors in the database.  Please note that the keywords
used are singular.

Once the data is in the database its easy to query it either with the
native query functions or with specialized find functions exposed to
the cm object.

To query for example a vm with the name "gregor-001" you can use

    vm = cm.find("vm", name="gregor-001").first()

Using the method::

    d = cm.o_to_d(vm)

returns a dict in the object d. Alternatively you could also use the
native database format and for example get information via::

    vm.name
    vm.status
    ....

In some cases using dicts is more convenient. You may want to chose if
you use the native form or the dict representation.






Updating an element in the database
------------------------------------

The cloud related data have a number of attributes that make it easy
to identify them.  The most important one is 'cm_id` which presents in
human readable format a unique id for the object in the database.

The id is generated fir the `getID` method.


Let us assume the following setup for our example::

    cm = CloudmeshDatabase(cm_user="gregor")

this will create a cm database object in which the user `gregor`
stores its values.  First we need to get a dictionary that we may want
to store and modify in the database.  We can obtain such an object
changeme from a live cloud with::

    cloud = OpenStack_libcloud(
        "acloudnamedefinedin_cludmesh.yaml",
        cm_user="yourusernameonthecloud")
    flavors = cloud.list("flavor", output="flat")

    internal_id = "1"

    changeme = flavors[internal_id]

However such an object could also be created by hand. To store the
element in the database we first need to generate a unique cm_id. In
our case we use the cloud object type (here flavor), the unique
internal id that we obtain for each flavor, and the name of the cloud
on which the object belongs to.::

        changeme["cm_id"] = cm.getID("flavor", internal_id, "india")

Just to be sure lest set the type to flavor::

        changeme["cm_type"] = "flavor"

Now let us change the label of the object to::

        changeme["label"] = "newlabel"

To update the new object to the database use::

        cm.update_from_dict(f)
        cm.save()

