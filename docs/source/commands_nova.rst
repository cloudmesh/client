Command Ideas
=======================================================================

cm nova list inactive
cm nova list name[regular expression] #now I can list all VM that starts with "a", for example
cm nova delete all-inactive
cm nova restart all-ERROR (if theres no resource available, it tries to change their flavor in order to run them successfully)
cm nova group-by user
cm nova --flavor-up [0:10] #changes VM flavor. VMs must have an index associated with them
cm nova --flavor-down [20:30] #changes VM flavor
cm nova lock --range[0:10] #if you are running an important task, it prevents you to change the VMs accidentally. It will require a password to delete, restart, ..., VMs in a certain range.
cm nova order-by-flavor
cm nova order-by-status
cm nova boot --flavor=$F --image=$I --key-name=$K --name=$N --label=$L #label tells what kind of tasks the VM is running. We could group them based one their labels in order to change their flavor, for example. 
cm nova boot --flavor=$F --image=$I --key-name=$K --name=$N --quantity=$Q #creates n VMs
cm nova delete-label --label="project A"

