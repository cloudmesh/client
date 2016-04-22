import inspect
import logging

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import path_expand
from cloudmesh_client.default import Default

# define the logger
LOGGER = logging.getLogger('LogUtil')


class LogUtil(object):
    # define global format for logs
    FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(funcName)s() %(message)s"

    # set global key for log
    LOG_LEVEL_KEY = "log_level"

    # default log level is ERROR
    DEFAULT_LOG_LEVEL = "ERROR"

    category = "general"

    @staticmethod
    def save():
        """
        save the loglevel for a cloud to the cloudmesh.yaml file
        """
        # TODO: BUG: this seems inconsistant as loglevels via default
        # can now be defined for clouds, but the yaml file only
        # specifies one value for all clouds.

        # get the log level from database
        log_level = Default.get(
            name=LogUtil.LOG_LEVEL_KEY,
            category=LogUtil.category) or LogUtil.DEFAULT_LOG_LEVEL

        # Update the cloudmesh config
        config = ConfigDict("cloudmesh.yaml")
        config["cloudmesh"]["logging"]["level"] = log_level

        # Save this into cloudmesh yaml
        config.save()

    @staticmethod
    def set_level(log_level):
        """
        sets th eloglevel in the database and the loglevel file from
        cloudmesh.yaml
        :param log_level: the loglevel
        :return:
        """
        # TODO: BUG: This seems inconsistent with our use as it mixes db and
        # cloudmesh.yaml.
        level = log_level.upper()

        Default.set(key=LogUtil.LOG_LEVEL_KEY,
                    value=log_level,
                    category=LogUtil.category)

        # get log level obj
        log_level_obj = LogUtil.get_level_obj(log_level)

        # Read the ConfigDict
        config = ConfigDict("cloudmesh.yaml")
        log_file = config["cloudmesh"]["logging"]["file"]

        # Set the logger config
        logging.basicConfig(format=LogUtil.FORMAT,
                            level=log_level_obj,
                            filename=path_expand(log_file))

        LOGGER.info("Set log level to: " + log_level)
        return "Ok."

    @staticmethod
    def get_level():
        """
        get the log level from database
        :param cloudname: The name of the cloud
        :return: the log level
        """
        log_level = Default.get(name=LogUtil.LOG_LEVEL_KEY,
                                category=LogUtil.category)

        LOGGER.info("Returning Log Level: " + log_level)

        # return the level
        return log_level

    @staticmethod
    def initialize_logging():
        """
        reads the log level from the cloudmesh.yaml file from
        cloudmesh.logging.level. If the value is not set the logging will be
        set to the default which is "ERROR"
        :return: the loglevel
        """
        config = ConfigDict("cloudmesh.yaml")
        log_level = config["cloudmesh"]["logging"]["level"] or LogUtil.DEFAULT_LOG_LEVEL

        print("PPPP", log_level)

        # Set the log level
        LogUtil.set_level(log_level)

        return

    @staticmethod
    def get_logger():
        """
        get caller file name
        :return: file name based on the context where the logger is caller
        """

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        the_class = module.__name__

        # return logger object
        return logging.getLogger(the_class)

    @staticmethod
    def get_level_obj(log_level):
        """
        gets the log level when passing a string
        :param log_level: case insensitive string. Valid values are debug,
                          info, warning, critical, error
        :return: a logging level
        """
        # Return log level obj
        level = log_level.lower()

        if level == "debug":
            log_level = logging.DEBUG
        elif level == "info":
            level = logging.INFO
        elif level == "warning":
            level = logging.WARNING
        elif level == "critical":
            level = logging.CRITICAL
        elif level == "error":
            level = logging.ERROR
        else:
            level = logging.DEBUG

        return level
