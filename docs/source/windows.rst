.. _windows-install:

Windows
=======


Install Python on Windows
-------------------------

Step 1: Download Python 2.7
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It can be found at http://www.python.org. We recommend to download and install the newest version of python. The 2.7.10 version is available from:

* https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi


  
Step 2: Install Python
^^^^^^^^^^^^^^^^^^^^^^

1. Navigate to the download location on your computer, double clicking the file and pressing run when the dialog box pops up.
2. Select the `Install Just for me` option then press `Next`.
3. Leave the Destination Directory as is and select `Next`.
4. Find the `Add Python.exe to Path` option. Choose the `Will be installed on local hard drive` option then press `Next`. 
5. Click on `Finish`.

This will install python, Setuptools and Pip.

Install Cygwin
---------------

We install cygwin via chocolatey. To do so you first have to
install chocolatey. Please open a::

  cmd.exe

window as administrator. Simply type cmd.exe in the serach and than start it.


Step 1: Install Chocolatey
--------------------------

You have to copy and paste the following comamnds into a the cmd.exe terminal::
 
   C:> @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

Step 2: Install Cygwin
----------------------

Put the following line into cmd.exe::
  
  choco install --force -y cygwin 
 
Note: if Cygwin is already installed, --force will reinstall it.


Step 3: Install apt-cyg
-----------------------

Now open cygwin window by clicking on the desktop icon. Put the following command into Cygwin terminal (its shorcut can be found on your Desktop)::
  
  lynx -source rawgit.com/transcode-open/apt-cyg/master/apt-cyg > apt-cyg
  install apt-cyg /bin

This will give you a nice command to add additional packages to cygwin without using the cygwin GUI.

  apt-cyg install emacs


Step 4: Install additional packages
-----------------------------------

Run the following command in Cygwin terminal to create a development environment for python::

  apt-cyg install git
  apt-cyg install wget
  apt-cyg install curl
  apt-cyg install nc
  apt-cyg install make
  apt-cyg install gcc-g++ diffutils libmpfr-devel libgmp-devel libmpc-devel
  apt-cyg install db

Making cygwin easier to use
===========================

In case you run Windows on virtualbox for example on a Mac, you may
want to enable the guest additions. As windows 10 is currently a
prerelease the integration with the guest additions is not yet
complete. However, you can browse to the virtual box repository go to
the current release version and click from within the interner
explorer on it (it will be an iso). Than you can follow the
instructions and it will install it in the running vm.

Next you want to enable past and copy from the host os to the guest
OS.

Add the following line to your ~/.bashrc::
  
  stty lnext ^q stop undef start undef

And add the following line to your ~/.inputrc::
  
  "\C-v": paste-from-clipboard

Now you can use C-v to past a text fro the host OS to the
Windows. This also includes cygwin terminals.
