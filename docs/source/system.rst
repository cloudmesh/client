.. _preparation:

Preparation
===================

The installation of cloudmesh is easy if you have prepared your system
with up-to-date software. We provide instructions to prepare your
system for a number of operating systems. After you have completed the
system preparation you can follow the Installation instructions which
will be the same for all systems.

In future we will provide an even simpler install mechanism on
the various operating systems based on simple install scripts.

If you like to help us in making the instructions simpler based on
your experience, please email us or create a pull request in github.

OSX
----------------------------------------------------------------------

You will need a number of tools that are not distributed with the
regular OSX operating system. First you need to install xcode. The
easiest is to open a terminal and type

.. prompt:: bash

  xcode-select --install


We recommend that you use python 2.7, e.g. at least python
2.7.10. This version of python is easy to install while downloading
the dmg and installing it on the system. You can find the python
version at:

* https://www.python.org/downloads/


You will still have access to the python version distributed with the
original OSX operating system. You will need to install pip, and
virtualenv which you can do with

.. prompt:: bash

  sudo easy_install pip
  sudo pip install virtualenv
  
To test out which version you have activated, you can use in the
command line

.. prompt:: bash

  python --version
  pip --version
  virtualenv --version 

Make sure that you have the supported versions:

  ==========  =========
  Software    Version
  ==========  =========
  Python      2.7.10
  pip         8.0.2
  virtualenv  13.1.2
  ==========  =========  
  
On OSX as well as the other operating systems we **require** you to
use virtualenv. First you need to find which version of python you
use. You can say

.. prompt:: bash

  which python

It will give you the path of the python interpreter. Let us assume the
interpreter was found in `/usr/local/bin/python`. Next you can create
a virtual ENV with

.. prompt:: bash

  virtualenv -p /user/local/bin/python ~/ENV


You will need to activate the virtualenv with

.. prompt:: bash

  source ~/ENV/bin/activate
  export PYTHONPATH=~/ENV/lib/python2.7/site-packages:$PYTHONPATH

If successful, your terminal will have (ENV) as prefix to the prompt::

  (ENV)machinename:dirname user$

If you like to use this version of python consistently, you may elect
to add it to your .bashrc file and add the command::

   source $HOME/ENV/bin/activate
   export PYTHONPATH=~/ENV/lib/python2.7/site-packages:$PYTHONPATH

We need to just do some simple updates in the virtualenv and you will
have an up to date python environment in ~/ENV

.. prompt:: bash

   pip install pip -U
   easy_install readline
   easy_install pycrypto
   pip install urllib3

.. warning:: We found that ``readline`` and ``pycrypto`` could not be
	  installed with pip at the time of writing of this manual,
	  despite the fact that pip claimed to have installed them.
	  However, the version installed with pip were not usable. The
	  workaround is to use easy_install for these packages as
	  shown above.  If you have better idea how to fix this, let
	  us know and send mail to laszewski@gmail.com.

It is recommended that you test the version of the python interpreter
and pip again

.. prompt:: bash
   
   pip --version

which should give the version 8.0.2

.. prompt:: bash

   python --version

which should give the version Python 2.7.10

OSX Quick Install Scripts (untested)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use at your own risk, we recommend that you follow the more detailed
instructions above

.. prompt:: bash

   xcode-select --install
   open https://www.python.org/downloads/

Install python 2.7.10. Next do

.. prompt:: bash

  sudo easy_install pip
  sudo pip install virtualenv
  virtualenv -p /user/local/bin/python ~/ENV
  source ~/ENV/bin/activate
  export PYTHONPATH=~/ENV/lib/python2.7/site-packages:$PYTHONPATH
  pip install pip -U
  easy_install readline
  easy_install pycrypto
  pip install urllib3

In case you have not added the two lines in your .bashrc script, you
will need to run them in any new terminal you start in which yo like
to use the new python version. It may just be easier to add them to
your .bashrc file.

  source ~/ENV/bin/activate
  export PYTHONPATH=~/ENV/lib/python2.7/site-packages:$PYTHONPATH


.. _windows-install:

Ubuntu 14.04/15.04
----------------------------------------------------------------------

As your ubuntu version may be outdated we ask you to run the following
commands

