import inspect
import logging
from cloudmesh_base.util import path_expand
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.common.ConfigDict import ConfigDict

# define global format for logs
FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(funcName)s() %(message)s"

# set global key for log
LOG_LEVEL_KEY = "log_level"

# default log level is ERROR
DEFAULT_LOG_LEVEL = "ERROR"

# define the logger
LOGGER = logging.getLogger('LogUtil')


class LogUtil(object):


    @staticmethod
    def save(cloudname):
        # Update the ConfigDict
        config = ConfigDict("cloudmesh.yaml")

        # get the log level from database
        log_level = Default.get(key=LOG_LEVEL_KEY,
                                cloud=cloudname) or \
                    DEFAULT_LOG_LEVEL

        # Update the cloudmesh config
        config["cloudmesh"]["logging"]["level"] = log_level

        # Save this into cloudmesh yaml
        config.save()

        return

    @staticmethod
    def set_level(log_level, cloudname):
        # set default log level
        Default.set(key=LOG_LEVEL_KEY,
                    value=log_level,
                    cloud=cloudname)

        # get log level obj
        log_level_obj = LogUtil.get_level_obj(log_level)

        # Read the ConfigDict
        config = ConfigDict("cloudmesh.yaml")
        log_file = config["cloudmesh"]["logging"]["file"]

        # Set the logger config
        logging.basicConfig(format=FORMAT, level=log_level_obj, filename=path_expand(log_file))

        LOGGER.info("Set log level to: " + log_level)
        return "Ok."

    @staticmethod
    def get_level(cloudname):
        # get the log level from database
        log_level = Default.get(key=LOG_LEVEL_KEY,
                                cloud=cloudname)

        LOGGER.info("Returning Log Level: " + log_level)

        # return the level
        return log_level

    @staticmethod
    def initialize_logging():
        # Read the ConfigDict
        config = ConfigDict("cloudmesh.yaml")
        log_level = config["cloudmesh"]["logging"]["level"] or \
                    DEFAULT_LOG_LEVEL

        # Get default cloud
        cloudname = Default.get_cloud()

        # Set the log level
        LogUtil.set_level(log_level, cloudname)

        return


    @staticmethod
    def get_logger():

        # get caller file name
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        the_class = module.__name__

        # return logger object
        return logging.getLogger(the_class)


    @staticmethod
    def get_level_obj(log_level):
        # Return log level obj
        if log_level == "DEBUG":
            log_level = logging.DEBUG
        elif log_level == "INFO":
            log_level = logging.INFO
        elif log_level == "WARNING":
            log_level = logging.WARNING
        elif log_level == "CRITICAL":
            log_level = logging.CRITICAL
        elif log_level == "ERROR":
            log_level = logging.ERROR
        else:
            log_level = logging.DEBUG

        return log_level