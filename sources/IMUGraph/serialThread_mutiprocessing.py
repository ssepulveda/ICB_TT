# QT thread
from PyQt4 import QtCore
from baseThread import BaseThread

# Serial
import serial

# Import IMU converters and scalers; senor fusion
from imu import IMU
from sensorFusion import SensorFusion

# Set Debug
from log import Log
log = Log("SerialThread")
log.setVerbose(False)


## Obtain and scale serial data in a thread
#
# Based on the BaseThread methods, enables a Qt4 thread for adquiring
# data from a serial port, using a Qt4 signal to interrupt Qt4 main
# thread process.
# @param BaseThread Basic class for thread handling
class SerialThread(BaseThread):
    ser = serial.Serial()
    A = [.0]*3
    G = [.0]*3
    M = [.0]*3
    E_dmp = [.3]*3
    E = [.0]*3
    LA = [.0]*3

    ## Constructor
    #
    # Enables the basic thread functions and logs
    # @param self The object pointer
    def __init__(self, device='MPU-9150'):
        BaseThread.__init__(self)
        log.d("Init serialThread")
        # configure and retrieve IMU scales
        self.imu = IMU(device)
        self.csvScale = self.imu.getScaleVector()
        self.csvSize = len(self.csvScale)
        self.range_accel = self.imu.getRangeAccelerometer()
        self.range_gyro = self.imu.getRangeGyroscope()
        self.range_mag = self.imu.getRangeMagnetometer()
        self.range_euler = self.imu.getRangeEuler()
        # star sensor fusion
        self.fusion = SensorFusion()

    ## Open the defined point
    #
    # Configures the serial port, address and speed, and verifies
    # correct initialization and status
    # @param self The object pointer
    def openPort(self, port='/dev/ttyUSB0', baud=115200):
        try:
            # configure port
            self.ser.port = port
            self.ser.baudrate = baud
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.rtscts = 1
            self.ser.timeout = 0.5

            # open port
            if self.ser.isOpen():
                log.w("Port is already open, closing it")
                self.ser.close()
            self.ser.open()
            # clear input
            self.ser.flushInput()
            # verify that port is open
            if self.ser.isOpen():
                log.d("Port "+port+" opened at "+str(baud))
        except serial.SerialException as se:
            log.e("Unable to open port %s" % port)
        except:
            raise

    ## The thread process itself
    #
    # Defines the "loop" method of the thread
    # + Obtain self.data from the defined self.serial port
    # + Separate in CSV format
    # + Assuming the input from a MPU-9150, scales self.data
    # + Manage incorrect CSV format (by size)
    # + Manage incomplete self.data transfer
    # + Notify main thread (Qt4) with a signal
    # @param self The objetc pointer
    def run(self):
        while not self.exiting and self.ser.isOpen():
            try:
                # check if there is self.data avaliable
                if self.ser.inWaiting() > 0:
                    raw = self.ser.readline().strip()
                    log.v(raw)
                    try:
                        # convert received data to a float list
                        data = map(float, raw.split(','))
                        # if got correct data size, scale it
                        if len(data) == self.csvSize:
                            for i in range(0, self.csvSize):
                                data[i] *= self.csvScale[i]
                            
                            # accelerometer
                            for i in self.range_accel:
                                self.A[i-self.range_accel[0]] = data[i]
                            # gyroscope
                            for i in self.range_gyro:
                                self.G[i-self.range_gyro[0]] = data[i]
                            # magnetometer
                            for i in self.range_mag:
                                self.M[i-self.range_mag[0]] = data[i]
                            # euler if its avaliable
                            if self.E_dmp[0] != -1:
                                for i in self.range_euler:
                                    self.E_dmp[i-self.range_euler[0]] = data[i]

                            # do sensor fusion
                            self.fusion.update9DOF(self.G, self.A, self.M)
                            self.LA = self.fusion.getLinearAcceleration()
                            self.E = self.fusion.getYawPitchRoll(True)

                            # notify new data is ready
                            self.emit(QtCore.SIGNAL('newData()'))

                        else:
                            log.d('Incorrect data format')
                            self.ser.flushInput()
                            pass
                    except:
                        self.ser.flushInput()
                        log.v("Skipping incomplete transfer")
                        pass
            except:
                self.closePort()
                log.e("Thread Stopped by unknow error")
                return
        log.d("Thread Stopped Normally")
        return

    ## Closes the self.serial port and waits for the thread to stop
    #
    # @param self The objet pointer#
    def closePort(self):
        log.i("Waiting Thread to stop...")
        while self.isRunning():
            self.exiting = True
            self.exit()
        self.ser.close()
        log.d("Port closed")

    def getAcceleration(self):
        return self.A

    def getLinearAccel(self):
        return self.LA

    def getGyroscope(self):
        return self.G

    def getMagnetometer(self):
        return self.M

    def getEulerDMP(self):
        return self.E_dmp

    def getEuler(self):
        return self.E
