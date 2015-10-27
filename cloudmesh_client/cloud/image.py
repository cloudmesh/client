from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.common.authenticate import Authenticate


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
    def refresh(cls, cloud):
        """
        This method would refresh the image list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        # set the environment
        nova = Authenticate.get_environ(cloud)

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
    def list(cls, cloud, format="table"):
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
                                      order=['uuid',
                                             'name',
                                             'cloud'],
                                      output=format)
        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.cm_db.close()

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            # taken live information from openstack
            nova = Authenticate.get_environ(cloud)
            details = nova.images.get(id)._info
            d = {}
            count = 0
            for key in details.keys():
                if key != 'links':
                    if key == 'metadata':
                        for meta_key in details['metadata'].keys():
                            d[count] = {}
                            d[count]["Property"], d[count]["Value"] = \
                                'metadata '+meta_key, details['metadata'][meta_key]
                            count += 1
                    elif key == 'server':
                        d[count] = {}
                        d[count]["Property"], d[count]["Value"] = key, details['server']['id']
                        count += 1
                    else:
                        d[count] = {}
                        d[count]["Property"], d[count]["Value"] = key, details[key]
                        count += 1
            return tables.dict_printer(d, order=['Property',
                                                 'Value'],
                                       output=format)

        else:
            # data taken from local database
            try:
                element = cls.cm_db.query(model.IMAGE).filter(
                    model.IMAGE.cloud == cloud,
                    model.IMAGE.uuid == id
                ).first()

                d = {}
                if element:
                    for i, key in enumerate(element.__dict__.keys()):
                        if not key.startswith("_sa"):
                            d[i] = {}
                            d[i]["Property"], d[i]["Value"] = key, str(element.__dict__[key])
                return tables.dict_printer(d, order=['Property',
                                                     'Value'],
                                           output=format)
            except Exception as ex:
                Console.error(ex.message, ex)
            finally:
                cls.cm_db.close()


if __name__ == "__main__":
    Image.details("india", "58c9552c-8d93-42c0-9dea-5f48d90a3188")