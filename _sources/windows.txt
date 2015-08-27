.. _windows-install:


Windows 10
==========

Install Python
-----------------------------

Python can be found at http://www.python.org. We recommend to download
and install the newest version of python. At this time we recommend
that you use version 2.7.10. Other versions may work to, but are not
supported or tested. A direct link to the install can be found at

* https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

In powershell you can type::

  explorer https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi

Thsi will open the Windows explorer, download the msi and ask you to
install it.

Once downloaded, open it by clicking on the downloaded file. You may
also want to change the properties and add python to the path

.. note:: Erika we need a simple tes to see if python is
	  installed. Who do I do this?

Install Cygwin
---------------

We install cygwin via chocolatey. To do so you first have to
install chocolatey. Please open a::

  cmd.exe

window as administrator. You have to copy and paste the following commands into a the cmd.exe terminal::

.. note:: Erika how do i log in as administrator?????
	  
   C:> @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

Next execute in cmd.exe::
  
  choco install --force -y cygwin 
 
Note: if Cygwin is already installed, --force will reinstall it.


.. note:: this seems not to work on windows 10.

Now open cygwin window by clicking on the desktop icon. Put the
following command into Cygwin terminal (its shorcut can be found on
your Desktop)::
  
  lynx -source rawgit.com/transcode-open/apt-cyg/master/apt-cyg > apt-cyg
  install apt-cyg /bin

This will give you a nice command to add additional packages to cygwin
without using the cygwin GUI. You will also want the following appliations::


  apt-cyg install emacs
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
the current release version and click from within the internet
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
