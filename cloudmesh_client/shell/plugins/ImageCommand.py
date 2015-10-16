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
                image list [--cloud=CLOUD] [--format=FORMAT]

                This lists out the images present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name

            Examples:
                cm image refresh
                cm image list
                cm image list --format=csv

        """
        cloud = arguments["--cloud"] or Default.get("cloud")
        if arguments["refresh"]:
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return
            result = Image.refresh_image_list(cloud)
            Console.msg(result)
            return

        if arguments["list"]:
            if not cloud:
                Console.error("Default cloud doesn't exist")
                return
            output_format = arguments["--format"]
            result = Image.list_images(cloud, output_format)
            print(result)
            return

