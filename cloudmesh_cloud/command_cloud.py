from __future__ import print_function
from cmd3.console import Console
from pprint import pprint
from cloudmesh_common.ConfigDict import ConfigDict
from cloudmesh_common.tables import dict_printer
import textwrap

class command_cloud(object):

    @classmethod
    def list(cls, filename):
        config = ConfigDict("cloudmesh.yaml")
        clouds = config["cloudmesh"]["clouds"]
        Console.ok("Clouds in the configuration file")
        print("")
        for key in clouds.keys():
            Console.ok("  " + key)

    @classmethod
    def  read_rc_file(cls, host, user, filename):
        Console.ok("register")
        print(user, host, filename)

    @classmethod
    def check_yaml_for_completeness(cls, filename):
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
            print ("")
            for line in output:
                Console.error("  " + line, prefix=False)


    @classmethod
    def register(cls, filename):
        Console.ok("register")
        print(filename)

    @classmethod
    def test(cls, filename):
        config = ConfigDict("cloudmesh.yaml")
        print (config)
        Console.ok("register")
        print(filename)

    @classmethod
    def fill_out_form(cls, filename):
        Console.ok("form")
        print(filename)
        config = ConfigDict("cloudmesh.yaml")
        # -----------------------------------------
        # edit profile
        # -----------------------------------------

        profile = config["cloudmesh"]["profile"]
        keys = profile.keys()
        for key in keys:
             result = raw_input("Please enter {:}[{:}]:".format(key,profile[key])) or profile[key]
             profile[key] = result
        config["cloudmesh"]["profile"] = profile
        config.save()

        # -----------------------------------------
        # edit clouds
        # -----------------------------------------
        clouds = config["cloudmesh"]["clouds"]
        for cloud in clouds.keys():
            print ("Editing the credentials for cloud", cloud)
            credentials = clouds[cloud]["credentials"]

            for key in credentials:
                if key not in ["OS_VERSION", "OS_AUTH_URL"]:
                    result = raw_input("Please enter {:}[{:}]:".format(key,credentials[key])) or credentials[key]
                    credentials[key] = result
        config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials
        config.save()

