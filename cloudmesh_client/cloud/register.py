from __future__ import print_function
import textwrap
from os.path import expanduser
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import path_expand
from cloudmesh_base.util import yn_choice
from builtins import input

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict, Config
from cloudmesh_client.common import dot_cloudmesh

class CloudRegister(object):
    @classmethod
    def get(cls, cloud):
        config = ConfigDict("cloudmesh.yaml")
        if cloud in config["cloudmesh"]["clouds"]:
            return dict(config["cloudmesh"]["clouds"][cloud])

    @classmethod
    def list(cls, filename):
        """
        lists clouds from cloudmesh.yaml file

        :param filename:
        :type filename: string
        :return:
        """
        config = ConfigDict("cloudmesh.yaml")
        clouds = config["cloudmesh"]["clouds"]
        Console.ok("Clouds specified in the configuration file " + filename)
        print("")
        for key in clouds.keys():
            Console.ok("  " + key)

    @classmethod
    def list_ssh(cls):
        """
        lists hosts from ~/.ssh/config

        :return:
        """
        result = Shell.fgrep("Host ",
                             Config.path_expand("~/.ssh/config")).replace(
            "Host ", "").replace(" ", "")
        Console.ok("The following hosts are defined in ~/.ssh/config")
        print("")
        for line in result.split("\n"):
            Console.ok("  " + line)

    @classmethod
    def read_rc_file(cls, host, filename=None):
        """

        :param host: the host name
        :type host: string
        :param filename: the file name
        :type filename: string
        :return:
        """
        if host == "india" and filename is None:
            filename = os.path.join(".cloudmesh", "india", "juno", "openrc.sh")

        Console.ok("register")
        print(host, filename)
        result = Shell.ssh(host, "cat", filename)
        print(result)
        lines = result.split("\n")
        config = ConfigDict("cloudmesh.yaml")
        for line in lines:
            if line.strip().startswith("export"):
                line = line.replace("export ", "")
                key, value = line.split("=", 1)
                config["cloudmesh"]["clouds"][host]["credentials"][key] = value
        config.save()

    @classmethod
    def check_yaml_for_completeness(cls, filename):
        """
        outputs how many values has to be fixed in cloudmesh.yaml file

        :param filename: the file name
        :type filename: string
        :return:
        """
        if filename is None:
            filename = "cloudmesh.yaml"

        config = ConfigDict(filename)

        content = config.yaml

        Console.ok("Checking the yaml file")
        count = 0
        output = []
        for line in content.split("\n"):
            if "TBD" in line:
                output.append(textwrap.dedent(line))
                count += 1
        if count > 0:
            Console.error("The file has {:} values to be fixed".format(count))
            print("")
            for line in output:
                Console.error("  " + line, prefix=False)

    @classmethod
    def host(cls, host, force=False):
        """
        copies the cloudmesh/clouds/india/juno directory from india
        to the ~/.cloudmesh/clouds/india/juno local directory.

        :param host: the host name
        :type host: string
        :param force: overwrite the local directory
        :type force: bool
        :return:
        """
        Console.ok("register {}".format(host))
        if host.lower() == "india":
            _from = 'india:.cloudmesh/clouds/india/juno'
            _to = path_expand(os.path.join(dot_cloudmesh, 'clouds', 'india'))

            if os.path.exists(_to):

                if not yn_choice("Directory already exists. Would you like "
                                 "to overwrite the {:} directory y/n? ".format(_to), force=force):
                    return

            else:
                Shell.mkdir(_to)

            try:
                Console.ok("fetching information from india ...")
                Shell.scp('-r', _from, _to)
                Console.ok("registration complete. ok.")
            except Exception, e:
                Console.error(e.message)
        else:
            Console.error("Cloud {:} not found".format(host))

    @classmethod
    def certificate(cls, host, path_cert, force=False):
        """
        copies the CERT to the ~/.cloudmesh/clouds/host directory and registers
        that cert in the coudmesh.yaml file

        :param host: the host name
        :type host: string
        :param path_cert: the path to cacert.pem
        :type path_cert: string
        :param force: overwrite cacert.pem
        :type force: bool
        :return:
        """
        Console.ok("register")

        if host == "india":
            # for india, CERT will be in india:.cloudmesh/clouds/india/juno/cacert.pem

            _from = 'india:{:}'.format(path_cert)
            _to = os.path.join(dot_cloudmesh, 'clouds', 'india', 'juno')

            # copies cacert.pem from india to the a local directory
            if os.path.exists(_to):

                if not yn_choice(
                        "File already exists. Would you like to overwrite "
                        "{:}/cacert.pem file y/n? ".format(_to),
                        force=force):
                    return

            try:
                Console.ok("Fetching certificate from india...")
                Shell.scp(_from, _to)
                Console.ok("certificate fetched. ok")
            except Exception, e:
                Console.error(e.message)
                return

            # registers cert in the cloudmesh.yaml file
            try:
                Console.ok("registering cert in cloudmesh.yaml file")
                home = expanduser("~")
                filename = home + os.path.join('~', '.cloudmesh', 'clouds', 'india', 'juno', 'openrc.sh')
                result = Shell.cat(filename)
            except IOError, e:
                print("ERROR: ", e)
                return

            lines = result.split("\n")
            config = ConfigDict("cloudmesh.yaml")
            for line in lines:
                if line.strip().startswith("export"):
                    line = line.replace("export ", "")
                    key, value = line.split("=", 1)
                    config["cloudmesh"]["clouds"][host]["credentials"][
                        key] = value
            config.save()
            Console.ok("cert registered in cloudmesh.yaml file.")
        else:
            Console.error("Cloud {:} not found".format(host))

    @classmethod
    def directory(cls, host, directory, force=False):
        """
        Copies the entire directory from the cloud and puts it in ~/.cloudmesh/clouds/host

        :param host: the host name
        :type host: string
        :param directory: the directory that will be fetched
        :type directory: string
        :param force: answer questions with yes
        :type force: bool
        :return:
        """
        Console.ok("register")
        if host.lower() == "india":
            _from = 'india:{:}'.format(directory)
            _to = path_expand(os.path.join('~', '.cloudmesh', 'clouds', host))

            #
            # BUG: the next line needs to be fixed to be linux and windows compatible
            #
            folder = directory.split('/')
            destination = _to + "/" + (folder[-1:])[0]

            if os.path.exists(destination):
                if not yn_choice("Directory already exists. Would you like to "
                                 "overwrite {:} directory y/n? ".format(destination),
                                 force=force):
                    return

            try:
                Console.ok("Fetching directory...")
                Shell.scp('-r', _from, _to)
                Console.ok("Directory fetched")
            except Exception, e:
                Console.error(e.message)
        else:
            Console.error("Cloud {:} not found".format(host))

    @classmethod
    def test(cls, filename):
        """
        TODO
        :param filename:
        :type filename: string
        :return:
        """
        config = ConfigDict("cloudmesh.yaml")
        print(config)
        Console.ok("register")
        print(filename)
        raise NotImplementedError("Not implemented")

    @classmethod
    def fill_out_form(cls, filename):
        """
        edits profile and clouds from cloudmesh.yaml
        :param filename:
        :type filename: string
        :return:
        """
        Console.ok("form")
        print(filename)
        config = ConfigDict("cloudmesh.yaml")
        # -----------------------------------------
        # edit profile
        # -----------------------------------------

        profile = config["cloudmesh"]["profile"]
        keys = profile.keys()

        # TODO: test this and delete this comment
        # get input that works in python 2 and 3

        # replaced by
        #   from builtins import input
        # input = None
        # try:
        #    input = raw_input
        # except NameError:
        #    pass

        for key in keys:
            result = input(
                "Please enter {:}[{:}]:".format(key, profile[key])) or profile[key]

            profile[key] = result
        config["cloudmesh"]["profile"] = profile
        config.save()

        # -----------------------------------------
        # edit clouds
        # -----------------------------------------
        clouds = config["cloudmesh"]["clouds"]
        for cloud in clouds.keys():
            print("Editing the credentials for cloud", cloud)
            credentials = clouds[cloud]["credentials"]

            for key in credentials:
                if key not in ["OS_VERSION", "OS_AUTH_URL"]:
                    result = raw_input("Please enter {:}[{:}]:"
                                       .format(key, credentials[key])) or credentials[key]
                    credentials[key] = result
            config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials
        config.save()
