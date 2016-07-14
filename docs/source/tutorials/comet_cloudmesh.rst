Comet Cloudmesh Tutorial
=========================

SetupCloudmesh Client on Ubuntu Desktop in Virtualbox

Virtual Box
----------------------------------------------------------------------

* For convenience we will be using Ubuntu Xenial in this demo to install
the cloudmesh client on it 

* Please make sure you have virtualbox installed

* The link to the download is https://www.virtualbox.org/wiki/Downloads

* Download ubuntu desktop
http://www.ubuntu.com/download

* Remember the location

* Start virtualbox, create e new VM (Ubuntu, 64bit)
* Start the box
* When asked for the iso, use the folder icon to browse to the location of the downloaded image.
* Start and configure the image
* Start a terminal 
* You may want to enable past and copy between host and vm and add the guest additions.
  
.. prompt:: bash

    wget -O cm-setup.sh http://bit.ly/cloudmesh-client-xenial
    sh cm-setup.sh

What is in the script:
    
.. prompt:: bash

    sudo apt install python-pip -y
    sudo apt install libssl-dev -y
    sudo pip install pip -U
    sudo apt install git -y
    sudo pip install ansible
    sudo pip install cloudmesh_client
    python --version
    pip --version
    git –version



Configure Cloudmesh
-------------------

.. prompt:: bash

   ssh-keygen
   cm
   cm version

    
Instalation with Pip
----------------------------------------------------------------------

Installing in a virtualenv is recommended.

.. prompt:: bash

  pip install cloudmesh_client
  cm help
  cm comet init

Getting access to your cluster
----------------------------------------------------------------------

Access your vc

Cluster info:

.. prompt:: bash

  cm comet cluster ll 
  cm comet cluster
  cm comet cluster vc2

ISO images:

.. prompt:: bash

  cm comet iso list
  cm comet iso attach ubuntu-14.04.4-server-amd64.iso vc2

Example: Install the front-end node
----------------------------------------------------------------------

Find an iso and attach

.. prompt:: bash

  cm comet iso list
  cm comet iso attach ubuntu-14.04.4-server-amd64.iso vc2

Getting network configuration parameters

.. prompt:: bash

  cm comet node info vc2

Power on the node

.. prompt:: bash

  cm comet power on vc2

If it is already running, please power if off so the iso attach could take effect:

.. prompt:: bash
  
  cm comet power off vc2

Attach console to finish the OS setup

.. prompt:: bash

  cm comet console vc2

Finishing Front-end setup
----------------------------------------------------------------------

.. prompt:: bash

    cm comet power off vc2

This ensures the iso could be detached

.. prompt:: bash

   cm comet iso detach vc2
   cm comet power on vc2

login and configure the cluster

via console:

.. prompt:: bash

  cm comet console vc2

via ssh:

.. prompt:: bash

  ssh USER@IP

Configuring the front-end node
----------------------------------------------------------------------

Configuring the internal NIC:
Modify /etc/network/interfaces, and add:

.. prompt:: bash

   auto eth0
   iface eth0 inet static
	  address 192.168.1.1
	  netmask 255.255.255.0
	  network 192.168.1.0
	  broadcast 192.168.1.255

Then bring up the port

.. prompt:: bash

   sudo ifup eth0

   wget -O deploy.sh http://bit.ly/vc-deploy
   sh deploy.sh


Example: Install Compute Nodes
----------------------------------------------------------------------

Compute node setup

.. prompt:: bash

   cm comet start vc2 vm-vc2-[1-2]


Took about 15~20 minutes

Once done, the node will be shutoff

Changing to localboot

Modify /var/lib/tftpboot/pxelinux.cfg/default

::

   #default netinstall
   default local


.. prompt:: bash

    cm comet power on vc2 vm-vc2-[1-2]

login to compute nodes from front-end, and run demo app

Screenshots
-----------

.. figure:: ./images/00_install_start.png
   :scale: 50 %
   :alt: screenshot

   00_install_start.png

.. figure:: ./images/01_NIC.png
   :scale: 50 %
   :alt: screenshot

   01_NIC.png

.. figure:: ./images/02_dhcp_failed.png
   :scale: 50 %
   :alt: screenshot

   02_dhcp_failed.png

.. figure:: ./images/03_netconf_manual.png
   :scale: 50 %
   :alt: screenshot

   03_netconf_manual.png

.. figure:: ./images/04_net_ip.png
   :scale: 50 %
   :alt: screenshot

   04_net_ip.png

.. figure:: ./images/05_net_mask.png
   :scale: 50 %
   :alt: screenshot

   05_net_mask.png

.. figure:: ./images/06_net_gateway.png
   :scale: 50 %
   :alt: screenshot

   06_net_gateway.png

.. figure:: ./images/07_net_dns.png
   :scale: 50 %
   :alt: screenshot

   07_net_dns.png

.. figure:: ./images/08_partition.png
   :scale: 50 %
   :alt: screenshot

   08_partition.png

.. figure:: ./images/09_services_packages.png
   :scale: 50 %
   :alt: screenshot

   09_services_packages.png

.. figure:: ./images/10_complete.png
   :scale: 50 %
   :alt: screenshot

   10_complete.png

.. figure:: ./images/11_complete_console_expired.png
   :scale: 50 %
   :alt: screenshot

   11_complete_console_expired.png

.. figure:: ./images/12_reboot_cd.png
   :scale: 50 %
   :alt: screenshot

   12_reboot_cd.png

.. figure:: ./images/13_reboot_cd_choose_hd.png
   :scale: 50 %
   :alt: screenshot

   13_reboot_cd_choose_hd.png

.. figure:: ./images/20_hostname.png
   :scale: 50 %
   :alt: screenshot

   20_hostname.png

.. figure:: ./images/21_domain.png
   :scale: 50 %
   :alt: screenshot

   21_domain.png

.. figure:: ./images/22_user_password_creation.png
   :scale: 50 %
   :alt: screenshot

   22_user_password_creation.png
