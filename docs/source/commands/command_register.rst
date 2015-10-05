Register Command
======================================================================


The manual page of the register command can be found at: `register <../man/man.html#register>`_


As we are managing multiple clouds with cloudmesh we need to register
them first. To make it easy for you cloudmesh reads the registered
clouds from an easy to manage yaml file. This yam file is installed by
default into the file::

  %HOME/.cloudmesh/cloudmesh.yaml

A number of templates in that file exist that refer to commonly used
clouds. YOu can fill out the yaml file with your information, add new
clouds, or delete templates of clouds that you do not use. We have
several different typoes of clouds that we support. This includes
OpenStack, AWS, and Azure clouds.

.. todo:: at this time we have not integrated our AWS and Azure IaaS
	  abstractions. We will make them available in future.

As it may be inconvenient to edit this file and look at the yaml
format, we provide several administrative commands. The command::

  $ register info

  File C:\Users\albert\.cloudmesh\cloudmesh.yaml exists

identifies if the `cloudmesh.yaml` file exists.

To view the contents of that file, you can cat it or use the command::

  register cat

To edit the file, you can use the command::

  register edit


register list
-------------

To list the clouds that are defined in the cloudmesh.yaml file, you
can use the command::

  $ register list

which will print a table with elementary information defined for the
clouds.::

    $ register list
    Clouds specified in the configuration file C:\Users\erika\.cloudmesh\cloudmesh.yaml

    +-------+-----------+---------+
    | Name  | Iaas      | Version |
    +-------+-----------+---------+
    | azure | azure     | N/A     |
    | aws   | ec2       | N/A     |
    | india | openstack | juno    |
    | juno  | openstack | juno    |
    | kilo  | openstack | kilo    |
    +-------+-----------+---------+

To list only the names, please use the command::

    $ register list --name
    Clouds specified in the configuration file C:\Users\erika\.cloudmesh\cloudmesh.yaml

    +-------+
    | Name  |
    +-------+
    | azure |
    | aws   |
    | india |
    | juno  |
    | kilo  |
    +-------+

As we also have to sometimes login to some remote hosts it is
convenient to reuse the ssh command for that. ssh has the advantage of
being able to use a config file in $HOME/.ssh/config. MOre information
about ssh config files and their format can be found in the many web
pages if you google for `ssh config`. In case you have defined 
a host `india` in ~/.ssh/config in the following way:

    Host india
        Hostname india.futuresystems.org
        User yourusername

The list command followd by ssh will give  you a list of hosts defined
in that file::

    $ cm register list ssh

    india


register india
----------------------------------------------------------------------

The command::

  register india [--force]

Is the same command as::

  register rc india


register rc
-----------

.. todo:: I think this is wrong, the rc command should probably just
	  take an openrc.sh file and create a new entry form it ...
	  THis needs to be clarified ...
  

In case you already use an openstack cloud you may have come across an
openrc.sh file. We are providing some very special helper functions, like
for example obtain the openrc files from the futuresystems india
cloud. This command will only work if you have an account on this
machine and it is integrated into the ssh config file as discussed
previously. Once this is done, you can obtain the india juno
credentials with the command::

  register rc india

The command::

  register rc india --version=juno

will fetch the juno cloud credentials, while the command::

  register rc india --version=kilo

will fetch the kilo cloud credentials.

You will also see a verbose output about what is included in that file.
However the passwords will be masked with eight stars: `********`.
In case you like also to see the password you can use the --password flag.

register rc india --version=kilo --password

You will see an output similar to::

    $ cm register rc india --version=juno
    Reading rc file from india
    +----------------+---------------------------------------------+
    | Variable       | Value                                       |
    +----------------+---------------------------------------------+
    | OS_VERSION     | juno                                        |
    | OS_AUTH_URL    | https://i5r.idp.iu.futuregrid.org:5000/v2.0 |
    | OS_USERNAME    | albert                                    |
    | OS_PASSWORD    | ********                                    |
    | OS_CACERT      | ~/.cloudmesh/clouds/india/juno/cacert.pem   |
    | OS_TENANT_NAME | fg478                                       |
    +----------------+---------------------------------------------+


register merge 
----------------

.. todo:: the description of what this is doing was ambigous, we need
	  to clarify if it only replaces to do or actually add things
	  that do not exist, or just overwrites.
	  
IN case you have already a yaml file, form another project
you can merge two of them into the same cloudmesh yaml file. You
simply have to specify the location of the file that you like to merge
into the existing yaml file. However, please be carefull, as it will
overwrite the contents in ~/.cloudmesh/cloudmesh.yaml

.. todo:: Erika. we used to have a .bak.# when we modified the yaml file, do
	  you still have this

Hence the command 

    $ cm register merge my_cloudmesh.yaml

does what ???

register form
---------------

In some cases it is nice to have an interactive mechanism to fill out
the missing yaml file information that is indicated with TBD. THis is
useful, if you do not have an editor at hand. Thus you can use the command::

  register form

  
It will interactively fills out the form wherever we find TBD::

    $ cm register form 
    Please enter email[TBD]:
    Editing the credentials for cloud india
    Please enter OS_TENANT_NAME[TBD]:
    Editing the credentials for cloud aws
    Please enter EC2_ACCESS_KEY[TBD]:
    Please enter EC2_SECRET_KEY[TBD]:
    Please enter keyname[TBD]:
    Please enter userid[TBD]:
    Editing the credentials for cloud azure
    Please enter managementcertfile[TBD]:
    Please enter servicecertfile[TBD]:
    Please enter subscriptionid[TBD]:
    Please enter thumbprint[TBD]:


register check
----------------------------------------------------------------------

o find any not filled out values, you can use the command::

  register check

which hecks the yaml file for completness and list all fields that
have the value TBD.

    $ cm register check
    ERROR: The file has 11 values to be fixed

      email: TBD
      username: TBD
      flavor: TBD
      EC2_ACCESS_KEY: TBD
      EC2_SECRET_KEY: TBD
      keyname: TBD
      userid: TBD
      managementcertfile: TBD
      servicecertfile: TBD
      subscriptionid: TBD
      thumbprint: TBD

register json HOST
----------------------------------------------------------------------

Instead of using the cat command and listing the contents of a cloud
registration in yaml format you can also explicitly obtain a jason
representation by issueing the command::

  register json

It will return output in json format::

    $ cm register json azure
    {
        "cm_heading": "Microsoft Azure Virtual Machines",
        "cm_label": "waz",
        "cm_host": "windowsazure.com",
        "default": {
            "flavor": "ExtraSmall",
            "image": "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150610-en-us-30GB",
            "location": "East US"
        },
        "credentials": {
            "managementcertfile": "TBD",
            "servicecertfile": "TBD",
            "subscriptionid": "TBD",
            "thumbprint": "TBD"
        },
        "cm_type": "azure",
        "cm_type_version": null
    }
