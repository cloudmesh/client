
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.shell.command import command
from cloudmesh_client.cloud.key import Key
from cloudmesh_client.shell.console import Console

class AkeyCommand(PluginCommand, CloudPluginCommand):
    topics = {"akey": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command akey")

    @command
    def do_akey(self, args, arguments):
        """
        ::

           Usage:
           akey
           akey list
           akey add --name=key-name --pub=pub-key-path --cert=certificate-file-path --pfx=pfx-file-path
        """
        # pprint("Akey command pressed")
        # pprint(args)
        # pprint(arguments)
        if arguments['list']:
            print("Key list time")
        elif arguments['add']:
            Console.info("Azure key addition invoked")
            if arguments['--name']:
                print("name:"+arguments['--name'])
                key_name = arguments['--name']
            if arguments['--cert']:
                print("cert:"+arguments['--cert'])
                certificate_path = arguments['--cert']
            if arguments['--pub']:
                print("pub:"+arguments['--pub'])
                key_path = arguments['--pub']
            if arguments['--pfx']:
                print("pfx:"+arguments['--pfx'])
                pfx_path = arguments['--pfx']
            Key.add_azure_key_to_db(key_name, key_path, certificate_path, pfx_path)
        return ""
