import os

from novaclient import client
import argparse
# TODO: please use docopts even if its just a test

class OpenStackProvider(object):
    # OpenStack Instance
    server = None

    def __init__(self, filename="~/.cloudmesh/cloudmesh.yaml"):
        # TODO: Use ConfigDict to read credentials from ~/.cloudmesh/cloudmesh.yaml
        return

    def getServer(self, serverID):
        # Get values from environment variables
        """
            TODO:
                Get Values from ~/.cloudmesh/cloudmesh.yaml using ConfigDict
                instead of reading environment variables.
        """
        OS_AUTH_URL = os.environ['OS_AUTH_URL']
        OS_USERNAME = os.environ['OS_USERNAME']
        OS_PASSWORD = os.environ['OS_PASSWORD']
        OS_TENANT_NAME = os.environ['OS_TENANT_NAME']
        OS_CACERT = os.environ['OS_CACERT']
        VERSION = 2

        # Initialize the Nova Client
        nova = client.Client(VERSION,
                            OS_USERNAME,
                            OS_PASSWORD,
                            OS_TENANT_NAME,
                            OS_AUTH_URL,
                            OS_CACERT)

        # Get the server using pythobn-novaclient API
        try:
            self.server = nova.servers.get(serverID)
        except:
            print("The OpenStack Instance with ID: [%s] does not exist! " % (serverID))
            return None

        # return the server
        return self.server

    def startServer(self, server):
        # Start the OpenStack instance
        server.start()
        print('Server start request  has been accepted!')
        return

    def stopServer(self, server):
        # Stop the OpenStack instance
        server.stop
        print('Server stop request has been accepted!')
        return

    def rebootServer(self, server):
        # Reboot the OpenStack instance
        server.reboot(reboot_type='SOFT')
        return

if __name__ == "__main__":
    # Define the argument parser
    parser = argparse.ArgumentParser()

    # Specify the commandline arguments
    parser.add_argument("command", help="Operation to perform on the OpenStack VM")
    parser.add_argument("serverid", help="ID of the OpenStack VM")

    # Fetch the arguments
    args = parser.parse_args()

    # Retrieve the Command & ServerID from Args
    command = args.command
    serverID = args.serverid

    # Initialize the OpenStackProvider class
    osProvider = OpenStackProvider()
    instance = osProvider.getServer(serverID)

    if not instance:
        print("Exiting the program!")
        exit(2)

    """
        Execute the desired commands
    """
    if command == "start":
        osProvider.startServer(instance)

    elif command == "stop":
        osProvider.stopServer(instance)

    elif command == "reboot":
        osProvider.rebootServer(instance)
