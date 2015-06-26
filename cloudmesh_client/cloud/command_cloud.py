from __future__ import print_function
from cmd3.console import Console
from pprint import pprint
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.tables import dict_printer
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.ConfigDict import Config
import os
import textwrap
from os.path import expanduser
from cloudmesh_base.util import path_expand
import os

class command_cloud(object):
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
        Console.ok("Clouds in the configuration file")
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
                             Config.path_expand("~/.ssh/config")).replace("Host ", "").replace(" ", "")
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
            filename = ".cloudmesh/clouds/india/juno/openrc.sh"

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
        config = ConfigDict("cloudmesh.yaml")

        content = config.yaml

        Console.ok("Checking the yaml file")
        count = 0
        output = []
        for line in content.split("\n"):
            if "TBD" in line:
                output.append(textwrap.dedent(line))
                count = count + 1
        if count > 0:
            Console.error("The file has {:} values to be fixed".format(count))
            print("")
            for line in output:
                Console.error("  " + line, prefix=False)

    @classmethod
    def register(cls, host, force=True):
        """
        copies the cloudmesh/clouds/india/juno directory from india
        to the ~/.cloudmesh/clouds/india/juno local directory.

        :param host: the host name
        :type host: string
        :param force:
        :type force: bool
        :return:
        """
        Console.ok("register")
        if host.lower() == "india":
            #copies the whole dir from india
            # todo:
            # what if the directory already exists in my local machine
            # We detected that the directory already exists
            # would you like to overwrite the following files in that directory ...
            # what happens if the directory is not on the remote machine

            _from = 'india:.cloudmesh/clouds/india/juno/'
            _to = path_expand('~/.cloudmesh/clouds/india/juno')

            if os.path.exists(_to):
                while True:
                    answer = ""
                    if not force:
                        answer = raw_input("Directory already exists. Would you like to overwrite {:} directory y/n? ".format(_to))
                    if  answer.lower() == 'y' or answer.lower() == 'yes' or force:
                        break
                    elif (answer.lower() != 'n' and answer.lower() != 'no'):
                        Console.ok("Invalid option")
                    else:
                        Console.ok("Operation aborted")
                        return
            else:
                try:
                    Shell.scp('-r', _from, _to)
                except Exception, e:
                    Console.error(e.message)
        else:
            Console.error("Cloud {:} not found".format(host))

    @classmethod
    def register_CERT(cls, host, cert=None):
        """
        copies the CERT to the ~/.cloudmesh/clouds/CLOUD directory and registers that cert in the coudmeh.yaml file

        :param host: the host name
        :type host: string
        :return:
        """
        Console.ok("register")
        if host == "india":#for india, CERT will be in ~/.cloudmesh/clouds/CLOUD/juno
            try:
                _from = 'india.futuresystems.org:.cloudmesh/clouds/india/juno/cacert.pem'
                _to   =  path_expand('~/.cloudmesh/clouds/india/juno')

                Shell.scp(_from, _to)

            except Exception, e:
                print ("ERROR: ", e)
                return
            try:
                home = expanduser("~")
                filename = home+'/.cloudmesh/clouds/india/juno/openrc.sh'
                result = Shell.cat(filename)
            except IOError, e:
                print ("ERROR: ", e)
                return

            
            lines = result.split("\n")
            config = ConfigDict("cloudmesh.yaml")
            for line in lines:
                if line.strip().startswith("export"):
                    line = line.replace("export ", "")
                    key, value = line.split("=", 1)
                    config["cloudmesh"]["clouds"][host]["credentials"][key] = value
            config.save()
        else:
             print ("Cloud not found")


    @classmethod
    def register_DIR(cls, host, dir):
        """
        Copies the entire directory from the cloud

        :param host: the host name
        :type host: string
        :param dir: the directory that will be fetched
        :type dir: string
        :return:
        """
        Console.ok("register")

        if host == "india":
            try:
                system("scp -r india.futuresystems.org:{:} ~/.cloudmesh/clouds/india/".format(dir))
            except Exception, e:
                print ("ERROR: ", e)
                return

        print ("successfully executed")

        #raise NotImplementedError("Not implemented")

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
        # get input that works in python 2 and 3
        input = None
        try:
            input = raw_input
        except NameError:
            pass
        for key in keys:
            result = input("Please enter {:}[{:}]:".format(key, profile[key])) or profile[key]

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
                    result = raw_input("Please enter {:}[{:}]:".format(key, credentials[key])) or credentials[key]
                    credentials[key] = result
        config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials
        config.save()
