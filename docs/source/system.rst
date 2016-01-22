Preparation
===================

The installation of cloudmesh is easy if you have prepared your system
with updated software. We provide instructions to prepare your system
for a number of operating systems listed in this section. After you
have completed the system preparation you can follow the Installation
instructions which will be the same for all systems.

The instructions provided here are for developers of the cloudmesh
client. In future we will provide an even simpler install mechanism on
the various operating systems. For now we ask you to prepare your
system as if you were a developer. If you like to help us in making
the instructions simpler based on your experience, please email us.

OSX
----------------------------------------------------------------------

Prior to developing code on OSX, you will need a number of tools that
are not distributed with the regular OSX operating system. First you
need to install xcode if you have not done so. The easiest is to open
a terminal and type::

  xcode-select --install
 

On OSX we recommend that you use at least python 2.7.10. This version
of python is easy to install while downloading the dmg and installing
it on the system. You can find the python version at:

* https://www.python.org/downloads/


You will still have access to the python version distributed with the
original OSX operating system. To test out which version you have
activated, you can use in the command line::

  python --version
  pip --version

They should show something similar to::

  Python 2.7.10
  pip 7.0.3

On OSX as well as the other operating systems we **require** you to
use virtualenv. First you need to find which version of python you
use. You can say::

  which python

It will give you the path of the python interpreter. Let us assume the
interpreter was found in `/usr/local/bin/python`.  Next you can create
a virtual ENV with::

  virtualenv -p /user/local/bin/python ~/ENV

Note: in case the virtualenv is not installed::

  pip install virtualenv

You will need to activate the virtualenv::

  source ~/ENV/bin/activate

If successful, your terminal will have (ENV) as prefix to the prompt::

  (ENV)machinename:dirname user$

As OSX comes with older versions of pip at this time, it is important
that you first prepare the environment before you install cloudmesh
client. To do so please issue the following commands::

   
   export PYTHONPATH=~/ENV/lib/python2.7/site-packages:$PYTHONPATH
   pip install pip -U
   easy_install readline
   easy_install pycrypto
   pip install urllib3

.. warning:: We found that ``readline`` and ``pycrypto`` could not be
	  installed with pip at the time of writing of this manual,
	  despite the fact that pip claimed to have installed them. However, the
	  version installed with pip were not usable. The workaround
	  is to use easy_install for these packages. If you have a
	  better idea how to fix this, let us know and send mail to
	  laszewski@gmail.com. 

It is recommended that you test the version of the python interpreter
and pip again::
   
   pip --version

which should give the version 7.1.2::

   python --version

which should give the version Python 2.7.10


.. _windows-install:

Ubuntu 14.04.3
----------------------------------------------------------------------

* http://www.ubuntu.com/download/desktop

.. todo:: Gurav provide instructions
	  
use fresh machine (VM).
use standard python
use ubuntu ???

wahtch out for
urllib 3
readline
pip update
aptget update
aptget upgrade
....

Ubuntu 15.04
----------------------------------------------------------------------

Please conduct the following steps first to update your system::

  sudo apt-get update        
  sudo apt-get upgrade       
  sudo apt-get dist-upgrade

  sudo apt-get install python-setuptools
  sudo apt-get install python-pip
  sudo apt-get install python-dev
  sudo apt-get install libncurses-dev
  sudo easy_install readline
  sudo pip install pycrypto

Cloudmesh shoould work in python 2.7.9, but if you like to upgrade to
a new version, you can install it alternatively in your system with::

   sudo apt-get install build-essential checkinstall
   sudo apt-get install libreadline-gplv2-dev
   sudo apt-get install libncursesw5-dev
   sudo apt-get install libssl-dev
   sudo apt-get install libsqlite3-dev
   sudo apt-get install tk-dev
   sudo apt-get install libgdbm-dev
   sudo apt-get install libc6-dev
   sudo apt-get install libbz2-dev
   cd $HOME
   wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
   tar xzf Python-2.7.10.tgz
   cd Python-2.7.10
   sudo ./configure
   sudo make altinstall

   python2.7 -V
   which python2.7

We recommend that you change your bashrc to include the python 2.7.10
path and you can issue::

   python --version

to get the version 2.7.10


CentOS
----------------------------------------------------------------------

This documentation assumes that the user is advanced enough to use
linux terminal. We also assume you are not logged in as root, but you
are a regular user. However to prepare the system we assume you have
sudoer privileges. First, we check for up-to-date versions of python
and pip::

   # python --version

which should give the version Python 2.7.10::

As CentOS typically comes with an old version of python (2.7.5), we would like to provide an alternative python
installation. This can be achieved by following these steps executing as normal user.
The following steps are customized for configuring python 2.7.10 to be used for virtualenv under $HOME/ENV
to be installed later.
(each line to be executed separately and sequentially)::

   sudo yum install -y gcc wget zlib-devel openssl-devel sqlite-devel bzip2-devel
   cd $HOME
   wget --no-check-certificate https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
   wget --no-check-certificate https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
   wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py

Further steps::

   tar -xvzf Python-2.7.10.tgz
   cd Python-2.7.10
   ./configure --prefix=/usr/local
   sudo make && sudo make altinstall
   export PATH="/usr/local/bin:$PATH"

Verify if you now have the correct alternative python installed::

   /usr/local/bin/python2.7 --version
   Python 2.7.10

Install setuptools and pip::

   cd $HOME
   sudo /usr/local/bin/python2.7 ez_setup.py
   sudo /usr/local/bin/python2.7 get-pip.py
Create symlinks::

   sudo ln -s /usr/local/bin/python2.7 /usr/local/bin/python
   sudo ln -s /usr/local/bin/pip /usr/bin/pip

