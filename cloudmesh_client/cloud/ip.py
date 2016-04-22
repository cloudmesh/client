from __future__ import print_function

import socket
from uuid import UUID

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

from pprint import pprint
from builtins import input


# noinspection PyBroadException,PyPep8Naming
class Ip(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def list(cls, cloud=None, names=None, output='table', live=False):

        try:

            if live:
                cls.refresh(cloud)

            elements = cls.cm.find(kind="vm", category=cloud)
            result = []
            if "all" in names:
                for element in elements:
                    result.append(element)
            elif names is not None:
                for element in elements:
                    if element["name"] in names:
                        result.append(element)

            (order, header) = CloudProvider(cloud).get_attributes("ip")

            return Printer.write(result,
                                 order=order,
                                 header=header,
                                 output=output)
        except Exception as ex:
            Console.error(ex.message)





            # def list_floating_ip_pools(self, **kwargs):
            #        return self._to_dict(self.provider.floating_ip_pools.list())
