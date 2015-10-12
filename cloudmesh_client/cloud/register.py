from __future__ import print_function
import textwrap
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import yn_choice
from builtins import input

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict, Config
from cloudmesh_client.common import tables

from urlparse import urlparse


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
        d = {}
        for i, key in enumerate(clouds.keys()):
            d[i] = {
                "Name": key,
                "Iaas":  config["cloudmesh"]["clouds"][key]["cm_type"],
                "Version":
                    config["cloudmesh"]["clouds"][key]["cm_type_version"] or "N/A"
            }
        return tables.dict_printer(d, order=['Name',
                                             'Iaas',
                                             'Version'])

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
    def read_rc_file(cls, host, version, openrc=None):
        """

        :param host: the host name
        :type host: string
        :param openrc: the file name
        :type openrc: string
        :return:
        """
        #TODO: if host not in ["india"]: raise exception ("read rc file for
        #  this host not supported")
        host_openrc_mapping = {("india", None): ".cloudmesh/clouds/india/juno/openrc.sh",
                               ("india", "juno"): ".cloudmesh/clouds/india/juno/openrc.sh",
                               ("india", "kilo"): ".cloudmesh/clouds/india/kilo/openrc.sh"
                               }
        try:
            if openrc is None:
                openrc = host_openrc_mapping[(host, version)]
        except Exception:
            Console.error("No openrc file specified or found")
            return

        Console.ok("Reading rc file from {}".format(host))
        result = Shell.ssh(host, "cat {}".format(openrc))

        lines = result.split("\n")
        config = ConfigDict("cloudmesh.yaml")
        for line in lines:
            if line.strip().startswith("export"):
                line = line.replace("export ", "")
                key, value = line.split("=", 1)
                config["cloudmesh"]["clouds"][host]["credentials"][key] = value
        config.save()
        return config["cloudmesh"]["clouds"][host]["credentials"]

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
    def make_dir(cls, dir_path):
        if not os.path.exists(Config.path_expand(dir_path)):
            os.makedirs(Config.path_expand(dir_path))

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
            _to = "~/.cloudmesh/clouds/india"
            if os.path.exists(Config.path_expand(os.path.join(_to))):

                if not yn_choice("Directory already exists. Would you like "
                                 "to overwrite the {:} directory y/n? ".format(_to)):
                    return

            else:
                CloudRegister.make_dir(_to)

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
            _to = '~/.cloudmesh/clouds/india/juno'

            # copies cacert.pem from india to the a local directory
            if os.path.exists(_to):

                if not yn_choice(
                        "File already exists. Would you like to overwrite "
                        "{:}/cacert.pem file y/n? ".format(_to)):
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
                filename = "~/.cloudmesh/clouds/india/juno/openrc.sh"
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
            _to = "~/.cloudmesh/clouds/india"

            #
            # BUG: the next line needs to be fixed to be linux and windows compatible
            #
            folder = directory.split('/')
            destination = os.path.join(_to, (folder[-1:])[0])

            if os.path.exists(Config.path_expand(destination)):
                if not yn_choice("Directory already exists. Would you like to "
                                 "overwrite {:} directory y/n? ".format(destination)):
                    return
            else:
                CloudRegister.make_dir(destination)

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
        Console.ok("Filling out form")
        print(filename)
        config = ConfigDict(filename)
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
            if profile[key] == "TBD":
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
                if key not in ["OS_VERSION", "OS_AUTH_URL"] and credentials[key] == "TBD":
                    result = raw_input("Please enter {:}[{:}]:"
                                       .format(key, credentials[key])) or credentials[key]
                    credentials[key] = result
            config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials
        config.save()

    @classmethod
    def from_file(cls, file_path):
        """
        Replaces the TBD in cloudmesh.yaml with the contents present in FILEPATH's FILE
        :param file_path:
        :return:
        """
        if not os.path.isfile(os.path.expanduser(file_path)):
            Console.error("{} doesn't exist".format(file_path))
            return

        path, file = file_path.rsplit("/", 1)
        # ----------------------Config file to be read from ------------------------

        from_config_file = ConfigDict(file, [path])

        # -------------------- cloudmesh.yaml file present in . or ~/.cloudmesh ----------------
        config = ConfigDict("cloudmesh.yaml")

        # -------------------- Merging profile -----------------------
        profile = config["cloudmesh"]["profile"]
        for profile_key in profile.keys():
            if profile[profile_key] == "TBD":
                profile[profile_key] = from_config_file["cloudmesh"]["profile"][profile_key]
        config.save()

        # -------------------- Merging clouds -----------------------
        clouds = config["cloudmesh"]["clouds"]
        for cloud in clouds.keys():
            cloud_element = clouds[cloud]
            for key in cloud_element.keys():
                if cloud_element[key] == "TBD":
                    cloud_element[key] = from_config_file["cloudmesh"]["clouds"][cloud][key]
            config["cloudmesh"]["clouds"][cloud] = cloud_element

            credentials = clouds[cloud]["credentials"]
            for key in credentials:
                if credentials[key] == "TBD":
                    credentials[key] = from_config_file["cloudmesh"]["clouds"][cloud]["credentials"][key]
            config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials

            defaults = clouds[cloud]["default"]
            for key in defaults:
                if defaults[key] == "TBD":
                    defaults[key] = from_config_file["cloudmesh"]["clouds"][cloud]["default"][key]
            config["cloudmesh"]["clouds"][cloud]["default"] = defaults
        config.save()

        Console.ok("Overwritten the TBD of cloudmesh.yaml with {} contents".format(file_path))

    @classmethod
    def read_env_config(cls):
        """
        Function that will read OS_* vairables from environment and populate dict env_config_data.
        :return: env_config_data dict
        """
        env_config_data = {"OS_AUTH_URL": None}
        for x in os.environ:
            if x.startswith("OS_"):
                # print("{:} = {:}".format(x, os.environ[x]))
                env_config_data[x] = os.environ[x]
                # print(env_config_data)
        return env_config_data

    @classmethod
    def register_from_env(cls, provider):
        """
        Reads env OS_* variables and registers a new cloud in yaml, interactively.
        :return:
        """
        yaml_data = ConfigDict("cloudmesh.yaml")
        env_config_data = cls.read_env_config()

        if env_config_data["OS_AUTH_URL"] is None:
            print("ERROR: Cloud credentials not set in environment")
            return

        cloudname_suggest = urlparse(env_config_data["OS_AUTH_URL"]).hostname

        # -------------------- Command line inputs -----------------------
        cloudname_to_use = raw_input("Name of the cloud (Default: {:}): ".format(cloudname_suggest)) \
                           or cloudname_suggest

        cm_label = raw_input("Label for the cloud (Default: {:}): ".format(cloudname_to_use)) \
                   or "{:}".format(cloudname_to_use)

        cm_heading = raw_input("Heading for the cloud (Default: {:} Cloud): ".format(cm_label)) \
                     or "{:} Cloud".format(cm_label)

        cm_host = raw_input("Cloud host name (Default: {:}): ".format(cloudname_suggest)) \
                  or "{:}".format(cloudname_suggest)

        if provider is None:
            # TODO: Check if the suggestion can be determined dynamically
            cm_type = raw_input("Type of the cloud- openstack/azure/ec2 "
                                "(Default: openstack): ") or "openstack"
        else:
            cm_type = provider

        while cm_type not in ["openstack", "azure", "ec2"]:
            print("\nSorry! Type of cloud '{:}' is invalid and should be one "
                  "of openstack/ azure/ ec2.\n"
                  .format(cm_type))
            cm_type = raw_input("Type of the cloud- openstack/azure/ec2 "
                                "(Default: openstack): ") or "openstack"

        cm_type_version = raw_input("Version of type {:} (Default: null): ".format(cm_type)) or None

        # ------- Populate the dict with the data fetched from env -----------
        yaml_data["cloudmesh"]["clouds"][cloudname_to_use] = \
            {"cm_heading": cm_heading,
             "cm_host": cm_host,
             "cm_label": cm_label,
             "cm_type": cm_type,
             "cm_type_version": cm_type_version,
             "credentials": env_config_data
             }

        # -------------------- Get defaults from user ------------------------

        default_flavor = raw_input("Default flavor for the cloud instances"
                                   "(Default: null): ") or None

        default_image = raw_input("Default image for the cloud instances"
                                  " (Default: null): ") or None

        default_location = raw_input("Default location for the cloud instances "
                                     "(Default: null): ") or None

        yaml_data["cloudmesh"]["clouds"][cloudname_to_use]["default"] = \
            {"flavor": default_flavor,
             "image": default_image,
             "location": default_location
            }

        # -------------------- Save data in yaml -----------------------
        yaml_data.save()
        print("New cloud config exported to {:}".format(yaml_data.filename))
