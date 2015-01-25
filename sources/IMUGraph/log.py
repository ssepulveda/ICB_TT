

## General logging for debugging
#
# Some simple debugging tools for enabling/disabling prints
class Log:
    ## Tag name for the log reference
    TAG = ""
    ## Initial status for the debug methods
    DEBUG = None
    ## Initial status for the error methods
    ERROR = None
    ## Initial status for the info methods
    INFO = None
    ## Initial status for the verbose methods
    VERBOSE = None
    ## Initial status for the warning methods
    WARN = None

    ## Constructor
    #
    # Initialices the log and defines the TAG value
    # @param self The object pointer
    # @param tag String with the name
    # @param debug define the output of debug methods
    # @param error define the output of error methods
    # @param info define the output of info methods
    # @param verbose define the output of verbose methods
    # @param warn define the output of warning methods
    def __init__(self, tag, debug=True, error=True, info=False, verbose=False,
                 warn=False):
        self.TAG = tag
        self.DEBUG = debug
        self.ERROR = error
        self.INFO = info
        self.VERBOSE = verbose
        self.WARN = warn

    ## Prints debugging messages
    #
    # @param self The object pointer
    # @param txt The message to print
    def d(self, txt):
        if self.DEBUG is True:
            print self.TAG+":DEBUG: "+txt

    ## Prints debugging errors
    #
    # @param self The object pointer
    # @param txt The message to print
    def e(self, txt):
        if self.ERROR is True:
            print self.TAG+":ERROR: "+txt

    ## Prints debugging informations
    #
    # @param self The object pointer
    # @param txt The message to print
    def i(self, txt):
        if self.INFO is True:
            print self.TAG+":INFO: "+txt

    ## Prints debugging verboses
    #
    # @param self The object pointer
    # @param txt The message to print
    def v(self, txt):
        if self.VERBOSE is True:
            print self.TAG+":VERBOSE: "+txt

    ## Prints debugging warnings
    #
    # @param self The object pointer
    # @param txt The message to print
    def w(self, txt):
        if self.WARN is True:
            print self.TAG+":WARNING: "+txt

    ## Enables/Disables messages from debugs
    #
    # @param self The object pointer
    # @param bool_ The status for the debuggin method
    # + @b TRUE : enabled
    # + @b FALSE : disabled
    def setDebug(self, bool_):
        self.DEBUG = bool_

    ## Enables/Disables messages from errors
    #
    # @param self The object pointer
    # @param bool_ The status for the debuggin method
    # + @b TRUE : enabled
    # + @b FALSE : disabled
    def setError(self, bool_):
        self.ERROR = bool_

    ## Enables/Disables messages from infos
    #
    # @param self The object pointer
    # @param bool_ The status for the debuggin method
    # + @b TRUE : enabled
    # + @b FALSE : disabled
    def setInfo(self, bool_):
        self.INFO = bool_

    ## Enables/Disables messages from verboses
    #
    # @param self The object pointer
    # @param bool_ The status for the debuggin method
    # + @b TRUE : enabled
    # + @b FALSE : disabled
    def setVerbose(self, bool_):
        self.VERBOSE = bool_

    ## Enables/Disables messages from warnings
    #
    # @param self The object pointer
    # @param bool_ The status for the debuggin method
    # + @b TRUE : enabled
    # + @b FALSE : disabled
    def setWarning(self, bool_):
        self.WARN = bool_

    ## Getter for the status for printing debugs
    #
    # @param self The object pointer
    # @return status of the debuggin
    def getDebug(self):
        return self.DEBUG

    ## Getter for the status for printing errors
    #
    # @param self The object pointer
    # @return status of the debuggin
    def getError(self):
        return self.ERROR

    ## Getter for the status for printing infos
    #
    # @param self The object pointer
    # @return status of the debuggin
    def getInfo(self):
        return self.INFO

    ## Getter for the status for printing verboses
    #
    # @param self The object pointer
    # @return status of the debuggin
    def getVerbose(self):
        return self.VERBOSE

    ## Getter for the status for printing warnings
    #
    # @param self The object pointer
    # @return status of the debuggin
    def getWarning(self):
        return self.WARN
