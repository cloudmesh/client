Limits Command
======================================================================

The manual page of the limits command can be found at: `Limits
<../man/man.html#limits>`_

Accounts may be pre-configured with a set of thresholds(or limits) to manage
capacity and prevent abuse of the system. Limits command gives a description
of the limits set for each resource along with the total number of resources
used.

limits list
----------------------------------------------------------------------

To list the limits on a default project/tenant you can use::

  $ cm limits list
    +-------------------------+-------+
    | Name                    | Value |
    +-------------------------+-------+
    | maxImageMeta            | 128   |
    | maxPersonality          | 5     |
    | maxPersonalitySize      | 10240 |
    | maxSecurityGroupRules   | 20    |
    | maxSecurityGroups       | 10    |
    | maxServerGroupMembers   | 10    |
    | maxServerGroups         | 10    |
    | maxServerMeta           | 128   |
    | maxTotalCores           | 20    |
    | maxTotalFloatingIps     | 10    |
    | maxTotalInstances       | 10    |
    | maxTotalKeypairs        | 100   |
    | maxTotalRAMSize         | 51200 |
    | totalCoresUsed          | 4     |
    | totalFloatingIpsUsed    | 0     |
    | totalInstancesUsed      | 4     |
    | totalRAMUsed            | 8192  |
    | totalSecurityGroupsUsed | 1     |
    | totalServerGroupsUsed   | 0     |
    +-------------------------+-------+

To export it in csv format, mention the format as csv::

    $ cm limits list --format=csv
    Name,Value
    maxServerMeta,128
    maxPersonality,5
    totalServerGroupsUsed,0
    maxImageMeta,128
    maxPersonalitySize,10240
    maxTotalRAMSize,51200
    maxTotalKeypairs,100
    maxSecurityGroupRules,20
    maxServerGroups,10
    totalCoresUsed,4
    totalRAMUsed,8192
    maxSecurityGroups,10
    totalFloatingIpsUsed,0
    totalInstancesUsed,4
    totalSecurityGroupsUsed,1
    maxTotalFloatingIps,10
    maxTotalInstances,10
    maxTotalCores,20
    maxServerGroupMembers,10

