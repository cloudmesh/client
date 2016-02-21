Exercises
===========

Assignment A: Prerequisite
---------------------------

* A.1) Get account on futuresystems.org or any other cloud you have
  access to. In case you take a class that uses cloudmesh and
  futuresystems, make sure to be in a valid project. Communicate with
  your teacher who will let you know.

* A.2) Why do you need to start assignment A.1 today and can not wait
  with it till the day before the due date?

Assignment B: IaaS
--------------------

* A.1) Is prerequisite
* B.1) Install cloudmesh on local machine (we recommend a virtual box)
* B.2) Start and stop vms on the kilo cloud
* B.3) Why do i need to shut down my VM?
* B.4) Can I leave my VM simply running?
* B.5) What will happen to your VM when there is a power outage that shuts down
  the cloud?
* B.6) Assume you create 2 VMs. How do you log in securely from one to the
  other VM. What needs to be done?

Assignment C: Ansible
----------------------

* A.1) Is prerequisite
* C.1) Install cloudmesh on local machine (we recommend a virtual box)
* C.2) Develop automated script for the installation
* C.3) Generate an image on kilo cloud that uses the automated script and
  install s cloudmesh in the image
* C.4) Develop an ansible script that generates an image that has cloudmesh
  installed in it
* C.5) Bonus: use docopt to select from a command that you develop which OS is
  used and conduct the ansible install for the OS
  that you chose.

Assignment D: Key Management
-----------------------------

* D.1) What is an RSA key?
* D.2) Where are such keys stored in a user environment?
* D.3) Describe the procedures needed to use the default key (rsa) in
  Openstack with the openstack client commands.
* D.4) Describe the procedures to use the default key (rsa) in cloudmesh client
* D.5) do B.6 How can this be generalized to n virtual machines. Can you
  write a script?
* D.6) What is a known_hosts file? Assume you have used a floating ip ip
  previously for one vm, than you delete the vm and reuse the ip for another
  vm, what impact has this for the known_hosts?
* D.7) Assume you like to log in from your current machine that started a vm
  to that vm. What needs to be done?
* D.8) What is a private and a public key?
* D.9) What is the consequence of copying your private key from your current
  machine to a virtual machine?

