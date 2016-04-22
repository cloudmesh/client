from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudPluginCommand, ShellPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.LogUtil import LogUtil

# get the logger
LOGGER = LogUtil.get_logger()


class LogLevelCommand(PluginCommand, CloudPluginCommand, ShellPluginCommand):
    topics = {"loglevel": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command loglevel")

    # noinspection PyUnusedLocal
    @command
    def do_loglevel(self, args, arguments):
        """
        ::

            Usage:
                loglevel set MODE [--cloud=CLOUD]
                loglevel get [--cloud=CLOUD]
                loglevel save [--cloud=CLOUD]

            Arguments:
                MODE    log level mode [DEBUG/INFO/WARNING/CRITICAL/ERROR]

            Options:
                --cloud=CLOUD    the name of the cloud

        Description:
            loglevel command sets the default logging level
            for a cloud.

        Examples:
            loglevel set DEBUG --cloud=kilo
                sets the default log level to DEBUG for kilo.

            loglevel get --cloud=kilo
                retreives the default log level for kilo cloud.

            loglevel save --cloud=kilo
                saves the log level preference to the db & yaml file.

        """
        # pprint(arguments)

        cloud = arguments["--cloud"] or Default.cloud
        LOGGER.info("Cloud: " + cloud + ", Arguments: " + str(arguments))

        if arguments["set"]:
            try:
                log_level = arguments["MODE"]
                response = LogUtil.set_level(log_level=log_level,
                                             cloudname=cloud)

                if response is not None:
                    Console.ok(response)
            except Exception as ex:
                Console.error(ex.message)

        elif arguments["get"]:
            try:
                log_level = LogUtil.get_level(cloudname=cloud)
                Console.ok("Current Log Level = " + log_level + ". Ok.")
            except Exception as ex:
                Console.error(ex.message)

        elif arguments["save"]:
            LogUtil.save(cloudname=cloud)
            pass
