#coding=utf-8

import os, logging.handlers
import config

LEVELS = {'NOSET': logging.NOTSET,
          'DEBUG': logging.DEBUG,
          'INFO': logging.INFO,
          'WARNING': logging.WARNING,
          'ERROR': logging.ERROR, 
          'CRITICAL': logging.CRITICAL}

flag_console = True if config.cf.get('logging', 'console').upper()=='TRUE' else False

# create logs file folder
def config_logging( file_name='', log_level='', logs_dir='' ):
    '''
    @summary: config logging to write logs to local file
    @param file_name: name of log file
    @param log_level: log level
    '''
    if not logs_dir:
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                config.cf.get('logging', 'log_dir'))
    if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
        pass
    else:
        os.makedirs(logs_dir)

    file_name = file_name if file_name else config.cf.get('logging', 'log_name')
    logs_dir = logs_dir if logs_dir else config.cf.get('logging', 'log_dir')
    file_name = os.path.join(logs_dir, file_name)
    # define a rotating file handler
    rotatingFileHandler = logging.handlers.RotatingFileHandler( filename = file_name,
                                                      maxBytes = 1024 * 1024 * 100,
                                                      backupCount = config.cf.getint("logging", "num_bak_files") )
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(lineno)3d %(levelname)-8s %(message)s")
    rotatingFileHandler.setFormatter(formatter)
    logging.getLogger("").addHandler(rotatingFileHandler)

    if flag_console:
        # define a handler whitch writes messages to sys
        console = logging.StreamHandler()
        # set a format which is simple for console use
        formatter = logging.Formatter("%(name)-12s: %(lineno)d %(levelname)-8s %(message)s")
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger("").addHandler(console)
    
    # set initial log level
    logger = logging.getLogger("")
    
    s = log_level if log_level else config.cf.get('logging', 'level')
    level = LEVELS[s.upper()]
    logger.setLevel(level)
