#coding=utf-8

import logging.handlers
import os

LEVELS = {'NOSET': logging.NOTSET,
          'DEBUG': logging.DEBUG,
          'INFO': logging.INFO,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR, 
          'CRITICAL': logging.CRITICAL}

# create logs file folder
def config_logging( file_name, log_level, logs_dir ):
    '''
    @summary: config logging to write logs to local file
    @param file_name: name of log file
    @param log_level: log level
    '''
    if not logs_dir:
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.makedirs(logs_dir)

    file_name = os.path.join(logs_dir, file_name)
    # define a rotating file handler
    rotatingFileHandler = logging.handlers.RotatingFileHandler( filename =file_name,
                                                      maxBytes = 1024 * 1024 * 100,
                                                      backupCount = 20 )
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(lineno)3d %(levelname)-8s %(message)s")
    rotatingFileHandler.setFormatter(formatter)
    logging.getLogger("").addHandler(rotatingFileHandler)

    # define a handler whitch writes messages to sys
#     console = logging.StreamHandler()
    # set a format which is simple for console use
#     formatter = logging.Formatter("%(name)-12s: %(lineno)d %(levelname)-8s %(message)s")
    # tell the handler to use this format
#     console.setFormatter(formatter)
    # add the handler to the root logger
#     logging.getLogger("").addHandler(console)
    # set initial log level
    logger = logging.getLogger("")
    level = LEVELS[log_level.upper()]
    logger.setLevel(level)
