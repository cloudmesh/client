Raspberry PI
============

SD Cards managers

Apple PI Baker

* https://www.tweaking4all.com/software/macosx-software/macosx-apple-pi-baker/
* download: https://www.tweaking4all.com/?wpfb_dl=94

Retina support

    defaults write com.tweaking4all.PiBaker AppleMagnifiedMode -bool no

Etcher

* https://etcher.io/

Hardware
--------

We are using Version 3.

Setup
-----

Download Raspbian and put it on an SD Card

* https://www.raspberrypi.org/downloads/raspbian/

On OSX, use *Disk Utility*, format the card to to FAT-32:

* click on Apple SDXC Reader and say erase, chodse MS-DOS FAT, say *earse*

Download Etcher and burn the image on the disk with Etcher.


Enable ssh withouot monitor
----------------------------

* https://bykov.tech/2016/10/05/step-by-step-tutorial-how-to-setup-new-raspberry-pi-from-command-line/


find the sd card volume. On OSX at /Volumes/boot

    touch /Volumes/boot/ssh

Configure WiFi
--------------

Create the network configuration in teh file *wpa_supplicant.conf*:

    network={
        ssid="YOUR_NETWORK_NAME"
        psk="YOUR_PASSWORD"
        key_mgmt=WPA-PSK
    }

Coy the file to the sd card


    cp wpa_supplicant.conf /Volumes/boot

Start the cluster
-----------------

Next start the cluster


Update
------

    sudo apt update
    sudo apt upgrade

Docker
------

Inastalation can be achieved with 

    ? sudo apt-get install lsb-release
    curl -sSL https://get.docker.com | sh
    
Refernces
-----------

* https://howchoo.com/g/njy4zdm3mwy/how-to-run-a-raspberry-pi-cluster-with-docker-swarm
* https://blog.alexellis.io/live-deep-dive-pi-swarm/
* https://github.com/alexellis/swarmmode-tests/tree/master/arm

Users
-----

Add new user with a command 

    sudo adduser youruser
    
Add the user to sudoers with visudo 

    sudo visudo
    
Add the following line in the end 

    youruser ALL=(ALL) NOPASSWD: ALL
    
Change password of pi user 

    passwd
    
Reboot your RPI 

    sudo rpi

Setup firewall
---------------

Install ufw with “sudo apt install ufw”
Allow minimum ssh ports with “sudo ufw allow 22/tcp”
Allow all other port you are going to use, i.e web “sudo ufw allow 80/tcp”
Enable ufw “sudo ufw enable”
Check the status “sudo ufw status”

Locales
-------

    sudo dpkg-reconfigure locales
    
en_US.UTF-8    