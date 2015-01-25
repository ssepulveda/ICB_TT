# Set debug
from log import Log
log = Log('IMU')


## IMU values for scales and data structure in the CSV data received
#
# Receives a IMU device name and returns data for scaling each type of data and
# the correct placement in the CSV format.
#
# Also fixes inverted and swaped axis.
class IMU:
    ## Constructor
    #
    # Creates a @ref self.SCALE_VECTOR for scaling the data based on the IMU
    # devices and the arregement on the CSV format.
    # @param self The object pointer
    # @param name IMU decive used for sending data
    def __init__(self, name='MPU-9150'):
        self.name = name
        log.d('Selected '+name+' IMU device')

        if name == 'MPU-9150':
            self.ACCEL = 0.000061035   # Gravity set at +-2g
            self.GYRO = 0.061035156    # deg/seg fullrange
            self.MAG_T = 0.000000293   # +- 1200 uT @ 13 bits
            self.MAG_GS = 0.001464844  # +- 12 Gs @ 13 bits
            self.EULER = 1             # Euler data comes in degrees
            # fixes for inverted axis
            self.SCALE_VECTOR = ([self.EULER]*3 +
                                 [self.ACCEL, -self.ACCEL, self.ACCEL] +
                                 [self.GYRO]*3 +
                                 [self.MAG_GS, self.MAG_GS, -self.MAG_GS])
            # fixes for swaped axis
            self.ACCEL_RANGE = [3, 4, 5]
            self.GYRO_RANGE = [6, 7, 8]
            self.MAG_RANGE = [10, 9, 11]
            self.EULER_RANGE = [0, 1, 2]

        elif name == 'SP_RAZOR':
            self.ACCEL = 0.00390625     # +- 2 g @ 10 bits
            self.GYRO = 0.061035156     # +- 2000 deg/seg @ 16 bits
            self.MAG_GS = 0.00390625    # +-8 Gs @ 12 bitss
            self.EULER = 1
            self.SCALE_VECTOR = ([self.ACCEL, -self.ACCEL, self.ACCEL] +
                                 [self.GYRO]*3 +
                                 [self.MAG_GS]*3)
            self.ACCEL_RANGE = [0, 1, 2]
            self.GYRO_RANGE = [3, 4, 5]
            self.MAG_RANGE = [6, 7, 8]
            self.EULER_RANGE = [-1, -1, -1]

        else:
            log.e('Selected '+name+' IMU device not found !')

    def getScaleVector(self):
        return self.SCALE_VECTOR

    def getRangeAccelerometer(self):
        return self.ACCEL_RANGE

    def getRangeGyroscope(self):
        return self.GYRO_RANGE

    def getRangeMagnetometer(self):
        return self.MAG_RANGE

    def getRangeEuler(self):
        return self.EULER_RANGE