.. prompt:: bash

  sudo apt-get update        
  sudo apt-get upgrade       
  sudo apt-get dist-upgrade
  sudo apt-get install python-setuptools
  sudo apt-get install python-pip
  sudo apt-get install python-dev
  sudo apt-get install libncurses-dev
  sudo apt-get install git
  sudo easy_install readline
  sudo pip install pycrypto
  sudo apt-get install build-essential checkinstall
  sudo apt-get install libreadline-gplv2-dev
  sudo apt-get install libncursesw5-dev
  sudo apt-get install libssl-dev
  sudo apt-get install libsqlite3-dev
  sudo apt-get install tk-dev
  sudo apt-get install libgdbm-dev
  sudo apt-get install libc6-dev
  sudo apt-get install libbz2-dev

.. note:: if pycrypto does not install with pip use easy_install
	  pycrypto
	  
We recommend that you use python 2.7.10, which you can install it
alternatively in your system with without overwriting the existing
python version

.. prompt:: bash

   cd $HOME
   wget --no-check-certificate https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
   wget --no-check-certificate https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
   wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
   tar xzf Python-2.7.10.tgz
   cd Python-2.7.10
   ./configure --prefix=/usr/local
   sudo make && sudo make altinstall
   export PATH="/usr/local/bin:$PATH"

Verify if you now have the correct alternative python installed

.. prompt:: bash

   /usr/local/bin/python2.7 --version

which will return Python 2.7.10. Next, Install setuptools and pip

.. prompt:: bash

   cd $HOME
   sudo /usr/local/bin/python2.7 ez_setup.py
   sudo /usr/local/bin/python2.7 get-pip.py

Create soft symbolic links

.. prompt:: bash

   sudo ln -sf /usr/local/bin/python2.7 /usr/local/bin/python
   sudo ln -sf /usr/local/bin/pip /usr/bin/pip

Verify if you now have the required pip version installed

.. prompt:: bash

   pip --version

It shoudl show the version 8.0.2. If you see a lower version of pip, you may
upgrade it with the following command

.. prompt:: bash

   pip install -U pip

Next, Install a python virtual environment on your machine as we do
not want to interfere with the system installed python
versions. Inside your terminal run

.. prompt:: bash

   sudo apt-get install virtualenv

Next we will create a python virtualenv in the directory $HOME/ENV. To
activate virtualenv, execute the following steps

.. prompt:: bash

   virtualenv -p /usr/local/bin/python $HOME/ENV
   source $HOME/ENV/bin/activate

This will add a '(ENV)' to your prompt in the terminal like following::

  (ENV)[user@hostname ~]$

Ubuntu Quick Install Scripts (untested)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use at your own risk, we recommend that you follow the more detailed
instructions above. THe script bellow contains also an update of the
python version from 2.7.9 to 2.7.10 in an alternate install. As
cloudmesh is running fine in python 2.7.9 the update may not be needed
and you may eliminate the steps in regards to this from the bellow
script if you wish.

.. prompt:: bash

  sudo apt-get update        
  sudo apt-get upgrade       
  sudo apt-get dist-upgrade
  sudo apt-get install python-setuptools
  sudo apt-get install python-pip
  sudo apt-get install python-dev
  sudo apt-get install libncurses-dev
  sudo apt-get install git
  sudo easy_install readline
  sudo pip install pycrypto
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
  wget --no-check-certificate https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
  wget --no-check-certificate https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
  wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
  tar xzf Python-2.7.10.tgz
  cd Python-2.7.10
  ./configure --prefix=/usr/local
  sudo make && sudo make altinstall
  export PATH="/usr/local/bin:$PATH"
  cd $HOME
  sudo /usr/local/bin/python2.7 ez_setup.py
  sudo /usr/local/bin/python2.7 get-pip.py
  sudo ln -sf /usr/local/bin/python2.7 /usr/local/bin/python
  sudo ln -sf /usr/local/bin/pip /usr/bin/pip
  pip install -U pip
  virtualenv -p /usr/local/bin/python $HOME/ENV

Add the following to your .bashrc file::

     source $HOME/ENV/bin/activate

  
CentOS
----------------------------------------------------------------------

This documentation assumes that the user is advanced enough to use
linux terminal. We also assume you are not logged in as root, but you
are a regular user. However to prepare the system we assume you have
sudo privileges.

One line install
^^^^^^^^^^^^^^^^^

You can conduct these steps automatically as well as the install of
cloudmesh by executing the following script in your command line.

.. promt:: bash

   curl http://cloudmesh.github.io/get/client/centos/install.sh | bash

After this you not only have the system updated for coudmesh with
necessary libraries and tools, but you will also have cloudmesh
installed.

We encourage you to inspect the script and assess if this is the way
you like to proceed. If you rather do a step by step install, please
read on.

