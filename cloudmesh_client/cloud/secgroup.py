from __future__ import print_function

import os
import uuid as UUID

from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

class SecGroup:

    cm_db = CloudmeshDatabase() # Instance to communicate with the cloudmesh database

    @classmethod
    def set_os_environ(cls, cloudname):
        """Set os environment variables on a given cloudname"""
        try:
            d = ConfigDict("cloudmesh.yaml")
            credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
            for key, value in credentials.iteritems():
                if key == "OS_CACERT":
                    os.environ[key] = Config.path_expand(value)
                else:
                    os.environ[key] = value

                print("Key: " + key + ", Value: " + os.environ[key])
        except Exception, e:
            print(e)

    # noinspection PyPep8Naming
    @classmethod
    def remove_subjectAltName_warning(cls, content):
        result = []
        for line in content.split("\n"):
            if "Certificate has no `subjectAltName`" in line:
                pass
            elif "SecurityWarning" in line:
                pass
            else:
                result.append(line)
        return "\n".join(result)

    @classmethod
    def create(cls, label, cloudname=None, tenant=None):
        """
        Method creates a new security group in database
        & returns the uuid of the created group
        :param label:
        :param cloudname:
        :param tenant:
        :return:
        """
        # Get user from cloudmesh.yaml
        user = cls.getUser(cloudname)
        # Generate UUID
        uuid = str(UUID.uuid1())

        if not cls.get_secgroup(label, tenant, cloudname):
            secgroup_obj = model.SECGROUP(
                label,
                uuid=uuid,
                cloud=cloudname,
                user=user,
                project=tenant
            )
            cls.cm_db.add(secgroup_obj)
            cls.cm_db.save()
            return uuid

        else:
            return None

        #args = ["--insecure", "secgroup-create", label,
        #        "\" Security group for cloud: [{}], tenant: [{}]\""
        #            .format(cloudname, tenant)]

        #result = Shell.execute("nova", args)
        #return result

    @classmethod
    def list_secgroup(cls, project, cloud="general"):
        """
        This method queries the database to fetch list of secgroups
        filtered by cloud, tenant.
        :param project:
        :param cloud:
        :return:
        """
        try:
            elements = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).all()

            # Convert to dict & print table
            d = {}
            for element in elements:
                d[element.id] = {}
                for key in element.__dict__.keys():
                    if not key.startswith("_sa"):
                        d[element.id][key] = str(element.__dict__[key])

            return (tables.dict_printer(d,
                                 order=["uuid",
                                        "user",
                                        "cloud",
                                        "name",
                                        "project"],
                                 output="table"))

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def get_secgroup(cls, name, project, cloud="general"):
        """
        This method queries the database to fetch secgroup
        with given name filtered by cloud.
        :param name:
        :param project:
        :param cloud:
        :return:
        """
        try:
            secgroup = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.name == name,
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).first()
            return secgroup

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def getUser(cls, cloudname):
        try:
            #currently support India cloud
            if cloudname == "india":
                d = ConfigDict("cloudmesh.yaml")
                credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
                for key, value in credentials.iteritems():
                    if key == "OS_USERNAME":
                        return value
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)