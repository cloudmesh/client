SecGroup Command
======================================================================

A security group is a named collection of network access rules
that are use to limit the types of traffic that have access to instances.
When you launch an instance, you can assign one or more security groups to it.
If you do not create security groups, new instances are automatically assigned to the default security group,
unless you explicitly specify a different security group.

The associated rules in each security group control the traffic to instances in the group.
Any incoming traffic that is not matched by a rule is denied access by default.
You can add rules to or remove rules from a security group,
and you can modify rules for the default and any other security group.

The manual page of the `secgroup` command can be found at: `secgroup
<../man/man.html#secgroup>`__


Security Group Create
----------------------

To create a security group with defined rule:

.. prompt:: bash, cm>

  secgroup add my_new_group webapp 8080 8080 tcp 0.0.0.0/0

This will create locally a secgroup named 'my_new_group', with a rule 'webapp'
defined, which opens port 8080 for protocol tcp and for the network 0.0.0.0/0.

To upload/update the group/rules into a cloud:

.. prompt:: bash, cm>

  secgroup upload --cloud=india

This will upload the locally defined security groups(s) and rule(s) to cloud
india, for the current (as specified in the yaml config file) user and project.
If no '--cloud' parameter is specified, or set to 'all', it will upload to all
'active' clouds.

Security Group List
--------------------

To list the Security Groups defined locally:

.. prompt:: bash, cm>
	    
  secgroup list

::
   
+--------+----------------+----------+--------+-----------+----------+
| name   | group          | fromPort | toPort | cidr      | protocol |
+--------+----------------+----------+--------+-----------+----------+
| http   | default        | 80       | 80     | 0.0.0.0/0 | tcp      |
| ssh    | default        | 22       | 22     | 0.0.0.0/0 | tcp      |
| ping   | default        | 0        | 0      | 0.0.0.0/0 | icmp     |
| https  | default        | 443      | 443    | 0.0.0.0/0 | tcp      |
| webapp | my-default     | 8080     | 8080   | 0.0.0.0/0 | tcp      |
+--------+----------------+----------+--------+-----------+----------+

To list the Security Groups currently in a specified cloud 'india':

.. prompt:: bash, cm>
	    
  secgroup list --cloud=india


Security Group Rule Delete
---------------------------

To delete a specific rule within a security group use:

.. prompt:: bash, cm>
	    
  secgroup delete my_secgroup_name rule_name

This will delete the named rule from the specified secgroup from the local
database. Use the 'secgroup upload' command to sync the changes to remote
cloud(s).

Security Group Delete
----------------------

To delete an entire security group use:

.. prompt:: bash, cm>
	    
  secgroup delete my_unused_secgroup --cloud=india

Use the --cloud parameter to specify on which cloud the named secgroup will
be deleted. If not specified, it will delete the secgroup locally, and use
'secgroup upload' to sync the changes to remote cloud(s).


Security Group/Rule upload/update
---------------------------------

.. prompt:: bash, cm>

  secgroup upload my_secgroup --cloud=india

This uploads the named secgroup 'my_secgroup' to the cloud 'india'. If no
secgroup name specified, it will upload/update all locally defined groups.
If no --cloud parameter specified, or set to 'all', it will upload to all
active clouds (as defined in the yaml config file).

