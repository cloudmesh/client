from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider

from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.default import Default
from cloudmesh_client.common.ConfigDict import ConfigDict

from pprint import pprint

class Image(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the image list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        # Newly implemented refresh
        result = cls.cm.refresh("image", cloud)
        return result

    @classmethod
    def list(cls, cloud, format="table"):
        """
        This method lists all images of the cloud
        :param cloud: the cloud name
        """
        # TODO: make a CloudmeshDatabase without requiring the user=

        try:
            elements = cls.cm.find(kind="image", category=cloud, scope="all")

            (order, header) = CloudProvider(cloud).get_attributes("image")

            return Printer.write(elements,
                                 order=order,
                                 header=header,
                                 output=format)

        except Exception as ex:
            Console.error(ex.message)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            cls.refresh(cloud)

        return CloudProvider(cloud).details('image', cloud, id, format)

    @classmethod
    def guess_username_from_category(cls, category, image, username=None):
        chameleon = "chameleon" in ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"][category]["cm_host"]
        username = None
        if chameleon:
            username = "cc"
        else:

            if username is None:
                Console.error("Could not guess the username of the vm", traceflag=False)
                return
            username = username or Image.guess_username(image)
        return username

    @classmethod
    def guess_username(cls, vm_name, cloud=None, description=None):
        username = None

        names = [vm_name]
        if description is not None:
            names.append(description)

        chameleon = cloud == "chameleon"
        for name in names:
            name = name.lower()
            if name.startswith("cc-") or chameleon:
                username = "cc"
                break
            elif any(x in name for x in ["ubuntu", "wily", "xenial"]):
                username = "ubuntu"
                break
            elif "centos" in name:
                username = "root"
                break
            elif "fedora" in name:
                username = "root"
                break
            elif "rhel" in name:
                username = "root"
                break
            elif "cirros" in name:
                username = "root"
                break
            elif "coreos" in name:
                username = "root"
                break

        return username

    @classmethod
    def get(cls, name=None, cloud=None):
        cloud = cloud or Default.cloud
        name = name or Default.image

        image = cls.cm.find(kind="image", category=cloud, name=name, output='dict', scope='first')
        return image

    @classmethod
    def get_username(cls, name, cloud, guess=False):
        image = cls.get(cloud=cloud, name=name)
        if guess and image.username is None:
            return cls.guess_username(image.name)
        return image.username

    @classmethod
    def set_username(cls, name=None, cloud=None, username=None):
        image = cls.get(cloud=cloud, name=name)

        cls.cm.set(name, "username", username, provider=image.provider, kind="image", scope="first")
