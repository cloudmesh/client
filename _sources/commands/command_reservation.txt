Reservation Command
======================================================================

.. warning:: THis command is experimental and is not yet fully
	     integrated. It only stores reservations, but does not act
	     upon them.

One of the features of cloudmesh is to build a mesh of resources and
services. In some cases we which to reserve resources that allow
reservations. However we also may want to use a resource till a
particular time frane and release it. For this cases it is practical
to provide the concept of a reservation. A simple reservation is named
and containes a start and end point. We currently store named virtual
machines into a reservation for named clouds. Reservations are similar
to groups just that they have a time frame associated with them. A
timeless reservation is like a group.
	     
The manual page of the key command can be found at: `reservation
<../man/man.html#reservation>`_


Adding a reservation
----------------------------------------------------------------------
::   

    $ cm reservation add --name=test3 --start="2015-09-30" --end="2016-09-30" --user=albert --project=cloudmesh --hosts=host001 --description=desc
    Reservation test3 added successfully
    info. OK.

List Reservation
----------------------------------------------------------------------
::

    $ cm reservation list
    +----+-------+------------+------------+-----------+-----------+---------+-------------+-------+
    | id | name  | start_time | end_time   | user      | project   | hosts   | description | cloud |
    +----+-------+------------+------------+-----------+-----------+---------+-------------+-------+
    | 1  | test3 | 2015-09-30 | 2016-09-30 | albert    | cloudmesh | host001 | desc        | comet |
    +----+-------+------------+------------+-----------+-----------+---------+-------------+-------+

Update Reservation
----------------------------------------------------------------------
::

    $ cm reservation update --name=test3 --project=cloudnauts
    Reservation test3 updated successfully
    info. OK.

Verify by listing::

    $ cm reservation list
    +----+-------+------------+------------+-----------+-----------+---------+-------------+-------+
    | id | name  | start_time | end_time   | user      | project   | hosts   | description | cloud |
    +----+-------+------------+------------+-----------+-----------+---------+-------------+-------+
    | 1  | test3 | 2015-09-30 | 2016-09-30 | albert    | cloudnauts| host001 | desc        | comet |
    +----+-------+------------+------------+-----------+-----------+---------+-------------+-------+

Delete Reservation
----------------------------------------------------------------------
::

    $ cm reservation delete --name=test2
    info. OK.

Verify by listing::

    $ cm reservation list
    None
    info. OK.
