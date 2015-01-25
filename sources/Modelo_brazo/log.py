#!/usr/bin/env python
import logging


## Log handler for de logging module
#
# Creates "simplier" wrappers for the logging function, keeping the same
# format for all modules using it
#
# @author Sebastian Sepulveda
class Log:
    ## Constructor of the Log class
    #
    # Defines the format of the output and the streamer
    # @param self Object pointer
    # @param title Name for the formatter (module or instance name)
    def __init__(self, title):
        log = logging.getLogger(title)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('[%(name)s:%(levelname)s] ' +
                                               '%(message)s'))
        log.addHandler(handler)
        self.log = log

    ## Sets the level for logging
    #
    # @param self Object pointer
    # @param level String with the Level name to set. Valid values are:
    # @c CRITICAL, @c ERROR, @c WARNING, @c INFO and @c DEBUG.
    def setLevel(self, level):
        if level == 'CRITICAL':
            self.log.setLevel(logging.CRITICAL)
        elif level == 'ERROR':
            self.log.setLevel(logging.ERROR)
        elif level == 'WARNING':
            self.log.setLevel(logging.WARNING)
        elif level == 'INFO':
            self.log.setLevel(logging.INFO)
        elif level == 'DEBUG':
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.DEBUG)

    ## Returns the level for logging
    #
    # @param Object Pointer
    # @return Logging level
    # @todo Not working properly
    def getLevel(self):
        #~ return int(self.log.getLevelName())
        return logging.getLogger().getEffectiveLevel()

    ## Logs text as critical
    #
    # @param self Object pointer
    # @param txt String to log
    def c(self, txt):
        self.log.critical(str(txt))

    ## Logs text as error
    #
    # @param self Object pointer
    # @param txt String to log
    def e(self, txt):
        self.log.error(txt)

    ## Logs text as warning
    #
    # @param self Object pointer
    # @param txt String to log
    def w(self, txt):
        self.log.warning(txt)

    ## Logs text as info
    #
    # @param self Object pointer
    # @param txt String to log
    def i(self, txt):
        self.log.info(txt)

    ## Logs text as debug
    #
    # @param self Object pointer
    # @param txt String to log
    def d(self, txt):
        self.log.debug(txt)
