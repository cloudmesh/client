from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource


'''


stdin, stdout, stderr = Shell.kegyen('ssh-keygen -t rsa -f id_rsa.key')
stdin, stdout, stderr = Shell.cat('id_rsa.key.pub')


class DistributeKeys(object):

    def read_ips(filename):

fo = open(<IP_LIST_FILE>, "rw+")

pubkeys = []


for ln in fo:
    ip = ln.split(",")
    usr = ip[0]
    addr = ip[1].replace('\n', '')
    op =stdout.read().splitlines()
    pubkeys.append(op[0])



full_keylst = open("team_pub_keys.txt","a")
for k in pubkeys:
    full_keylst.write(k+"\n")

fo = open("ips.txt", "rw+")
for ln in fo:
    ip = ln.split(",")
    usr = ip[0]
    addr = ip[1].replace('\n', '')
    print "Connecting to ",addr
    sftp = ssh.open_sftp()
    f = sftp.open("~/.ssh/authorized_keys",'w')
    keys = open("team_pub_keys.txt","r")
    for key in keys:
        f.write(key)
    print "Public keys written into",addr
    f.close()
    ssh.close()

'''


class Vc(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the vc list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """

        return cls.cm.refresh('vc', cloud)

    @classmethod
    def list(cls, cloud, live=False, format="table"):
        """
        This method lists all vcs of the cloud
        :param cloud: the cloud name
        """

        try:

            if live:
                cls.refresh(cloud)

            elements = cls.cm.find(kind="vc", category=cloud)

            # pprint(elements)

            (order, header) = CloudProvider(cloud).get_attributes("vc")

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

        return CloudProvider(cloud).details('vc', cloud, id, format)


