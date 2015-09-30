#! /bin/bash

#
# Testing fresh virtualenv and pip
#

ENV="ENV"

BASE_DIR=`pwd`



# REPO_DIR="$HOME/github/cloudmesh-new/client"
REPO_DIR="${BASE_DIR}"
VIRTUALENV_DIR="${HOME}/${ENV}"
DEST_DIR="$HOME/cloudmesh-testenv"

set -e
set -x

# Build the source distribution
cd ${REPO_DIR}
source ${VIRTUALENV_DIR}/bin/activate
rm -rf dist/
python setup.py build sdist

# Move to the distination directory, create the test environment and instal.
mkdir -p ${DEST_DIR}
cd ${DEST_DIR}
virtualenv -p /Users/big/ENV/bin/python .
source bin/activate

pip install -U pip
pip install ${REPO_DIR}/dist/*

# The installation was successful. Destroy the test environment.
cd ${REPO_DIR}
rm -fr ${DEST_DIR}
