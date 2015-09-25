"""
Script to read "OS_" environment variables and create a new cloud entry in cloudmesh.yaml

Run: python os_vars_to_yaml.py

NOTE:- re-running for existing cloud entry overwrites it.
"""

import os
from cloudmesh_client.common.ConfigDict import ConfigDict
from urlparse import urlparse

import pyaml
import json


class ConfigEnv (object):

    yaml_data = ConfigDict("cloudmesh.yaml")
    env_config_data = {"OS_AUTH_URL": None}

    def __init__(self, context):
        """
        Init Method
        :param context:
        :return:
        """
        self.context = context
        if self.context.debug:
            print("Init ConfigEnv")
        ConfigEnv.yaml_data = ConfigDict("cloudmesh.yaml")
        ConfigEnv.env_config_data = {"OS_AUTH_URL": None}

    @staticmethod
    def export(format_name="yaml", save_cm=False):
        """
        Function to export/ print the data with new cloud.
        :param format_name: format to display the data (yaml | sh | json)
        :param save_cm: Boolean flag if true, saves the data to cloudmesh.yaml
        :return:
        """
        if format_name == "yaml":
            print(pyaml.dump(ConfigEnv.yaml_data.__dict__))
        elif format_name == "json":
            print(json.dumps(ConfigEnv.yaml_data.__dict__, indent=4))
        elif format_name == "sh":
            # TODO Implement sh format
            print("TODO: Print sh format")

        # Save in cloudmesh.yaml if flag true
        if save_cm:
            ConfigEnv.yaml_data.save()
            print("New cloud config exported to {:}".format(ConfigEnv.yaml_data.filename))

    @staticmethod
    def __str_():
        """
        Utility function to export data in sh format.
        :return:
        """
        ConfigEnv.export(format_name="sh")

    @staticmethod
    def add():
        """
        Function to suggest and ask values of parameters for the new cloud.
        :return:
        """
        if ConfigEnv.env_config_data["OS_AUTH_URL"] is None:
            print("ERROR: Cloud credentials not set in environment")
            exit(1)

        cloudname_suggest = urlparse(ConfigEnv.env_config_data["OS_AUTH_URL"]).hostname

        cloudname_to_use = raw_input("Cloud name (Default: {:}): ".format(cloudname_suggest)) or cloudname_suggest
        cm_heading = raw_input("cm_heading (Default: {:} Cloud): ".format(cloudname_suggest)) \
            or "{:} Cloud".format(cloudname_suggest)

        cm_host = raw_input("cm_host name (Default: {:}): ".format(cloudname_suggest)) or "{:}"\
            .format(cloudname_suggest)

        cm_label = raw_input("cm_label name (Default: {:}): ".format(cloudname_suggest)) or "{:}"\
            .format(cloudname_suggest)

        # TODO: Check if the suggestion can be determined dynamically
        cm_type = raw_input("cm_type name (Default: openstack): ") or "openstack"

        cm_type_version = raw_input("cm_type_version name (Default: null): ") or None

        ConfigEnv.yaml_data["cloudmesh"]["clouds"][cloudname_to_use] = {"cm_heading": cm_heading,
                                                                        "cm_host": cm_host,
                                                                        "cm_label": cm_label,
                                                                        "cm_type": cm_type,
                                                                        "cm_type_version": cm_type_version,
                                                                        "credentials": ConfigEnv.env_config_data}
        # print(yaml_data)

    @classmethod
    def read(cls):
        """
        Function that will read OS_* vairables from environment and populate dict env_config_data.
        :return:
        """
        for x in os.environ:
            if x.startswith("OS_"):
                # print("{:} = {:}".format(x, os.environ[x]))
                ConfigEnv.env_config_data[x] = os.environ[x]
                # print(env_config_data)

# Main execution begins here
ConfigEnv.read()
ConfigEnv.add()
ConfigEnv.export()
