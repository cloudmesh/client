from __future__ import print_function
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class ImageCommand(object):
    topics = {"image": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command image")

    @command
    def do_image(self, args, arguments):
        """
        ::

            Usage:
                image refresh [--cloud=CLOUD]
                image list [ID] [--cloud=CLOUD] [--format=FORMAT] [--refresh]

                This lists out the images present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        live data taken from the cloud

            Examples:
                cm image refresh
                cm image list
                cm image list --format=csv
                cm image show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh

        """
        cloud = arguments["--cloud"] or Default.get("cloud")
        if arguments["refresh"]:
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return
            result = Image.refresh(cloud)
            Console.msg(result)
            return

        if arguments["list"]:

            id = arguments['ID']
            output_format = arguments["--format"]
            live = arguments['--refresh']
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return

            output_format = arguments["--format"]
            if id is None:
                result = Image.list(cloud, output_format)
            else:
                result = Image.details(cloud, id, live, output_format)
            if result is None:

                Console.error("Could not find this image.")
            # Todo:
            # if database size = 0:
            #    Console.error("No images in the database, please refresh.")

            print(result)
            return

