#!/bin/bash

# Script to install cloudmesh client using pip in a virtualenv on Ubuntu Xenial 
# as installed by Comet VC Tutorial. If required development tools are not
# installed they will be added.

sudo apt update

if [[ ! -x $(which python) ]]; then
    echo "You need Python 2.7.10 or higher version of Python 2.7 to run cloudmesh"
    sudo apt install python-minimal -y
fi

sudo apt-get install build-essential checkinstall -y
sudo apt-get install python-dev virtualenv python-pip libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev -y

if [[ -d $HOME/.cloudmesh ]]; then
    echo "Removing old cloudmesh configuration..."
    rm -rf $HOME/.cloudmesh
fi

# Create a virtualenv for cloudmesh
echo "Creating/activating virtualenv for cloudmesh..."
virtualenv ~/CLOUDMESH
source ~/CLOUDMESH/bin/activate

# Install cloudmesh in the virtual env
echo "Installing cloudmesh into virtualenv..."
# pip install backports.ssl-match-hostname
pip install cloudmesh_client
cm version

exit 0
