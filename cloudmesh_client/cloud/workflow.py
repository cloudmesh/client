from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource


class Workflow(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the workflow list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """

        Console.TODO("this method is not yet implemented. dont implement this yet")
        return


        return cls.cm.refresh('workflow', cloud)

    @classmethod
    def delete(cls,cloud, id):
        print (id)
        cls.cm.delete(kind="workflow", category='general' ,cm_id =id)
        return True

    @classmethod
    def list(cls, name, live=False, format="table"):
        """
        This method lists all workflows of the cloud
        :param cloud: the cloud name
        """

        # Console.TODO("this method is not yet implemented")
        # return

        try:

            elements = cls.cm.find(kind="workflow", category='general')

            # pprint(elements)

            # (order, header) = CloudProvider(cloud).get_attributes("workflow")
            order = None
            header= None
            # Console.msg(elements)
            return Printer.write(elements,
                                 order=order,
                                 header=header,
                                 output=format)
        except Exception as ex:
            Console.error(ex.message)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        elements = cls.cm.find(kind="workflow", category='general' ,cm_id =id)
        Console.msg(elements)
        order = None
        header= None
        # Console.TODO("this method is not yet implemented")
        return Printer.write(elements,
                                 order=order,
                                 header=header,
                                 output=format)

    @classmethod
    def save(cls, cloud, name, str):
        workflow = {
                "category": "general",
                "kind": "workflow",
                "name": name,
                "workflow_str": str
        }

        cls.cm.add(workflow, replace=False)
        cls.cm.save()

        return "Workflow saved in database!"

    @classmethod
    def run(cls,cloud,id):
        elements = cls.cm.find(kind="workflow", category='general', cm_id = id)
        Console.msg(elements)
        order = None
        Console.msg("Executing")
        header= None
        return elements
        # Console.TODO("this method is not yet implemented")
        # return Printer.write(elements,
        #                          order=order,
        #                          header=header,
        #                          output=format)
