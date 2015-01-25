#!/usr/bin/env python
from multiprocessing import Process, Event
import numpy as np
from time import time
import serial

# logging
from log import Log


## Creates a parallel process for data adquisition
#
# Using the multiprocessing python library, creates a parallel process for data
# adquisition from a defined serial port. To avoid data lost, all data is
# returned in a mutiprocessing queue
#
# @param Process Object type
# @author Sebastian Sepulveda
class SerialProcess(Process):
    ## Constructor
    #
    # @param self Object pointer
    # @param queue A queue where adquired data will be returned
    def __init__(self, queue):
        Process.__init__(self)
        self.exit = Event()
        # local variables
        self.ser = serial.Serial()
        self.queue = queue
        # logging
        self.log = Log('SerialProcess')

    ## Process method
    #
    # Starts and holds the adquisition from a opened serial port, splitting
    # the CSV data and putting the processed data in a queue
    #
    # Will run until a @def closePort function is called
    # @param self Object pointer
    # @return Nothing
    def run(self):
        self.init_time = time()
        try:
            while self.ser.isOpen() and not self.exit.is_set():
                data = self.ser.readline().strip()
                try:
                    data = map(float, data.split(','))
                    self.queue.put([time() - self.init_time] + data)
                except:
                    pass
            return
        except:
            self.log.e("Exception in SerialProcess")
            raise
        finally:
            self.closePort()
            self.log.i("Finished SerialProcess normally")

    ## Opens a serial port
    #
    # Trys to open a selected serial port at specified baudrate with 8N1
    # configuration.
    # @param self Object pointer
    # @param port Address for the serial port (default: @c /dev/ttyACM0)
    # @param bd Baudrate for the serial port (default: 115200 kbps)
    # @return
    # + @b True : if the serial port is open
    # + @b False : if the serial port couldn't be open
    def openPort(self, port='/dev/ttyACM0', bd=115200):
        self.ser.port = port
        self.ser.baudrate = bd
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.rtscts = 1
        self.ser.timeout = 0.5

        if self.ser.isOpen():
            return False
        try:
            self.ser.open()
            self.ser.flushInput()
            self.log.i("Opened Serial port" + str(port))
            return True
        except:
            self.log.e("Failed to open Serial port " + str(port))
            return False

    ## Closes the currently opened serial port
    #
    # Inits the Process Event for exiting, finally closing the serial port
    # @param self Object pointer
    def closePort(self):
        self.log.i("Exiting process...")
        self.exit.set()

if __name__ == "__main__":
    import os
    os.system("python main.py")
