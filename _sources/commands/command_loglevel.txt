Loglevel Command
======================================================================

The cloudmesh loglevel command provides you with the ability to easily
switch on and control the level of logging.

The manual page of the  command can be found at: `list
<../man/man.html#loglevel>`_



loglevel set MODE

eg: loglevel set DEBUG
This command will save the log level preference for the user in the database

loglevel get

This command will return the current log level preference.
Checks the database, if no log level set in the db, it returns from cloudmesh.yaml file

loglevel save

This command will save the current log level preference to the cloudmesh.yaml file (and the db).

 cloudmesh.yaml file is getting updated correctly.
Again, using the logger is simple.

Usage in API:

from cloudmesh_client.common.LogUtil import LogUtil
# get the logger
LOGGER = LogUtil.get_logger()
LOGGER.info("Cloud: " + cloud + ", Arguments: " + str(arguments))
