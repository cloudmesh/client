System Preparation
===================

The instalation of cloudmesh is easiest if you prepare your system with some elementary
software. We provide such information for the following Operating systems:

* Linux

  * Ubuntu
  * Centos
    
* OSX
* Windows

For each of these operating systems we are provide specific
instalation instructions.

Prepare the system
------------------

OSX
^^^

On OSX we recommend that you use python 2.7.10. This version of python
is easy to install while downloading the dmg and installing it on the
system. You will still have access to the python version distributed
with the original OSX operating system.

To test out which version you have activated, you can use in the
commandline::

  python --version
  pip --version

They should show something similar to::

  Python 2.7.10
  pip 7.0.3

Oon OSX as well as the other operating systems we **require** you to
use virtualenv. First you need to find which version of python you
use. You can say::

  which python

It will give you the path of the python interpreter. Let us assume the
interpreter was found in `/usr/local/bin/python`.  Next you can create
a virtual ENV with::

  virtualenv -p /user/local/bin/python ~/ENV

You will need to activate the virtualenv::

  source ~/ENV/bin/activate

If sucessfull, your terminal will have (ENV) as prefix to the prompt::

  (ENV)machinename:dirname user$

As OSX comes with older versions of pip at this time, it is important
that you first prepare the environment before you install cloudmesh
client. To do so please isseue the following commands::

   
   export PYTHONPATH=~/ENV/lib/python2.7/site-packages:$PYTHONPATH
   pip install pip -U
   easy_install readline
   easy_install pycrypto
   pip install urllib3

.. warning:: We found that ``readline`` and ``pycrypto`` could not be
	  installed with pip at the time of writing of this manual,
	  despite the fact that pip installed it. Howerver, the
	  version installed with pip were not usable. The workaround
	  is to use easy_install for these packages. If you have a
	  better idea how to fix this, let us know and send mail to
	  laszewski@gmail.com.

It is recommended that you test the version of the python interpreter
and pip again::
   
   pip --version

which should give the version 7.1.2
   
::

   python --version


which should give the version Python 2.7.10


.. _windows-install:


Windows 10
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	     
Python can be found at http://www.python.org. We recommend to download
and install the newest version of python. At this time we recommend
that you use version 2.7.10. Other versions may work to, but are not
supported or tested. A direct link to the install can be found at

* https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

In powershell you can type::

  explorer https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

This will open the internet explorer and download the python msi installer.
The installer will be downloaded in the "Downloads" directory in user home.

You can navigate to the Downloads folder and check if the msi is downloaded::

  PS> cd Downloads
  PS> ls

It should have the "python-2.7.10.msi" listed.

Next, execute the following command from Downloads directory to install Python::

  PS> msiexec /i python-2.7.10.msi /qb

This will open a basic dialog to perform installation and close after completion.
To set the Path environment variable run the following command::

  PS> [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")

You should now have a Python environment installed on your
machine. You need to start a new powershell to access python from the
commandline.


Install ssh and git and an editor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we need to do some editing you will need a nice editor. PLeas do
not use notpad and notpad++ as they have significant issues, Usu vi,
vim, or emacs. Emecs is easy to use as it has a GUI on
windows. Install emacs::

  Start-Process powershell -Verb runAs 
  Set-ExecutionPolicy Unrestricted -force 
  iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1')) 
  choco install emacs -y

To install Git and paste the following command into the powershell::

  explorer https://github.com/git-for-windows/git/releases/latest

.. note:: When installing you will see at one point a screen that asks
	  you if you like to add the commands to the shell. This comes
	  with a warning that some windows commands will be
	  overwritten. This is different from Guravs instructions and
	  I am not sure if it woll work if you install the middle
	  button. It will not work if you just run it from bit-bash

Next we integrate git into powershell with ::

  (new-object Net.WebClient).DownloadString("http://psget.net/GetPsGet.ps1") | iex
  Set-ExecutionPolicy Unrestricted
  install-module posh-git –force
  Set-ExecutionPolicy Restricted -force


Now we are ready to use ssh and git. Let us create a key::

  ssh-keygen

Follow the instructions and leave the path unchanged. Make sure you
specify a passpharse. It is policy on many compute resources that your
key has a passphrase. Look at the public key as we will need to upload
it to some resources::

  cat ~/.ssh/id_rsa.pub

Go to::

  https://portal.futuresystems.org

Once you log in you can use the following link::

  https://portal.futuresystems.org/my/ssh-keys

Naturally this only works if you are elidgable to register and get an
account. Once you are in a valid project you can user indias
resources. After that you need to upload your public key that you
generated into the portal and did a cat on.

.. warning:: Windows will not past and copy correctly, please make
	     sure that newlines are removed for the text box where you
	     past the key. This is cause for many errors. Make sure
	     that the key in the text box is a single line and looks
	     like when you did the cat on it.

Next you can ssh into the machine like this from powershell::

   ssh  $PORTALNAME@india.futuregrid.org

where $PORTALNAME is your futuresystems portal name. Note that a login
without the -i seems not to work.

To simplify access you will need to configure a ssh coonfig file with
the following contents::

   Host india
        Hostname india.futuresystems.org
        User PORTALNAME

open new powershell

cat ~/.ssh/id_rsa.pub

past and copy in portal.futuresystems.org

.. warning:: we recommend that you are not modifying your /etc/hosts
	     in order not to confuse you about the definition of the
	     hosts you define in .ssh/config 

Obsolete - Install Gnu Like tools - Erika and Gourav
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install Git in Windows
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To download and install git for windows, please go to

* https://git-scm.com/download/win

You will be asked a couple of questions and you should make sure that
you install it so that git can be run from the terminal.

.. image:: images/git_setup/git_setup.png

Read and Accept the License to proceed.

.. image:: images/git_setup/git_setup_license.png

Select which components need to be installed. Keep the default options.

.. image:: images/git_setup/git_setup_components.png

We prefer to use GitBash as our command line tool for Git

.. image:: images/git_setup/git_setup_path.png

Select OpenSSH as the secure shell client program.

.. image:: images/git_setup/git_setup_ssh.png

Keep the default option selected - MinTTY terminal

.. image:: images/git_setup/git_setup_terminal.png

Then select the default options to proceed; Git will be installed on your machine.

To check if Git is installed on your machine, open GitBash from Start menu
and type the following::

  git --version

This should return git version 2.5.0.windows.1

Install make In Windows
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

To download and install "make" for windows, please go to:

* http://gnuwin32.sourceforge.net/downlinks/make.php

This will download the installer for make on your machine. Follow the
on-screen instructions and make will be installed.

.. image:: images/make_setup/make_setup.png

Read and Accept the License to proceed.

.. image:: images/make_setup/make_setup_license.png

Select which components need to be installed. Keep the default options.

.. image:: images/make_setup/make_setup_components.png

Select path where make is to be installed on your machine.

.. image:: images/make_setup/make_setup_dest.png

Then select the default options to proceed; Make will be installed on your machine.

Next, you need to add the location of "make.exe" to your system PATH environment variable.

Make.exe will most likely be installed at::

  C:\Program Files (x86)\GnuWin32\bin\make.exe

Add this location to the PATH variable::

  PATH = %PATH%;C:\Program Files (x86)\GnuWin32\bin;

Makeing python usable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

CentOS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: Mangirish provide instructions

Ubuntu
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: Gurav provide instructions


