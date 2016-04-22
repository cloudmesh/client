from __future__ import print_function

import os
import platform
import textwrap

try:  # python3
    from urllib.request import urlopen
    from urllib.parse import urlparse
except ImportError:  # python2
    from urlparse import urlparse
    from urllib import urlopen

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict, Config
from cloudmesh_client.common import Printer
from cloudmesh_client.common.util import path_expand
from builtins import input
import cloudmesh_client
from pprint import pprint
import sys
from cloudmesh_client.common.util import banner

class Register(object):
    @classmethod
    def entry(cls, name):

        banner("Register {}".format(name))

        name = str(name)
        etc_config = ConfigDict("cloudmesh.yaml", etc=True)
        config = ConfigDict("cloudmesh.yaml")

        clouds = config["cloudmesh.clouds"]
        clusters = config["cloudmesh.hpc.clusters"]

        if name in clouds:
            name = "cloudmesh.clouds.{}.credentials".format(name)
        elif name in clusters:
            name = "cloudmesh.hpc.clusters.{}.credentials".format(name)
        elif not name.startswith("cloudmesh."):
            name = "cloudmesh." + name

        try:
            etc = etc_config[name]
            yaml = config[name]

            # walk yaml
            for key in etc:
                if etc[key] == "TBD":
                    result = input("Enter {:} ({:}): ".format(key, yaml[key]))
                    if result != '':
                        yaml[key] = result

            config.save()
        except Exception as e:
            Console.error("Could not find {} in the yaml file".format(name), traceflag=False)


