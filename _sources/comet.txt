Comet Virtual Cluster
======================================================================

Example CLI usage to manage comet virtual cluster using cloudmesh
client

Configure the comet section in ~/.cloudmesh/cloudmesh.yaml file first.
auth_provider could be userpass or apikey. When specified, the
corresponding credential is needed. Please communicate with comet
admins to get the username/password or api key and secret assigned.::
  
    comet:
        auth_provider: apikey
        userpass:
            username: TBD
            password: TBD
        apikey:
            api_key: KEYSTRING
            api_secret: SECRETSTRING

List all clusters owned by the authenticated identity (summarized
format)::
  
  cm comet ll

List all clusters owned by the authenticated identity (detailed
list)::
  
  cm comet cluster
    
List a cluster by name::
  
  cm comet cluster vc2
    
List all defined computesets::

  cm comet computeset
    
List one computeset::
  
   cm comet computeset 63
    
Power on a set of compute nodes in cluster vc4::
  
    cm comet power on vc4 vm-vc4-[0-3]
    
This will request the nodes for a default period of time - 2 hours.

To request for a longer time period, use --walltime parameter. 
E.g., 100m (100 minutes), 6h (6 hours), 2d (2 days) , 1w (1 week)::

    cm comet power on vc4 vm-vc4-[0-3] --walltime=6h

The above will put the request under the one allocation associated with the cluster.
If your cluster have more than one allocations, use --allocation parameter::

    cm comet power on vc4 vm-vc4-[0-3] --allocation=YOUR_ALLOCATION

If you have more allocations, but does not specify via CLI, you will see a list of 
allocations to choose from to use.

You can power off and back on individual nodes of an active computeset. E.g.::

    cm comet power off vc4 vm-vc4-[0,1]

and then::

    cm comet power on vc4 vm-vc4-0

Or power off the whole computeset by specifying the computeset id::

    cm comet power off vc4 123

or by specifying the hosts::

    cm comet power off vc4 vm-vc4-[0-3]

Please note if you powered off all nodes from an active computeset, the computeset 
itself will be removed as well (changed to 'completed' status)

You can also power on one single node as a computese::
  
    cm comet power on vc4 vm-vc4-[7]

or simply::

    cm comet power on vc4 vm-vc4-7

Power on the front end node of the specified cluster::
  
    cm comet power on vc4
    
Get console of a running node::
  
    cm comet console vc4 vm-vc4-0

Get console of the front end::
  
    cm comet console vc4
