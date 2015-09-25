"""
Script to read "OS_" environment variables and create a new cloud entry in cloudmesh.yaml

Run: python os_vars_to_yaml.py

NOTE:- re-running for existing cloud entry overwrites it.
"""

import os
from cloudmesh_client.common.ConfigDict import ConfigDict
from urlparse import urlparse

yaml_data = ConfigDict("cloudmesh.yaml")
env_config_data = {"OS_AUTH_URL": None}


def populate_os_vars():
    """
    Function that will read OS_* vairables from environment and populate dict env_config_data.
    :return:
    """
    for x in os.environ:
        if x.startswith("OS_"):
            # print("{:} = {:}".format(x, os.environ[x]))
            env_config_data[x] = os.environ[x]
            # print(env_config_data)


def add_new_cloud_to_yaml():
    """
    Function to suggest and ask values of parameters for the new cloud.
    :return:
    """
    if env_config_data["OS_AUTH_URL"] is None:
        print("ERROR: Cloud credentials not set in environment")
        exit(1)

    cloudname_suggest = urlparse(env_config_data["OS_AUTH_URL"]).hostname

    cloudname_to_use = raw_input("Cloud name (Default: {:}): ".format(cloudname_suggest)) or cloudname_suggest
    cm_heading = raw_input("cm_heading (Default: {:} Cloud): ".format(cloudname_suggest)) \
        or "{:} Cloud".format(cloudname_suggest)

    cm_host = raw_input("cm_host name (Default: {:}): ".format(cloudname_suggest)) or "{:}".format(cloudname_suggest)

    cm_label = raw_input("cm_label name (Default: {:}): ".format(cloudname_suggest)) or "{:}".format(cloudname_suggest)

    # TODO: Check if the suggestion can be determined dynamically
    cm_type = raw_input("cm_type name (Default: openstack): ") or "openstack"

    cm_type_version = raw_input("cm_type_version name (Default: null): ") or None

    yaml_data["cloudmesh"]["clouds"][cloudname_to_use] = {"cm_heading": cm_heading,
                                                          "cm_host": cm_host,
                                                          "cm_label": cm_label,
                                                          "cm_type": cm_type,
                                                          "cm_type_version": cm_type_version,
                                                          "credentials": env_config_data}
    # print(yaml_data)


def export_yaml():
    """
    Function to save the yaml with the changes to file.
    :return:
    """
    yaml_data.save()


# Main execution begins here
populate_os_vars()
add_new_cloud_to_yaml()
export_yaml()
print("New cloud config exported to {:}".format(yaml_data.filename))