class CloudRegister(object):
    @classmethod
    def get(cls, cloud):
        config = ConfigDict("cloudmesh.yaml")
        if cloud in config["cloudmesh"]["clouds"]:
            return dict(config["cloudmesh"]["clouds"][cloud])
        else:
            return None

    @classmethod
    def list(cls, filename, cloud, info=False, output='table'):
        """
        lists clouds from cloudmesh.yaml file

        :param filename:
        :type filename: string
        :return:
        """
        config = ConfigDict("cloudmesh.yaml")
        clouds = config["cloudmesh"]["clouds"]
        if info:
            Console.ok("Cloudmesh configuration file: {}".format(filename))
            print("")
        d = {}
        for i, key in enumerate(clouds.keys()):
            d[i] = {
                "id": i,
                "cloud": key,
                "iaas": config["cloudmesh"]["clouds"][key]["cm_type"],
                "version":
                    config["cloudmesh"]["clouds"][key]["cm_type_version"] or "",
                # "active": "*" if key in config["cloudmesh"]["active"] else "",
                "active": config["cloudmesh"]["active"].index(key) + 1 if key in config["cloudmesh"]["active"] else "",
                "default": "*" if key == cloud else ""
            }
        return Printer.Printer.write(d,
                                     order=['id',
                                            'default',
                                            'cloud',
                                            'iaas',
                                            'version',
                                            'active'],
                                     output=output)

    @classmethod
    def list_ssh(cls):
        """
        lists hosts from ~/.ssh/config

        :return:
        """
        filename = Config.path_expand("~/.ssh/config")
        with open(filename, 'r') as f:
            lines = f.read().split("\n")
        hosts = []
        for line in lines:
            if "Host " in line:
                host = line.strip().replace("Host ", "", 1).replace(" ", "")
                dhost = {"host": host}
                hosts.append(dhost)
        return hosts

    @classmethod
    def read_rc_file(cls, host, openrc, force=False):
        """

        :param host: the host name
        :type host: string
        :param openrc: the file name
        :type openrc: string
        :return:
        """

        openrc = Config.path_expand(openrc)

        # check if file exists
        if not os.path.isfile(openrc):
            Console.error("File not found.")
            return

        with open(openrc, 'r') as f:
            lines = f.read().split("\n")

        config = ConfigDict("cloudmesh.yaml")
        credentials = {}
        for line in lines:
            if line.strip().startswith("export "):
                line = line.replace("export ", "")
                key, value = line.split("=", 1)
                credentials[key] = value

        if host not in config["cloudmesh.clouds"] or force:
            config["cloudmesh"]["clouds"][host] = {
                "credentials": credentials,
                "cm_heading": "TBD",
                "cm_host": "TBD",
                "cm_label": "TBD",
                "cm_type": "TBD",
                "cm_type_version": "TBD"}

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
    def make_dir(cls, directory):
        if not os.path.exists(Config.path_expand(directory)):
            os.makedirs(Config.path_expand(directory))

    @classmethod
    def remote(cls, host, force=False):
        """

        TODO: there is a bug in the instalation of kilo the openrc file on
        the remote machine is not called openrc.sh but contains username and
        project number.

        :param host: the remote host
        :param force:
        :return:
        """

        config = ConfigDict("cloudmesh.yaml")

        host_spec = config["cloudmesh.clouds." + host]
        host_credentials = host_spec["credentials"]

        if 'cm_openrc' in host_spec:
            Console.ok("looking for openrc")
        else:
            Console.error("no cm_openrc specified in the host")
            return

        hostname = config["cloudmesh.clouds." + host + ".cm_host"]
        Console.ok("fetching information from {:}  ...".format(host))

        openrc = host_spec["cm_openrc"]

        directory = os.path.dirname(openrc)
        base = os.path.basename(openrc)

        _from_dir = "{:}:{:}".format(hostname, directory + "/*").replace("~/", "")
        # _to_dir = os.path.dirname(Config.path_expand(directory))
        # FIX: Issues with path expanding on Windows
        _to_dir = os.path.realpath(
            os.path.expanduser(directory)
        )

        '''
        In Windows, SCP fails with path such as C:\\Users\\...,
            and passes with '~/.cloudmesh/...'
        But on Linux machines, it fails with ~/.cloudmesh/...
            and passes with /home/user/...
        Hence, adding OS check below for SCP copy directory
        '''
        os_type = platform.system().lower()
        if 'windows' not in os_type:
            directory = _to_dir

        # FIX: fix for scp not working on Windows, because scp does not
        # understand
        # paths in format: "C:/Users/<>", rather expects "~/.cloudmesh/<>"
        # openrc_file = Config.path_expand(openrc)
        openrc_file = os.path.realpath(
            os.path.expanduser(openrc)
        )
        print("From:  ", _from_dir)
        print("To:    ", _to_dir)
        print("Openrc:", openrc_file)

        cls.make_dir(_to_dir)
        r = ""
        Console.ok("Reading rc file from {}".format(host))
        try:
            r = Shell.scp('-r', _from_dir, directory)
        except Exception as e:
            print(e)
            return

        #
        # TODO: the permission are not yet right
        #
        os.chmod(_to_dir, 0o700)
        for root, dirs, _ in os.walk(_to_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o700)
        #
        # END PERMISSION
        #

        with open(openrc_file, 'r') as f:
            lines = f.read().split("\n")

        config = ConfigDict("cloudmesh.yaml")
        for line in lines:
            if line.strip().startswith("export"):
                line = line.replace("export ", "")
                key, value = line.split("=", 1)
                config["cloudmesh"]["clouds"][host]["credentials"][key] = value
        host_spec = config["cloudmesh"]["clouds"][host]
        credentials = host_spec["credentials"]

        if "cm_openrc" in host_spec:
            openrc = host_spec["cm_openrc"]
            for attribute in credentials:
                if attribute in openrc:
                    openrc.replace(attribute, credentials[attribute])
        config.save()
        config = ConfigDict("cloudmesh.yaml")
        return config["cloudmesh"]["clouds"][host]["credentials"]

    @classmethod
    def ec2(cls, cloud, zipfile):

        def sanitize(name):
            return name.replace(".zip", "").replace("@", "_")

        def find_exports(filename):
            with open(filename, "r") as f:
                content = f.read()
            data = {}
            for line in content.split("\n"):
                if line.startswith("export "):
                    line = line.replace("export ", "")
                    attribute, value = line.split("=", 1)
                    value = value.replace("${NOVA_KEY_DIR}/", "")
                    # remove comments
                    data[attribute] = value.split("#")[0].strip()
            return data

        base = sanitize(os.path.basename(zipfile))
        dest = sanitize(os.path.join(
            path_expand("~"),
            ".cloudmesh",
            "clouds",
            cloud,
            os.path.basename(zipfile)))
        Console.msg("Unzip file {} -> {}".format(zipfile, dest))
        r = Shell.unzip(zipfile, dest)
        rcfile = os.path.join(dest, "ec2rc.sh")
        data = find_exports(rcfile)
        data["DEST"] = dest
        data["CLOUD"] = cloud
        d = {
            "cm_heading": "{CLOUD}, EC2".format(**data),
            "cm_host": None,
            "cm_label": "{CLOUD}_ec2".format(**data),
            "cm_type": "ec2",
            "cm_type_version": "ec2",
            "credentials": {
                "EC2_ACCESS_KEY": "{EC2_ACCESS_KEY}".format(**data),
                "EC2_SECRET_KEY": "{EC2_SECRET_KEY}".format(**data),
                "keyname": "TBD_not_used",
                "userid": "TBD_not_used",
                "EC2_URL": "{EC2_URL}".format(**data),
                "EC2_USER_ID": "{EC2_USER_ID}",
                "EC2_PRIVATE_KEY": "{DEST}/pk.pem".format(**data),
                "EC2_CERT": "{DEST}/cert.pem".format(**data),
                "NOVA_CERT": "{DEST}/cacert.pem".format(**data),
                "EUCALYPTUS_CERT": "{DEST}/cacert.pem".format(**data),
            },
            "default": {
                "flavor": "m1.small",
                "image": "None",
            }
        }
        config = ConfigDict("cloudmesh.yaml")
        config["cloudmesh"]["clouds"][cloud] = d
        config.save()
        # Console.error("THIS METHOD IS NOT IMPLEMENTED YET")

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
        #
        # edit profile
        #

        profile = config["cloudmesh"]["profile"]
        keys = list(profile.keys())

        # TODO: test this and delete this comment
        # get input that works in python 2 and 3

        # replaced by
        #   from builtins import input
        # input = None
        # try:
        #    input = input
        # except NameError:
        #    pass

        for key in keys:
            if profile[key] == "TBD":
                result = input("Please enter {:}[{:}]:".format(key, profile[key])) or profile[key]
                profile[key] = result

        config["cloudmesh"]["profile"] = profile
        config.save()

        # edit clouds
        clouds = config["cloudmesh"]["clouds"]
        for cloud in list(clouds.keys()):
            print("Editing the credentials for cloud", cloud)
            credentials = clouds[cloud]["credentials"]

            for key in credentials:
                if key not in ["OS_VERSION", "OS_AUTH_URL"] and credentials[key] == "TBD":
                    result = input("Please enter {:}[{:}]:".format(key, credentials[key])) or credentials[key]
                    credentials[key] = result
            config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials
        config.save()

    @classmethod
    def from_file(cls, filename):
        """
        Replaces the TBD in cloudmesh.yaml with the contents present in FILEPATH's FILE
        :param filename:
        :return:
        """
        if not os.path.isfile(os.path.expanduser(filename)):
            Console.error("{} doesn't exist".format(filename))
            return

        # BUG should use path separator
        path, filename = filename.rsplit("/", 1)
        # Config file to be read from

        from_config_file = ConfigDict(filename, [path])

        config = ConfigDict("cloudmesh.yaml")

        # Merging profile
        profile = config["cloudmesh"]["profile"]
        for profile_key in list(profile.keys()):
            if profile[profile_key] == "TBD":
                profile[profile_key] = \
                    from_config_file["cloudmesh"]["profile"][profile_key]
        config.save()

        # Merging clouds
        clouds = config["cloudmesh"]["clouds"]
        for cloud in list(clouds.keys()):
            cloud_element = clouds[cloud]
            for key in list(cloud_element.keys()):
                if cloud_element[key] == "TBD":
                    cloud_element[key] = \
                        from_config_file["cloudmesh"]["clouds"][cloud][key]
            config["cloudmesh"]["clouds"][cloud] = cloud_element

            credentials = clouds[cloud]["credentials"]
            for key in credentials:
                if credentials[key] == "TBD":
                    credentials[key] = \
                        from_config_file["cloudmesh"]["clouds"][cloud][
                            "credentials"][key]
            config["cloudmesh"]["clouds"][cloud]["credentials"] = credentials

            defaults = clouds[cloud]["default"]
            for key in defaults:
                if defaults[key] == "TBD":
                    defaults[key] = \
                        from_config_file["cloudmesh"]["clouds"][cloud][
                            "default"][
                            key]
            config["cloudmesh"]["clouds"][cloud]["default"] = defaults
        config.save()

        Console.ok(
            "Overwritten the TBD of cloudmesh.yaml with {} contents".format(
                filename))

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
    def from_environ(cls, provider):
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

        # Command line inputs
        cloudname_to_use = input(
            "Name of the cloud (Default: {:}): ".format(
                cloudname_suggest)) or cloudname_suggest

        cm_label = input(
            "Label for the cloud (Default: {:}): ".format(cloudname_to_use)) or "{:}".format(cloudname_to_use)

        cm_heading = input(
            "Heading for the cloud (Default: {:} Cloud): ".format(cm_label)) or "{:} Cloud".format(cm_label)

        cm_host = input("Cloud host name (Default: {:}): ".format(cloudname_suggest)) or "{:}" \
            .format(cloudname_suggest)

        if provider is None:
            # TODO: Check if the suggestion can be determined dynamically
            cm_type = input("Type of the cloud- openstack/azure/ec2 "
                            "(Default: openstack): ") or "openstack"
        else:
            cm_type = provider

        while cm_type not in ["openstack", "azure", "ec2"]:
            print("\nType of cloud '{:}' is invalid and should be one "
                  "of openstack/ azure/ ec2.\n"
                  .format(cm_type))
            cm_type = input("Type of the cloud- openstack/azure/ec2 "
                            "(Default: openstack): ") or "openstack"

        cm_type_version = input(
            "Version of type {:} (Default: null): ".format(cm_type)) or None

        #  Populate the dict with the data fetched from env
        yaml_data["cloudmesh"]["clouds"][cloudname_to_use] = \
            {"cm_heading": cm_heading,
             "cm_host": cm_host,
             "cm_label": cm_label,
             "cm_type": cm_type,
             "cm_type_version": cm_type_version,
             "credentials": env_config_data
             }

        # Get defaults from user

        default_flavor = input("Default flavor for the cloud instances"
                               "(Default: null): ") or None

        default_image = input("Default image for the cloud instances"
                              " (Default: null): ") or None

        default_location = input(
            "Default location for the cloud instances "
            "(Default: null): ") or None

        yaml_data["cloudmesh"]["clouds"][cloudname_to_use]["default"] = \
            {"flavor": default_flavor,
             "image": default_image,
             "location": default_location
             }

        # Save data in yaml
        yaml_data.save()
        print("New cloud config exported to {:}".format(yaml_data.filename))

    @classmethod
    def set_username(cls, username):
        """
        Method that sets the username in yaml.
        :param username:
        :return:
        """
        config = ConfigDict("cloudmesh.yaml")
        config['cloudmesh']['profile']['user'] = username
        config.save()
