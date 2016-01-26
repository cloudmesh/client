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
    
You can also power on one single node as a computese::
  
    cm comet power on vc4 vm-vc4-[7]

Power on the front end node of the specified cluster::
  
    cm comet power on vc4
    
Get console of a running node::
  
    cm comet console vc4 vm-vc4-0

Get console of the front end::
  
    cm comet console vc4

Power off one node or a set of nodes (if they all belonging to one
active computeset)::
  
    cm comet power off vc4 vm-vc4-[0-3]    
