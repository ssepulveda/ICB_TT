#!/usr/bin/env python

# Imports
import sys
from gui import *
from serialThread import SerialThread
from serial.tools import list_ports

# csv export
from csvExport import CSVExport

# detection algorithms imports
from activityDetection import ActivityDetection
from fallDetection import FallDetection
from posture import Posture

# openGL cube for rotations
from cube import Cube

# Set Debug
from log import Log
log = Log("Main")
log.setVerbose(False)
log.setInfo(False)

# Buffer size for the data and plot buffers
WINDOW = 1024*3
UPDATE_SIZE = -3
RANGE_ACCEL = 2.0
RANGE_GYRO = 2000.0
RANGE_MAG = 1
RANGE_EULER = 180


## Managing and plotting adquired data
#
# @param QtGui.QMainWindow Qt4 Main Window reference
class MainWindow(QtGui.QMainWindow):
    ## Configures initial settings of the window.
    #
    # Initialize data, plots, imported functions and timers
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables
        self.resetData()
        ## Reference update plot timer
        #
        # Qt4 timer to trigger the @updatePlot function
        self.timer = QtCore.QTimer(self)
        ## Qt4 timer for activity
        self.timerActivity = QtCore.QTimer(self)

        # Qt signals
        # start button signal
        QtCore.QObject.connect(self.ui.pButton_Start,
                               QtCore.SIGNAL('clicked()'), self.start)
        # stop button signal
        QtCore.QObject.connect(self.ui.pButton_Stop,
                               QtCore.SIGNAL('clicked()'), self.stop)
        # start cube button signal
        QtCore.QObject.connect(self.ui.pButton_Cube,
                               QtCore.SIGNAL('clicked()'), self.startCube)

        # start reset button signal
        QtCore.QObject.connect(self.ui.pButton_Reset,
                               QtCore.SIGNAL('clicked()'), self.resetData)

        # timer signal
        QtCore.QObject.connect(self.timer,
                               QtCore.SIGNAL('timeout()'), self.updatePlot)
        QtCore.QObject.connect(self.timerActivity,
                               QtCore.SIGNAL('timeout()'), self.updateActivity)

        # Configure UI
        # cBoxs
        self.ui.cBox_Port.addItems(self.getPorts())
        self.ui.cBox_Speed.addItems(["9600", "57600", "115200"])
        self.ui.cBox_Speed.setCurrentIndex(2)
        self.setUILocked(False)

        self.ui.cBox_IMU.addItems(['MPU-9150', 'SP_RAZOR'])

        # Configure plots
        self.configurePlot(self.ui.plt1, RANGE_ACCEL, "Acceleration", "g")
        self.configurePlot(self.ui.plt2, RANGE_GYRO, "Angular Velocity",
                           "deg/seg")
        self.configurePlot(self.ui.plt3, RANGE_MAG, "Flux", "Gs")
        self.configurePlot(self.ui.plt4, RANGE_EULER, "Euler angles DMP",
                           "degree")
        self.configurePlot(self.ui.plt5, RANGE_EULER, "Euler angles", "degree")
        self.configurePlot(self.ui.plt6, RANGE_ACCEL, "Linear Acceleration",
                           "g")

    ## Executed when pressing Start Buttton
    #
    # Starts data adquisition and timers, blocking the UI elements
    # @param self The object pointer.
    def start(self):
        ## Reference for the Threaded serial adquisition
        #
        # Threaded adquisition for a serial device with interrupts
        # using Qt4 signals
        self.data = SerialThread(str(self.ui.cBox_IMU.currentText()))
        self.data.openPort(str(self.ui.cBox_Port.currentText()),
                           int(self.ui.cBox_Speed.currentText()))
        ## Register the data object with the cube
        self.cube = Cube(self.data)

        # start file
        if self.ui.chBox_export.isChecked():
            ## export data
            self.csv = CSVExport()
            self.ui.statusbar.showMessage("Exporting data")
        else:
            self.ui.statusbar.showMessage("Adquiring data")

        # start data thread
        self.data.start()
        # dataThread new data signal
        self.connect(self.data, QtCore.SIGNAL('newData()'),
                     self.updateData)
        # update UI
        self.setUILocked(True)
        # start timer for updating plot
        self.timer.start(20)
        # start timer every second for activity
        self.timerActivity.start(1000)

        ## Reference for the activity detection algorithm
        #
        # Activity detection algorithm propossed by Dr. Pablo Reyes
        self.activity = ActivityDetection(70, 175, 20, .02)

        ## Reference for the fall detection algorithm
        #
        # Fall detection algorithm propossed by Dr. Pablo Reyes
        self.fall = FallDetection(.02, 2.8, .65)
        #~ self.fall = FallDetection(.02, 2.0, .65)

        ## Reference for
        self.posture = Posture()

    ## Executed every time new data is adquired
    #
    # Executed by @ref serialThread_MPU9150 with QT4 Signal
    # @param self The object pointer.
    def updateData(self):
        tmp = []
        tmp = self.data.getAcceleration()
        self.AX.pop(0)
        self.AY.pop(0)
        self.AZ.pop(0)
        self.AX.append(tmp[0])
        self.AY.append(tmp[1])
        self.AZ.append(tmp[2])

        tmp = self.data.getGyroscope()
        self.GX.pop(0)
        self.GY.pop(0)
        self.GZ.pop(0)
        self.GX.append(tmp[0])
        self.GY.append(tmp[1])
        self.GZ.append(tmp[2])

        tmp = self.data.getMagnetometer()
        self.MX.pop(0)
        self.MY.pop(0)
        self.MZ.pop(0)
        self.MX.append(tmp[0])
        self.MY.append(tmp[1])
        self.MZ.append(tmp[2])

        tmp = self.data.getEulerDMP()
        self.Y.pop(0)
        self.P.pop(0)
        self.R.pop(0)
        self.Y.append(tmp[0])
        self.P.append(tmp[1])
        self.R.append(tmp[2])

        tmp = self.data.getEuler()
        self.Y2.pop(0)
        self.P2.pop(0)
        self.R2.pop(0)
        self.Y2.append(tmp[0])
        self.P2.append(tmp[1])
        self.R2.append(tmp[2])

        tmp = self.data.getLinearAccel()
        self.LAX.pop(0)
        self.LAY.pop(0)
        self.LAZ.pop(0)
        self.LAX.append(tmp[0])
        self.LAY.append(tmp[1])
        self.LAZ.append(tmp[2])

        # detection algorithms
        # falls
        #~ self.fall.updateFall(self.AX[self.POS], self.AY[self.POS],
                             #~ self.AZ[self.POS], self.Y[self.POS],
                             #~ self.P[self.POS], self.R[self.POS])
        # include posture offset update every second
        # posture offset calibration
        #~ if self.POS < 10:
            #~ self.posture.offset(self.AX[self.POS], self.AY[self.POS],
                                #~ self.AZ[self.POS])
        # get tilt data
        #~ [ang_front, ang_lat] = self.posture.getTilt(self.AX[self.POS],
                                                    #~ self.AY[self.POS],
                                                    #~ self.AZ[self.POS])
        #~ log.v('Tilt : ['+str(ang_front)+', '+str(ang_lat)+']')

        # write data to CSV if its enabled
        if self.ui.chBox_export.isChecked():
            self.csv([self.AX[WINDOW], self.AY[WINDOW], self.AZ[WINDOW]])

    def updateActivity(self):
        # detection algorithms
        # activity
        #~ if self.POS > 50:
            #~ self.activity.updateActivity(self.LAX[self.POS-50:self.POS],
                                         #~ self.LAY[self.POS-50:self.POS],
                                         #~ self.LAZ[self.POS-50:self.POS])
            #~ log.i('Energy consumption per second ' +
                  #~ str(self.activity.getEnergyConsumption()/1000)+' Kcal')
        print ""

    ## Executed every 20 ms for updating plot
    #
    # Executed by QtTimer every 20 ms after pressed start button.
    # Stops and reset timer when stop button is pressed.
    # @param self The object pointers
    def updatePlot(self):
        # plot acceleration
        self.ui.plt1.clear()
        self.ui.plt1.plot(self.AX[:UPDATE_SIZE], pen='r')
        self.ui.plt1.plot(self.AY[:UPDATE_SIZE], pen='g')
        self.ui.plt1.plot(self.AZ[:UPDATE_SIZE], pen='b')

        # plot gyroscope
        self.ui.plt2.clear()
        self.ui.plt2.plot(self.GX[:UPDATE_SIZE], pen='r')
        self.ui.plt2.plot(self.GY[:UPDATE_SIZE], pen='g')
        self.ui.plt2.plot(self.GZ[:UPDATE_SIZE], pen='b')

        # plot magnetometer
        self.ui.plt3.clear()
        self.ui.plt3.plot(self.MX[:UPDATE_SIZE], pen='r')
        self.ui.plt3.plot(self.MY[:UPDATE_SIZE], pen='g')
        self.ui.plt3.plot(self.MZ[:UPDATE_SIZE], pen='b')

        # plot euler
        self.ui.plt4.clear()
        self.ui.plt4.plot(self.Y[:UPDATE_SIZE], pen='r')
        self.ui.plt4.plot(self.P[:UPDATE_SIZE], pen='g')
        self.ui.plt4.plot(self.R[:UPDATE_SIZE], pen='b')

        # plot euler dmp
        self.ui.plt5.clear()
        self.ui.plt5.plot(self.Y2[:UPDATE_SIZE], pen='r')
        self.ui.plt5.plot(self.P2[:UPDATE_SIZE], pen='g')
        self.ui.plt5.plot(self.R2[:UPDATE_SIZE], pen='b')

        # plot linear acceleration
        self.ui.plt6.clear()
        self.ui.plt6.plot(self.LAX[:UPDATE_SIZE], pen='r')
        self.ui.plt6.plot(self.LAY[:UPDATE_SIZE], pen='g')
        self.ui.plt6.plot(self.LAZ[:UPDATE_SIZE], pen='b')

    ## Executed when Stop Button is pressed.
    #
    # Stops data threads, timers and unlocks UI.
    # @param self The object pointer.
    def stop(self):
        # stop threads
        self.data.closePort()
        self.timer.stop()
        self.timerActivity.stop()

        # update UI
        self.setUILocked(False)

    ## Axis configuration of a PyQtGraph plot
    #
    # Stops data threads, timers and unlocks UI.
    # @param self The object pointer.
    # @param plot The reference to the plot to be configured
    # @param Range The range (+/-) for the Y axis of the plot
    # @param title The title of the plot
    # @param unit The measurement unit for the plot (auto-scaled)
    def configurePlot(self, plot, Range, title, unit):
        plot.setXRange(0, WINDOW)
        plot.setYRange(-Range, Range)
        plot.showGrid(x=False, y=True)
        plot.showAxis('bottom', False)
        plot.setMouseEnabled(x=False, y=False)
        plot.setLabel('left', title, unit)

    ## Set the lock status of the UI elements
    #
    # Enables or disables UI elements of the window.
    # Executed during adquisition, blocks UI elements to only enable
    # the Stop button and disable configuration UI elements.
    #
    # + if @c bool_ = @b TRUE: allows configuration of the adquisition
    # + if @c bool_ = @b FALSE: disables configuratin of the adquisition
    # @param self The object pointer.
    # @param bool_ The status of the UI
    def setUILocked(self, bool_):
        self.ui.pButton_Stop.setEnabled(bool_)
        self.ui.pButton_Cube.setEnabled(bool_)
        self.ui.pButton_Start.setEnabled(not bool_)
        self.ui.cBox_Port.setEnabled(not bool_)
        self.ui.cBox_Speed.setEnabled(not bool_)
        self.ui.cBox_IMU.setEnabled(not bool_)
        self.ui.chBox_export.setEnabled(not bool_)

    ## Gets avaliable serial ports on the system
    #
    # Search trough all avaliable serial ports (virtuals included) and
    # lists only those who have a connection avaliable.
    # @param self The object pointer.
    # @retval portList list with the serial ports routes
    def getPorts(self):
        portList = []
        for ports in list_ports.comports():
            if ports[2] != "n/a":
                portList.append(ports[0])
        self.ui.statusbar.showMessage("Detected "+str(len(portList)) +
                                      " serial ports")
        return portList

    ## Clear data buffers for plotting
    #
    # Fill with zeroes all data buffers used for plotting and position
    # the data.
    #
    # Size of the buffers can be changed by the class variable WINDOW
    # @param self The object pointer.
    def resetData(self):
        ## Buffer for Acceleration in X axis
        #
        # Acceleration in g (gravity)
        self.AX = [0.0]*WINDOW
        ## Buffer for Acceleration in Y axis
        #
        # Acceleration in g (gravity)
        self.AY = [0.0]*WINDOW
        ## Buffer for Acceleration in Z axis
        #
        # Acceleration in g (gravity)
        self.AZ = [0.0]*WINDOW
        ## Buffer for Angular Velocity in X axis
        #
        # Angular Velocity in degrees/second
        self.GX = [0.0]*WINDOW
        ## Buffer for Angular Velocity in Y axis
        #
        # Angular Velocity in degrees/second
        self.GY = [0.0]*WINDOW
        ## Buffer for Angular Velocity in Z axis
        #
        # Angular Velocity in degrees/second
        self.GZ = [0.0]*WINDOW
        ## Buffer for Magnetic field in X axis
        #
        # Magnetic field flux in Gauss (Gs)
        self.MX = [0.0]*WINDOW
        ## Buffer for Magnetic field in Y axis
        #
        # Magnetic field flux in Gauss (Gs)
        self.MY = [0.0]*WINDOW
        ## Buffer for Magnetic field in Z axis
        #
        # Magnetic field flux in Gauss (Gs)
        self.MZ = [0.0]*WINDOW
        ## Buffer for Euler angles in X axis (Yaw)
        #
        # Angles in degrees. Obtained directicly from the DMP of the
        # MPU-9150 internal sensor fusion with 6DOF (Accelerometer +
        # Gyroscope).
        self.Y = [0.0]*WINDOW
        ## Buffer for Euler angles in Y axis (Pitch)
        #
        # Angles in degrees. Obtained directicly from the DMP of the
        # MPU-9150 internal sensor fusion with 6DOF (Accelerometer +
        # Gyroscope).
        self.P = [0.0]*WINDOW
        ## Buffer for Euler angles in Z axis (Roll)
        #
        # Angles in degrees. Obtained directicly from the DMP of the
        # MPU-9150 internal sensor fusion with 6DOF (Accelerometer +
        # Gyroscope).
        self.R = [0.0]*WINDOW
        ## Buffer for Euler angles in X axis (Yaw)
        #
        # Angles in degrees. Obtained from the sensor fusion algorithm
        # (9DOF) developed by Sebastian Madgwick and implemented by
        # Fabio Varesano.
        self.Y2 = [0.0]*WINDOW
        ## Buffer for Euler angles in Y axis (Pitch)
        #
        # Angles in degrees. Obtained from the sensor fusion algorithm
        # (9DOF) developed by Sebastian Madgwick and implemented by
        # Fabio Varesano.
        self.P2 = [0.0]*WINDOW
        ## Buffer for Euler angles in Z axis (Roll)
        #
        # Angles in degrees. Obtained from the sensor fusion algorithm
        # (9DOF) developed by Sebastian Madgwick and implemented by
        # Fabio Varesano.
        self.R2 = [0.0]*WINDOW
        ## Buffer for Linear Acceleration in X axis
        #
        # Acceleration in g (gravity). The 9DOF sensor fusion algorithm
        # allows to estimate the expected gravity coordinates and
        # dinamically delete it from the measured acceleration, allowing
        # the gravity compensated linear acceleration
        self.LAX = [0.0]*WINDOW
        ## Buffer for Linear Acceleration in Y axis
        #
        # Acceleration in g (gravity). The 9DOF sensor fusion algorithm
        # allows to estimate the expected gravity coordinates and
        # dinamically delete it from the measured acceleration, allowing
        # the gravity compensated linear acceleration
        self.LAY = [0.0]*WINDOW
        ## Buffer for Linear Acceleration in Z axis
        #
        # Acceleration in g (gravity). The 9DOF sensor fusion algorithm
        # allows to estimate the expected gravity coordinates and
        # dinamically delete it from the measured acceleration, allowing
        # the gravity compensated linear acceleration
        self.LAZ = [0.0]*WINDOW
        ## Indicates the current index for storing data in the buffers
        #
        # Updated and reseted by @ref updateData limits its count to
        # @ref WINDOW variable
        self.POS = 0

    def startCube(self):
        self.cube.start()

# start app
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
