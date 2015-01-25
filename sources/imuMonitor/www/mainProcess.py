#!/usr/bin/env python
from multiprocessing import Process, Event
import sys
import getopt
import os.path
import time
import math
sys.path.append('.')
import RTIMU

from pca9547 import PCA9547
from csvExport import CSVExport


SETTINGS_FILE_0 = "RTIMU0"
SETTINGS_FILE_1 = "RTIMU1"
SETTINGS_FILE_2 = "RTIMU2"
SETTINGS_FILE_3 = "RTIMU3"
SETTINGS_FILE_4 = "RTIMU4"
SETTINGS_FILE_5 = "RTIMU5"

## Thread for adquiring data from IMUs
#
# @param Process the process object
class MainProcess(Process):
	## Constructor
	#
	# Inits the process, the CSV file, the PCA9547 Multiplexor, the settings
	# file for each sensor (with calibration)
	# @param self The object pointer
    def __init__(self):
        Process.__init__(self)
        self.exit = Event()

        self.csv = CSVExport()
        self.i2cMux = PCA9547()

        self.settings0 = RTIMU.Settings(SETTINGS_FILE_0)
        self.settings1 = RTIMU.Settings(SETTINGS_FILE_1)
        self.settings2 = RTIMU.Settings(SETTINGS_FILE_2)
        self.settings3 = RTIMU.Settings(SETTINGS_FILE_3)
        self.settings4 = RTIMU.Settings(SETTINGS_FILE_4)
        self.settings5 = RTIMU.Settings(SETTINGS_FILE_5)

        self.imu0 = RTIMU.RTIMU(self.settings0)
        self.imu1 = RTIMU.RTIMU(self.settings1)
        self.imu2 = RTIMU.RTIMU(self.settings2)
        self.imu3 = RTIMU.RTIMU(self.settings3)
        self.imu4 = RTIMU.RTIMU(self.settings4)
        self.imu5 = RTIMU.RTIMU(self.settings5)

        self.settings = [self.settings0, self.settings1, self.settings2, self.settings3, self.settings4, self.settings5]
        self.imus = [self.imu0, self.imu1, self.imu2, self.imu3, self.imu4, self.imu5]

        self.detectedIMU = [False] * 6
        self.detectImu()

        self.pollInterval = 2

	## Detectes the number of IMUs avaliable in each channel
	#
	# @param self The object pointer
	# @return number of detected IMUs
    def detectImu(self):
        try:
            for n, imu in enumerate(self.imus):
                self.i2cMux.setChannel(n)
                if imu.IMUInit():
                    self.detectedIMU[n] = True
                else:
                    self.detectedIMU[n] = False
        except:
            print("Error in detection")
        return self.detectedIMU


    def setPollInterval(self, pollInterval):
        self.pollInterval = pollInterval

	## Sets file name for the CSV file
	#
	# @param self The object pointer
	# @param txt file name
    def setFileName(self, txt):
        self.csv.setTitle(txt)

	## gets the current data from the current sensor
	#
	# @param self The object pointer
	# @return all sensor data as a vector
    def getData(self):
        return self.allData

	## stops the thread and signals to exit
	#
	# @param self The object pointer
    def stop(self):
        self.exit.set()

    def saveSettings(self):
        try:
            for s in self.setting:
                s.save()
        except:
            print("Error in detection")
        return self.detectedIMU

	## Thread loop
	#
	# Get data in the polling interval definid time, and stores
	# data form all the avaliable sensor with his identificator and timestamp
	# @param self The object pointer
	# @return finalized job
    def run(self):
        self.csv.createFile()
        init_time = time.time()
        while not self.exit.is_set():
            try:
                for n, imu in enumerate(self.imus):
                    if self.detectedIMU[n]:
                        self.i2cMux.setChannel(n)
                        if imu.IMURead():
                            data0 = imu.getIMUData()
                            quaternion = data0["fusionQPose"]
                            acceleration = data0["accel"]
                            gyro = data0["gyro"]
                            compass = data0["compass"]

                            nowTime = time.time() - init_time

                            self.allData = [n] + \
                                      [nowTime] + \
                                      [acceleration[0]] + \
                                      [acceleration[1]] + \
                                      [acceleration[2]] + \
                                      [gyro[0]] + \
                                      [gyro[1]] + \
                                      [gyro[2]] + \
                                      [compass[0]] + \
                                      [compass[1]] + \
                                      [compass[2]] + \
                                      [quaternion[0]] + \
                                      [quaternion[1]] + \
                                      [quaternion[2]] + \
                                      [quaternion[3]]

                            self.csv.csvWrite(self.allData)
                            #print(self.allData)
                            time.sleep(self.pollInterval * 1.0/1000.0)
            except (KeyboardInterrupt, SystemExit):
                print("Finishing Thread bad")
                self.exit.set()
        print("Finished Adquisition")
        return
        

if __name__ == "__main__":
    app = MainProcess()
    app.start()
    app.join()
    sys.exit()
