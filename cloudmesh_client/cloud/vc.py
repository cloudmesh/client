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


    '''
    vc key list NAMES [--usort]
    '''

    @classmethod
    def list(cls, names, usort=False, format="table"):
        """
        This method lists all vcs of the cloud
        :param cloud: the cloud name
        """

        Console.error("NOT YET IMPLEMENTED")
        return None




