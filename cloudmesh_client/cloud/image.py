from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProviderOpenstack import CloudProviderOpenstack


class Image(object):
    cm_db = CloudmeshDatabase()

    @classmethod
    def clear(cls, cloud):
        """
        This method deletes all images of the cloud
        :param cloud: the cloud name
        """
        try:
            image = cls.cm_db.query(model.IMAGE).filter(
                model.IMAGE.cloud == cloud
            ).all()

            for ima in image:
                cls.cm_db.delete(ima)
        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.cm_db.close()

    @classmethod
    def refresh_image_list(cls, cloud):
        """
        This method would refresh the image list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        # set the environment
        d = ConfigDict("cloudmesh.yaml")
        cloud_details = d["cloudmesh"]["clouds"][cloud]
        nova = CloudProviderOpenstack(cloud, cloud_details).nova

        # delete previous data
        Image.clear(cloud)

        try:
            # get the user
            user = cls.cm_db.user

            # read data from openstack
            for image in nova.images.list():
                image_dict = image._info
                image_obj = model.IMAGE(
                    image_dict['name'],
                    image_dict['id'],
                    type="string",
                    cloud=cloud,
                    user=user
                )
                cls.cm_db.add(image_obj)
                cls.cm_db.save()

            return "Images for cloud {} refreshed successfully".format(cloud)

        except Exception as ex:
            Console.error(ex.message, ex)
            return ex
        finally:
            cls.cm_db.close()

    @classmethod
    def list_images(cls, cloud, format="table"):
        """
        This method lists all images of the cloud
        :param cloud: the cloud name
        """
        try:
            elements = cls.cm_db.query(model.IMAGE).filter(
                model.IMAGE.cloud == cloud
            ).all()

            if elements:
                d = {}
                for element in elements:
                    d[element.id] = {}
                    for key in element.__dict__.keys():
                        d[element.id][key] = str(element.__dict__[key])
            else:
                return "Image list empty, kindly do image refresh of the cloud"

            return tables.dict_printer(d,
                                      order=['cloud',
                                             'uuid',
                                             'name'],
                                      output=format)
        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.cm_db.close()

