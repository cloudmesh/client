import inspect
import logging
from cloudmesh_base.util import path_expand
from cloudmesh_client.common.ConfigDict import ConfigDict

class LogUtil(object):

    # TODO: review DebugCOmmand as example
    # TODO: cm has loglevel command, please review what it does

    @staticmethod
    def save(loglevel):
        """Saves the current log level to the yaml file and the database"""
        # TODO: implement see configdict save, see examples on how we set
        # defaults
        raise ValueError("not yet implemented")

    @staticmethod
    def set(loglevel):
        """Saves the current log level to the database"""
        # TODO: implement see configdict save, see examples on how we set
        # defaults
        raise ValueError("not yet implemented")


    @staticmethod
    def get():
        """Returns the loglevel set in the database. If the values is not
        set it is read from the yaml file and than written into the
        database. If the value is not set in the yaml file, The value is set
        to ERROR"""
        # TODO: implement
        raise ValueError("not yet implemented")


    @staticmethod
    def init_logging():
        # TODO: method name is awkward
        # TODO: implement get and set methed oand use that in this method
        # TODO: make FORMAT a variable global to the class
        logger = logging.getLogger('LogUtil')
        FORMAT = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)s %(funcName)s() %(message)s"

        # Read the ConfigDict
        config = ConfigDict("cloudmesh.yaml")
        log_dict = config["cloudmesh"]["logging"]
        log_level = log_dict["level"]
        log_file = log_dict["file"]

        # Define Log Level
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

        # Set the logger config
        logging.basicConfig(format=FORMAT, level=log_level, filename=path_expand(log_file))

        # TODO: I do not think its necessary to send a message that the
        # logger was started
        logger.info("Logger Initialized!")

    @staticmethod
    def get_logger():
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        the_class = module.__name__

        return logging.getLogger(the_class)