import inspect
import logging
from cloudmesh_base.util import path_expand
from cloudmesh_client.common.ConfigDict import ConfigDict

class LogUtil(object):

    @staticmethod
    def init_logging():
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

        logger.info("Logger Initialized!")

    @staticmethod
    def get_logger():
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        the_class = module.__name__

        return logging.getLogger(the_class)