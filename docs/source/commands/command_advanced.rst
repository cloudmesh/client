Advanced Command Usage
======================================================================

In this section we explain some very onvenient usage to create 3
virtual machines and the corresponding inverntory.txt file for use
with possible ansible scripts.

The following commands are used in a cloudmesh script

* `vm <../man/man.html#vm>`_
* `var <../man/man.html#var>`_  


Script to create 3 vms
--------------------------

Let us assume the cloud is the chameleon cloud on which we like to
create the vms. Than our script `vms.cm` looks as follows::


    var cloud=chameleon

    refresh on
    debug off
    key add --ssh
    default cloud=$cloud
    secgroup upload --cloud=$cloud


    #
    # GET 3 VMS WITH IP
    #
    vm boot
    var vm1=default.vm

    vm boot
    var vm2=default.vm

    vm boot
    var vm3=default.vm

    #
    # WAIT FOR THE VMS
    #
    vm ip wait $vm1
    vm ip wait $vm2
    vm ip wait $vm3

    #
    # ASSIGN IPS
    #
    vm ip assign $vm1
    vm ip assign $vm2
    vm ip assign $vm3
    
    # CREATE THE INVENTORY

    vm ip inventory $vm1,$vm2,$vm3
    
    #
    # TEST SSH
    #

    vm ssh $vm1 --command=hostname
    vm ssh $vm2 --command=hostname
    vm ssh $vm3 --command=hostname


To execute simply say

.. prompt:: bash
  
  cm vms.cm
