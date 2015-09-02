from __future__ import print_function
from pprint import pprint

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.cm import command
from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_base.menu import dict_choice, menu_return_num
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.common.ConfigDict import ConfigDict


class SelectCommand(object):

    topics = {"select": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command key")

    @command
    def do_select(self, args, arguments):
        """
        ::

          Usage:
              select image [CLOUD]
              select flavor [CLOUD]
              select cloud [CLOUD]
              select key [CLOUD]

          selects interactively the default values

          Arguments:

            CLOUD    the name of the cloud

          Options:

        """
        pprint(arguments)
        cloud = arguments["CLOUD"]
        if arguments["image"]:
            pass
        elif arguments["flavor"]:
            pass
        elif arguments["cloud"]:

            config = ConfigDict("cloudmesh.yaml")
            clouds = config["cloudmesh"]["clouds"]

            for key in clouds.keys():
                Console.ok("  " + key)

            number = menu_return_num(title="Select a cloud",
                                     menu_list=clouds.keys(),
                                     tries=10,
                                     with_display=True)
            if number == "q":
                pass
            else:
                cloud = clouds.keys()[number]

            print ("Selected cloud " + cloud)
            Default.set("cloud", cloud, "general")

        elif arguments["key"]:

            db = SSHKeyDBManager()

            d = db.table_dict()

            try:
                element = dict_choice(d)

                keyname = element["name"]
                print("Set default key to ", keyname)
                db.set_default(keyname)
                Default.set("key", keyname, "general")

            except:
                print("ERROR: could not set key")
            pass

        pass


if __name__ == '__main__':
    command = cm_shell_select()
    command.do_select("image")
    command.do_select("flavor")
    command.do_select("cloud")
    command.do_select("key")

