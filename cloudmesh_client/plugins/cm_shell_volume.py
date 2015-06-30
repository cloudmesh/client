from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_volume import command_volume


class cm_shell_volume:
    def activate_cm_shell_volume(self):
        self.register_command_topic('cloud', 'volume')

    @command
    def do_volume(self, args, arguments):
        """
        ::

            Usage:
                volume list
                volume create SIZE
                              [--snapshot-id=SNAPSHOT-ID]
                              [--image-id=IMAGE-ID]
                              [--display-name=DISPLAY-NAME]
                              [--display-description=DISPLAY-DESCRIPTION]
                              [--volume-type=VOLUME-TYPE]
                              [--availability-zone=AVAILABILITY-ZONE]
                volume delete VOLUME
                volume attach SERVER VOLUME DEVICE
                volume detach SERVER VOLUME
                volume show VOLUME
                volume SNAPSHOT-LIST
                volume snapshot-create VOLUME-ID
                                       [--force]
                                       [--display-name=DISPLAY-NAME]
                                       [--display-description=DISPLAY-DESCRIPTION]
                volume snapshot-delete SNAPSHOT
                volume snapshot-show SNAPSHOT
                volume help


            volume management

            Arguments:
                SIZE              Size of volume in GB
                VOLUME            Name or ID of the volume to delete
                VOLUME-ID         ID of the volume to snapshot
                SERVER            Name or ID of server(VM).
                DEVICE            Name of the device e.g. /dev/vdb. Use "auto" for
                                  autoassign (if supported)
                SNAPSHOT          Name or ID of the snapshot

            Options:
                --snapshot-id SNAPSHOT-ID     Optional snapshot id to create
                                              the volume from.  (Default=None)
                --image-id IMAGE-ID           Optional image id to create the
                                              volume from.  (Default=None)
                --display-name DISPLAY-NAME   Optional volume name. (Default=None)
                --display-description DISPLAY-DESCRIPTION
                                              Optional volume description. (Default=None)
                --volume-type VOLUME-TYPE
                                              Optional volume type. (Default=None)
                --availability-zone AVAILABILITY-ZONE
                                              Optional Availability Zone for
                                              volume. (Default=None)
                --force                       Optional flag to indicate whether to snapshot a
                                              volume even if its
                                              attached to an
                                              instance. (Default=False)

            Description:
                volume list
                    List all the volumes
                volume create SIZE [options...]
                    Add a new volume
                volume delete VOLUME
                    Remove a volume
                volume attach SERVER VOLUME DEVICE
                    Attach a volume to a server
                volume-detach SERVER VOLUME
                    Detach a volume from a server
                volume show VOLUME
                    Show details about a volume
                volume snapshot-list
                    List all the snapshots
                volume snapshot-create VOLUME-ID [options...]
                    Add a new snapshot
                volume snapshot-delete SNAPSHOT
                    Remove a snapshot
                volume-snapshot-show SNAPSHOT
                    Show details about a snapshot
                volume help
                    Prints the nova manual

        """
        # pprint(arguments)
        if arguments["list"]:
            Console.ok('list all the volumes')
        elif arguments["create"]:
            size = arguments["SIZE"]
            snapshot_id = arguments["--snapshot-id"]
            image_id = arguments["--image-id"]
            display_name = arguments["--display-name"]
            display_description = arguments["--display-description"]
            volume_type = arguments["--volume-type"]
            availability_zone = arguments["--availability-zone"]
            Console.ok(
                'create {} {} {} {} {} {} {}'.format(size,
                                                     snapshot_id,
                                                     image_id,
                                                     display_name,
                                                     display_description,
                                                     volume_type,
                                                     availability_zone))
        elif arguments["delete"]:
            volume = arguments["VOLUME"]
            Console.ok('delete volume {}'.format(volume))
        elif arguments["attach"]:
            server = arguments["SERVER"]
            volume = arguments["VOLUME"]
            device = arguments["DEVICE"]
            Console.ok('attach {} {} {}'.format(server, volume, device))
        elif arguments["detach"]:
            server = arguments["SERVER"]
            volume = arguments["VOLUME"]
            Console.ok('detach {} {}'.format(server, volume))
        elif arguments["show"]:
            volume = arguments["VOLUME"]
        elif arguments["SNAPSHOT-LIST"]:
            snapshot_list = arguments["SNAPSHOT-LIST"]
            Console.ok('snapshot-list {}'.format())
        elif arguments["snapshot-create"]:
            volume_id = arguments["VOLUME-ID"]
            force = arguments["--force"]
            display_name = arguments["--display-name"]
            display_description = arguments["--display-description"]
            Console.ok('snapshot-create {} {} {} {}'.format(volume_id,
                                                            force,
                                                            display_name,
                                                            display_description))
        elif arguments["snapshot-delete"]:
            snapshot = arguments["SNAPSHOT"]
            Console.ok('snapshot-delete {}'.format(snapshot))
        elif arguments["snapshot-show"]:
            snapshot = arguments["SNAPSHOT"]
            Console.ok('snapshot-show {}'.format(snapshot))
        pass


if __name__ == '__main__':
    command = cm_shell_volume()
    command.do_volume("list")
    command.do_volume("a=x")
    command.do_volume("x")
