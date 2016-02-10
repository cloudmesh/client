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
        localdir = Config.path_expand(localdir)

        # check if local directory exists
        if not os.path.exists(localdir):
            if operation == "put":
                Console.error("The local directory [{}] does not exist."
                              .format(localdir))
                return None
            elif operation == "get":
                # for receiving, create local dir
                os.mkdir(localdir)
                Console.msg("Created local directory [{}] for sync."
                            .format(localdir))

        # sync entire local directory
        elif os.path.isdir(localdir):
            if operation == "put":
                localdir += "/*"
            elif operation == "get":
                localdir += "/"

        # for windows use pscp
        # rsync has issues with latest win10
        if 'windows' in os_type:
            ppk_file = ''
            while ppk_file == '':
                ppk_file = raw_input("Please enter putty private key(ppk) "
                                     "file path: ")
                # expand the path
                ppk_file = Config.path_expand(ppk_file)
                pass

            host = cls.get_host(cloudname)
            if host is None:
                Console.error("Cloud [{}] not found in cloudmesh.yaml file."
                              .format(cloudname))
                return None
            else:
                # Get the hostname and user of remote host
                hostname = cls.get_hostname(host)
                user = cls.get_hostuser(host)

                # Console.msg("Syncing local dir [{}] with remote host [{}]"
                #            .format(localdir, user + "@" + hostname))
                args = None
                if operation == "put":
                    # Construct the arguments
                    # local dir comes first (send)
                    args = [
                        "-i",
                        ppk_file,
                        localdir,
                        user + "@" + hostname + ":" + remotedir
                    ]
                elif operation == "get":
                    # Construct the arguments
                    # remote dir comes first (receive)
                    args = [
                        "-i",
                        ppk_file,
                        user + "@" + hostname + ":" + remotedir,
                        localdir
                    ]

                try:
                    # Convert command to string
                    cmd = " ".join(["pscp"] + args)
                    result = os.system(cmd)
                    if result != 0:
                        Console.error("Something went wrong. Please try again later.")
                        return None
                    else:
                        return "Success."
                except Exception as ex:
                    print(ex, ex.message)

        # for linux/mac machines use rsync
        else:
            host = cls.get_host(cloudname)
            if host is None:
                Console.error("Cloud [{}] not found in cloudmesh.yaml file."
                              .format(cloudname))
                return None
            else:
                args = None
                if operation == "put":
                    args = [
                        localdir,
                        host + ":" + remotedir
                    ]
                elif operation == "get":
                    args = [
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