Deatailed Step-by-Step system preparation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I you like to conduct these steps by hand please read on. First, we
check for up-to-date versions of python and pip

.. prompt:: bash

   python --version

As CentOS typically comes with an old version of python (2.7.5), we
will install in addition to the system provided python, an alternative
python installation. This is achieved by following the next steps
executing them as normal user. They will install python 2.7.10
under`$HOME/ENV`

.. prompt:: bash

   sudo yum install -y gcc wget zlib-devel openssl-devel sqlite-devel bzip2-devel
   cd $HOME
   wget --no-check-certificate https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
   wget --no-check-certificate https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
   wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
   tar -xvzf Python-2.7.10.tgz
   cd Python-2.7.10
   ./configure --prefix=/usr/local
   sudo make && sudo make altinstall
   export PATH="/usr/local/bin:$PATH"

Verify if you now have the correct alternative python installed

.. prompt:: bash

   /usr/local/bin/python2.7 --version

which should return Python 2.7.10. Next, install setuptools and pip and
create symbolic links to them

.. prompt:: bash

   cd $HOME
   sudo /usr/local/bin/python2.7 ez_setup.py
   sudo /usr/local/bin/python2.7 get-pip.py
   sudo ln -s /usr/local/bin/python2.7 /usr/local/bin/python
   sudo ln -s /usr/local/bin/pip /usr/bin/pip

Verify if you now have the required pip version installed (this may require
a new terminal to test or a source or the .bashrc script)

.. prompt:: bash

   pip --version
   pip 8.0.2 from /usr/lib/python2.7/site-packages/pip-8.0.2-py2.7.egg (python 2.7)

If you see an older version of pip, upgrade it with the following
command

.. prompt:: bash

   pip install -U pip

Next, Install a python virtual environment on your machine as we do
not want to interfere with the system installed python
versions. Inside your terminal run

.. prompt:: bash

   sudo pip install virtualenv

Next we will create a python virtualenv in the directory $HOME/ENV. To
activate virtualenv, execute the following steps

.. prompt:: bash

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

Centos Quick Install Scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use at your own risk, we recommend that you follow the more detailed
instructions above

.. prompt:: bash

   sudo yum install -y gcc wget zlib-devel openssl-devel sqlite-devel bzip2-devel
   cd $HOME
   wget --no-check-certificate https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
   wget --no-check-certificate https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
   wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
   tar -xvzf Python-2.7.10.tgz
   cd Python-2.7.10
   ./configure --prefix=/usr/local
   sudo make && sudo make altinstall
   export PATH="/usr/local/bin:$PATH"
   cd $HOME
   sudo /usr/local/bin/python2.7 ez_setup.py
   sudo /usr/local/bin/python2.7 get-pip.py
   sudo ln -s /usr/local/bin/python2.7 /usr/local/bin/python
   sudo ln -s /usr/local/bin/pip /usr/bin/pip
   pip install -U pip
   sudo pip install virtualenv
   virtualenv -p /usr/local/bin/python $HOME/ENV

Add the following to your .bashrc script::

   source $HOME/ENV/bin/activate


Windows 10
----------------------------------------------------------------------

Install Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	     
Python can be found at http://www.python.org. We recommend to download
and install the newest version of python. At this time we recommend
that you use version 2.7.10. Other versions may work to, but are not
supported or tested. A direct link to the install can be found at::

    https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

In powershell you need to type::

    PS> explorer https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

This will open the internet browser and download the python msi
installer. It will walk you through the install process.

.. note:: If you like to install it separately, you can find the
    downloaded msi in the `~/Downloads` directory. To install
    it in powershell use::

        PS> cd ~/Downloads
        PS> msiexec /i python-2.7.10.msi /qb

    This will open a basic dialog to perform installation and
    close after completion.

.. note:: While installing python, you have the option to
    automatically include python binaries in the system Path.
    This is disabled by default, so you will need to enable it explicitly.
    Skip below step if you have choose to enable this feature.

After you have installed python (and not explicitly enabled the feature to add python to system path)
include it in the Path environment variable while you type in powershell::

        PS> [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Python27\;C:\Python27\Scripts\", "User")
        PS> $env:Path=[Environment]::GetEnvironmentVariable("Path", "User")


This should install Python 2.7.10 successfully. You can now proceed to the
next step.

Install Chocolatey, Git, VirtualEnv, Make
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we need to do some editing you will need a nice editor. Please do
not use notepad and notepad++ as they have significant issues, please
use vi, vim, or emacs. Emacs is easy to use as it has a GUI on
windows. Install emacs::

    PS> Start-Process powershell -Verb runAs

This will open a new Powershell window with administrator privileges.
Continue the below steps to install chocolatey & make::

    PS> Set-ExecutionPolicy Unrestricted -force
    PS> iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))
    PS> choco install emacs -y
    PS> choco install make -y
  
