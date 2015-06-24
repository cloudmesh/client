API
===

Updating an element in the database
===================================

The cloud related data have a number of attributes that make it easy to identify them.
The most important one is 'cm_id` which presents in human readable format a unique id for
the object in the database.

The id is generated fir the `getID` method.


Let us assume the following setup for our example::

    cm = CloudmeshDatabase(cm_user="gregor")

this will create a cm database object in which the user `gregor` stores its values.
First we need to get a dictionary that we may want to store and modify in the database.
We can obtain such an object changeme from a live cloud with::

    cloud = OpenStack_libcloud(
        "acloudnamedefinedin_cludmesh.yaml",
        cm_user="yourusernameonthecloud")
    flavors = cloud.list("flavor", output="flat")

    internal_id = "1"

    changeme = flavors[internal_id]

However such an object could also be created by hand. To store the element in
the database we first need to generate a unique cm_id. In our case we use the cloud object type (here falvor),
the unique internal id that we obtain for each flavor, and the name of the cloud on which the object belongs to.::

        changeme["cm_id"] = cm.getID("flavor", internal_id, "india")

Just to be sure lest set the type to flavor::

        changeme["cm_type"] = "flavor"

Now let us change the label of the object to::

        changeme["label"] = "newlabel"

To update the new object to the database use

        cm.update_from_dict(f)
        cm.save()

