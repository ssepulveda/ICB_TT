from PyQt4 import QtCore


## Defines basic methods for dealing with Qt Threads and all Threads
#
# Implement handles for the events of the Qt Threads and UI elements
# (main thread and UI thread).
class BaseThread(QtCore.QThread):
    ## Constructor
    #
    # Initializes threads
    # @param self The objetc pointer
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.exiting = False

    ## Deconstructor
    #
    # Closes and exits from threads
    # @param self The objetc pointer
    def __del__(self):
        ## Notifies all threads to stop
        self.exiting = True
        self.wait()