Verify if you now have the required pip version installed::

   pip --version
   pip 8.0.2 from /usr/lib/python2.7/site-packages/pip-8.0.2-py2.7.egg (python 2.7)

If you see a lower version of pip, you may upgrade it with the following command::

   pip install -U pip

Next, Install a python virtual environment on your machine as we do
not want to interfere with the system installed python
versions. Inside your terminal run::

   sudo pip install virtualenv

Next we will create a python virtualenv in the directory $HOME/ENV. To
activate virtualenv, execute the following steps::

   virtualenv -p /usr/local/bin/python $HOME/ENV
   source $HOME/ENV/bin/activate

This will add a '(ENV)' to your prompt in the terminal like following::

  (ENV)[user@hostname ~]$

On more permanent basis, if you want to avoid activating virtualenv
every time you log in, You can add the activation of the virtualenv to
the ~/.bashrc file with your favourate editor::

   emacs ~/.bashrc

Add the command::

   source $HOME/ENV/bin/activate

to the file and save the file. You may test if this works, by
launching a new terminal session and checking if (ENV) is seen
added to the prompt.


Windows 10
----------------------------------------------------------------------

Install Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	     
Python can be found at http://www.python.org. We recommend to download
and install the newest version of python. At this time we recommend
that you use version 2.7.10. Other versions may work to, but are not
supported or tested. A direct link to the install can be found at

* https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

In powershell you can type::

  explorer https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

This will open the internet explorer and download the python msi
installer. It will walk you through the install process.

.. note:: If you like to install it separately, you can find the
	  downloaded msi in the `~/Downloads` directory. To install
	  it in powershell use::
	    
	    cd ~/Downloads
	    msiexec /i python-2.7.10.msi /qb

	  This will open a basic dialog to perform installation and
	  close after completion.

After you have installed python include it in the Path environment
variable while you type in powershell::

  [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")

You need to start a new powershell to access python from the
command line.


Install ssh, git, make, pscp and an editor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we need to do some editing you will need a nice editor. Please do
not use notepad and notepad++ as they have significant issues, please
use vi, vim, or emacs. Emacs is easy to use as it has a GUI on
windows. Install emacs::

  Start-Process powershell -Verb runAs 
  Set-ExecutionPolicy Unrestricted -force 
  iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1')) 
  choco install emacs -y
  choco install make -y
  choco install pscp -y
  choco install vim -y
  
To install Git and paste the following command into the powershell::

  explorer https://github.com/git-for-windows/git/releases/latest

.. note:: When installing you will see at one point a screen that asks
	  you if you like to add the commands to the shell. This comes
	  with a warning that some windows commands will be
	  overwritten. This is different from bellows instructions.

Next we integrate git into powershell with ::

  (new-object Net.WebClient).DownloadString("http://psget.net/GetPsGet.ps1") | iex
  Set-ExecutionPolicy Unrestricted
  install-module posh-git –force
  Set-ExecutionPolicy Restricted -force


Now we are ready to use ssh and git. Let us create a key::

  ssh-keygen

Follow the instructions and leave the path unchanged. Make sure you
specify a passphrase. It is policy on many compute resources that your
key has a passphrase. Look at the public key as we will need to upload
it to some resources::

  cat ~/.ssh/id_rsa.pub

Go to::

  https://portal.futuresystems.org

Once you log in you can use the following link::

  https://portal.futuresystems.org/my/ssh-keys

Naturally this only works if you are eligible to register and get an
account. Once you are in a valid project you can use indias
resources. After that you need to upload your public key that you
generated into the portal and did a cat on.

.. warning:: Windows will not past and copy correctly, please make
	     sure that newlines are removed for the text box where you
	     past the key. This is cause for many errors. Make sure
	     that the key in the text box is a single line and looks
	     like when you did the cat on it.

Throughout the manual we will be using the environment variable
`$PORTALNAME` for your portal name on futuresytems. In order for you to
conveniently access it you can set it as follows::

   [Environment]::SetEnvironmentVariable("PORTALNAME","putyourportalnamehere")

and replace the string `putyourportalnamehere` with your own portal name.
	     
Next you can ssh into the machine like this from powershell::

   ssh  $PORTALNAME@india.futuregrid.org

where $PORTALNAME is your futuresystems portal name. Note that a login
without the -i seems not to work.

To simplify access you will need to configure a ssh config file with
the following contents::

   Host india
        Hostname india.futuresystems.org
        User putyourportalnamehere

	
open new powershell::

  cat ~/.ssh/id_rsa.pub

past and copy this key into a new ssh key in your futuresystems
account at::

* http::portal.futuresystems.org/my/ssh-key

.. warning:: we recommend that you are not modifying your /etc/hosts
	     in order not to confuse you about the definition of the
	     hosts you define in .ssh/config 


Install make In Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To download and install "make" for windows, in powershell type::

  explorer http://gnuwin32.sourceforge.net/downlinks/make.php

This will open the internet explorer and download the make exe
installer. It will walk you through the install process.

.. note:: If you like to install it separately, you can find the
	  downloaded exe in the `~/Downloads` directory. To install
	  it in powershell use::

	    cd ~/Downloads
	    .\make-3.81.exe /install=agent /silent

	  This will open a basic dialog to perform installation and
	  close after completion.

After you have installed make, include it in the Path environment
variable while you type in powershell::

  [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Program Files (x86)\GnuWin32\bin\", "User")

You need to start a new powershell to access make from the
command line.

Makeing python usable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To test if you have the right version of python execute::

  python --version

which should return 2.7.10 and::

  pip --version

You might see version 7.0.1 in which case you should update with::

  pip install -U pip 

.. note:: the update may not work as some error is reported. This
	  needs to be investigated and a workaround needs to be found.

We want also to install virtualenv::

  pip install virtualenv

and pyreadline::

   pip install pyreadline

