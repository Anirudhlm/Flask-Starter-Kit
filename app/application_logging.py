#!/usr/bin/env python

import logging

class ApplicationLogger:
   """ A class that standarizes the use of the python logging module by
       by delegating to the standard logging module to set the format 
       string, log path, and logger name.
    """
    def __init__(self, log_path = './', logger_name='', 
                 log_level=logging.DEBUG):
        """ Constructor
            Arguments:
               log_path:    The path to log file
               logger_name: The entity name associated with log entries
                            from this logger instance.
        """ 

        self.log_path = log_path
        self.logger_name = logger_name
        self.log_format = ('%(asctime)-15s %(levelname)s %(name)s %(lineno)s '
                           '%(message)s')
        logging.basicConfig(format=self.log_format, filename=self.log_path, 
                            level=log_level)

    def getLogger(self):
         """ Returns a logger 
         """
         return logging.getLogger(self.logger_name)
