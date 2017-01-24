#! /bin/sh

set -x

sudo apt-update
sudo apt install -y \
     python-dev \
     python-pip \
     python-virtualenv \
     libssl-dev \
     libffi-dev \
     git
pip install cloudmesh_client

cm help


