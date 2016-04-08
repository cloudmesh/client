from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.menu import menu_return_num
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.cloud.key import Key

# noinspection PyBroadException,PyBroadException
class SelectCommand(PluginCommand, CloudPluginCommand):
    topics = {"select": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command select")

    # noinspection PyUnusedLocal
    @command
    def do_select(self, args, arguments):
        """
        ::

          Usage:
              select image [CLOUD] [--refresh]
              select flavor [CLOUD] [--refresh]
              select cloud [CLOUD]
              select key [CLOUD]

          selects interactively the default values

          Arguments:

            CLOUD    the name of the cloud

          Options:

            --refresh   refreshes the data before displaying it
                        from the cloud

        """
        # pprint(arguments)
        cloud = arguments["CLOUD"] or Default.cloud
        if arguments["image"]:
            try:
                refresh = arguments['--refresh'] or Default.refresh
                if refresh:
                    Image.refresh(cloud)

                image_dict = Image.list(cloud, format="dict")

                image_names = list()
                for image in list(image_dict.values()):
                    image_names.append(image["name"])

                number = menu_return_num(title="Select an Image",
                                         menu_list=image_names,
                                         tries=10,
                                         with_display=True)

                if number == "q":
                    pass
                else:
                    image = image_names[number]
                    print("Selected image " + image)
                    Default.set("image", image, category=cloud)
            except:
                print("ERROR: could not set image.")

        elif arguments["flavor"]:
            try:
                refresh = arguments['--refresh'] or Default.refresh
                if refresh:
                    Flavor.refresh(cloud)

                flavor_dict = Flavor.list(cloud, format="dict")

                flavor_names = list()
                for flavor in list(flavor_dict.values()):
                    flavor_names.append(flavor["name"])

                number = menu_return_num(title="Select a Flavor",
                                         menu_list=flavor_names,
                                         tries=10,
                                         with_display=True)

                if number == "q":
                    pass
                else:
                    flavor = flavor_names[number]
                    print("Selected flavor " + flavor)
                    Default.set("flavor", flavor, category=cloud)
            except:
                print("ERROR: could not set flavor.")

        elif arguments["cloud"]:
            try:
                config = ConfigDict("cloudmesh.yaml")
                clouds = config["cloudmesh"]["clouds"]

                for key in clouds:
                    Console.ok("  " + key)

                number = menu_return_num(title="Select a cloud",
                                         menu_list=list(clouds),
                                         tries=10,
                                         with_display=True)
                if number == "q":
                    pass
                else:
                    cloud = list(clouds)[number]
                    print("Selected cloud " + cloud)
                    Default.set("cloud", cloud, "general")
            except:
                print("ERROR: could not set cloud.")

        elif arguments["key"]:
            try:
                #db = SSHKeyDBManager()

                key_dict = Key.all(output='dict')

                key_names = list()
                for key in key_dict.values():
                    key_names.append(key["name"])

                number = menu_return_num(title="Select a Key",
                                         menu_list=key_names,
                                         tries=10,
                                         with_display=True)

                if number == "q":
                    pass
                else:
                    key = key_names[number]
                    print("Selected key " + key)

                    # TODO Fix default key setting in key DB
                    # db.set_default(key)

                    Default.set("key", key, category=cloud)
            except:
                print("ERROR: could not set key")

        return ""

