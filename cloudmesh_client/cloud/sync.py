from __future__ import print_function

import os
import platform
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell


class Sync(object):
    @classmethod
    def sync(cls, cloudname, localdir, remotedir, operation=None):
        """
        Syncs a local directory with a remote directory.
        Either from local to remote OR vice-versa
        :param cloudname:
        :param localdir:
        :param remotedir:
        :param operation: get/put
        :return:
        """
        # Get the operating system
        os_type = cls.operating_system()

        # fix the local dir path
        localdirpath = Config.path_expand(localdir)

        # check if local directory exists
        if not os.path.exists(localdirpath):
            if operation == "put":
                Console.error("The local directory [{}] does not exist."
                              .format(localdirpath))
                return None
            elif operation == "get":
                # for receiving, create local dir
                os.mkdir(localdirpath)
                Console.msg("Created local directory [{}] for sync."
                            .format(localdirpath))

        """
            rsync now works on windows machines as well.
            we install rsync (v5.4.1.20150827) on windows via chocolatey
            $ choco install rsync
        """

        host = cls.get_host(cloudname)
        if host is None:
            Console.error("Cloud [{}] not found in cloudmesh.yaml file."
                          .format(cloudname))
            return None
        else:
            args = None
            if operation == "put":
                args = [
                    "-r",
                    localdir,
                    host + ":" + remotedir
                ]
            elif operation == "get":
                args = [
                    "-r",
                    host + ":" + remotedir,
                    localdir
                ]
            # call rsync
            return Shell.rsync(*args)

    @classmethod
    def operating_system(cls):
        return platform.system().lower()

    @classmethod
    def get_host(cls, cloudname):
        """
        Method to get host for cloud
        from the cloudmesh.yaml file
        :param cloudname:
        :return:
        """
        # Get the remote host details
        # search based on cloudname
        config = ConfigDict("cloudmesh.yaml")
        clouds = config["cloudmesh"]["clouds"]

        # check if cloud exists in yaml
        if clouds[cloudname] is not None:
            # get the host for cloud
            hostname = clouds[cloudname]["cm_host"]
            return hostname
        else:
            return None

    @classmethod
    def get_hostname(cls, host):
        """
        Method to return hostname
        for a host in ssh config
        :param host:
        :return:
        """
        filename = Config.path_expand("~/.ssh/config")
        with open(filename, 'r') as f:
            lines = f.read().split("\n")

        found = False
        for line in lines:
            # search for host
            if "Host " in line:
                _host = line.strip().replace("Host ", "", 1).replace(" ", "")
                # if host found in ssh config
                if _host == host:
                    found = True
                    pass

            # search for hostname
            if "Hostname " in line and found is True:
                # return corresponding hostname
                hostname = line.strip().replace("Hostname ", "", 1).replace(" ", "")
                return hostname

    @classmethod
    def get_hostuser(cls, host):
        """
        Method to return user login
        for a host in ssh config
        :param host:
        :return:
        """
        filename = Config.path_expand("~/.ssh/config")
        with open(filename, 'r') as f:
            lines = f.read().split("\n")

        found = False
        for line in lines:
            # search for host
            if "Host " in line:
                _host = line.strip().replace("Host ", "", 1).replace(" ", "")
                # if host found in ssh config
                if _host == host:
                    found = True
                    pass

            # search for user
            if "User " in line and found is True:
                # return corresponding user
                username = line.strip().replace("User ", "", 1).replace(" ", "")
                return username