Next, to install Git, type the following command into powershell::

    PS> explorer https://git-scm.com/download/win

This will open the internet browser and download the git
installer. It will walk you through the install process.

.. note:: When installing you will see at one point a screen that asks
        you if you like to add the commands to the shell. It is recommended
        you select option (3) to add Unix shell commands to windows.
        This will install Unix style commands to Windows and include it in path.

Follow the on screen instructions, selecting the default values
for all of the options (except for above note). This will install
Git & Git Bash successfully.


Install VirtualEnv and Create a Virtual Python Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At the time this guide was written, the latest version of python virtualenv
was 14.0.2. But Windows 10 users were facing a lot of issues with this version,
and so we recommend installing a lower version of virtualenv::

    PS> pip install virtualenv==13.0.2

This will install python virtualenv on your system. To setup the environment
in powershell, run the following command::

    PS> virtualenv ~/ENV

This will create a new directory `~/ENV/` comprising a local python environment.
To activate this new environment, run::

    PS> ~/ENV/Scripts/activate.ps1

This will activate your new python virtual environment. As a proof,
you will now see a `(ENV)` prefixed to the powershell. It will look like::

    (ENV) PS> python --version
              Python 2.7.10

Congratulations, you have now activated your python virtualenv.

.. note:: To deactivate this virtualenv, you need to run
    the following command::

        (ENV) PS> deactivate

    But always remember to activate the virtualenv before using cloudmesh.
Next step is to install necessary python packages.

Install Pycrypto
^^^^^^^^^^^^^^^^^

First, if not already done, activate your virtualenv::

    PS> ~/ENV/Scripts/activate.ps1

Next, update your python-pip::

    (ENV) PS> pip install pip -U

Check the python and pip version::

    (ENV) PS> python --version
          Python 2.7.10

    (ENV) PS> pip --version
          pip 8.0.2 from c:\users\test-pc\ENV\lib\site-packages (python 2.7)


Then to install pycrypto, run the following::

    (ENV) PS> easy_install http://www.voidspace.org.uk/python/pycrypto-2.6.1/pycrypto-2.6.1.win32-py2.7.exe


Install FireFox Browser
^^^^^^^^^^^^^^^^^^^^^^^^

Cloudmesh contains tools for generating and viewing the html
documentation files. It uses FireFox to render HTML pages. To install
FireFox, run the following command::

    (ENV) PS> explorer https://www.mozilla.org/en-US/firefox/new/#download-fx

This will download the latest FireFox browser installer on your machine.
Follow the on-screen instructions to install. Once complete, add FireFox to
your path::

    (ENV) PS> [Environment]::SetEnvironmentVariable("Path", "$env:Path;C:\Program Files (x86)\Mozilla Firefox\", "User")
    (ENV) PS> $env:Path=[Environment]::GetEnvironmentVariable("Path", "User")

COngratulations! You have now successfully setup your Windows 10 machine,
and are all ready to now install Cloudmesh.


Adding SSH Key to Futuresystems Portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Close the current Powershell window and open a new one.
Now we are ready to use ssh and git. But first, let's create a key::

    PS> ssh-keygen -t rsa

Follow the instructions and leave the path unchanged. Make sure you
specify a passphrase. It is a policy on many compute resources that your
key has a passphrase. Look at the public key as we will need to upload
it to some resources::

    PS> cat ~/.ssh/id_rsa.pub

Go to the futuresystems portal::

    https://portal.futuresystems.org

Once you log in you can use the following link to add
your public key to futuresystems::

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

To simplify SSH access, you will need to configure a ssh config file.
You will need to first create a `config` file as follows::

    PS> vim ~/.ssh/config

This should open the VIM editor and next you need to enter
the following contents::

   Host india
        Hostname india.futuresystems.org
        User <your_portal_username>
        IdentityFile <path_to_id_rsa_file>

Replace `your_portal_username` with your futuresystems username and
`path_to_id_rsa_file` with the path to your private key file.
It generally is at ~/.ssh/id_rsa.

You can now easily perform ssh to futuresystems cloud using::

    PS> ssh india