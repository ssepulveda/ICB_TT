# Math Libs: integratin, sqrt
from numpy import trapz
from math import sqrt

# Set Debug
from log import Log
log = Log('FallDetection')
log.setVerbose(False)


## Detects fall from the accelerometer data
#
# Using an accelerometer calculates:
# + Impact normalized force (SV) and impact ranges (UFT, LFT)
# + Detectes a range of time during the detected impact (tm, ti)
# + Determinates the speed of the fall during the fallind time (V0)
# + Detect the posture (change in orientation) respect the initial
# impact posture.
# With all these data and determinations is possible to estimate with
# presition a fall and impact.
#
# @author Dr. Pablo Reyes
# @author Sebastian Sepulveda
# @todo Validate algorithms
class FallDetection:
    ## Buffer size for SV
    #
    # Determinate the buffer size for storing the SV data
    SIZE = 1024
    ## Upper force trigger
    #
    # Upper force trigger for detecting an impact, in g (gravities)
    UFT = 2.8
    ## Lower force trigger
    #
    # Lower force trigger for detecting the start of the impact, in
    # g (gravities)
    LFT = 0.65
    ## Time between samples
    #
    # Time between samples, in seconds
    fs = .02
    ## List for SV values
    #
    # Stores the last SV values
    SV = [0.0]*SIZE
    ## List for angles monitoring posture
    YAW = [.0]*SIZE
    PITCH = [.0]*SIZE
    ROLL = [.0]*SIZE
    ## Indicates for the buffers index
    POSITION = 0
    ## Indicates if a fall was detected
    #
    # + if @b TRUE: a fall was detected
    # + if @b FALL: a fall wasn't detected
    DROP = False
    SEMIDROP = False

    ## Constructor for the Fall Detection algorithm
    #
    # Initializes the values of fs, UFT and LFT allowing to change the
    # default values of the algorithms
    # @param self The object pointer
    # @param fs Time between samples, in seconds
    # @param UFT UFT trigger, in g (gravities)
    # @param LFT LFT trigger, in g (gravities)
    def __init__(self, fs=.02, UFT=2.8, LFT=.65):
        self.UFT = UFT
        self.LFT = LFT
        self.fs = fs

    ## Calculates de normal vector of three vectors
    #
    # Uses the math library from Python
    # @param self The objetc pointer
    # @param x 1st value to normalize
    # @param y 2nd value to normalize
    # @param z 3rd value to normalize
    # @return Normalized value of x,y and z
    def normalVector(self, x, y, z):
        return sqrt(x*x+y*y+z*z)

    ## Finds the first lower value on a list
    #
    # Finds the first lower value of LFT on a list
    # @param self The objetc pointer
    # @param value The value to find in the list
    # @param vector The list to find on
    # @return The index where the value (or 1st lower) was found
    def search1LFT(self, value, vector):
        _range = range(0, len(vector))
        for i in reversed(_range):
            if vector[i] <= value:
                return i
        return 0

    ## Finds the first upper value on a list
    #
    # Finds the first upper value of LFT on a list
    # @param self The objetc pointer
    # @param value The value to find in the list
    # @param vector The list to find on
    # @return The index where the value (or 1st upper) was found
    def search2LFT(self, value, vector):
        _range = range(0, len(vector))
        for i in reversed(_range):
            if vector[i] >= value:
                return i
        return 0

    ## Updates the Fall Detection algorithm with the last data.
    #
    # The function searches for a SV in between the impact range,
    # a fall speed between the time corresponding the impact and the
    # posture when a fall is detected.
    #
    # @param self The objetc pointer
    # @param x acceleration in X axis, in g (gravities)
    # @param y acceleration in Y axis, in g (gravities)
    # @param z acceleration in Z axis, in g (gravities)
    #
    # @note The algorithm proposed sugest to filter the adquired data
    # with a lowpass 1st order butterworth at 100 Hz. The data adquired
    # from the MPU-9150 (or even ADXL-345) digital accelerometers can
    # (and is) configured to filter the data and outputs filtered raw
    # data. Therefore, this filter is not implemented.
    # @note The algorithm has been implemented asumming a sensor fusion running
    # continusly for obtaining yaw, pitch, roll. The class stores the data
    # in a buffer for look back at the posture.
    def updateFall(self, x, y, z, yaw, pitch, roll):
        # calculate impact
        self.SV[self.POSITION] = self.normalVector(x, y, z)
        # Posture buffers
        self.YAW[self.POSITION] = yaw
        self.PITCH[self.POSITION] = pitch
        self.ROLL[self.POSITION] = roll

        # search last self.LFT
        if self.SV[self.POSITION] >= self.UFT:
            tf = self.POSITION*self.fs
            log.v('UFT found, finding 1st LFT')
            size = self.search1LFT(self.LFT, self.SV[:self.POSITION])-1
            tm = size*self.fs

            if (tf-tm) <= .350:
                size2 = self.search2LFT(self.LFT, self.SV[:size])-1
                ti = size2*self.fs
                log.v('2nd LFT found')

                if (tf-ti) <= .600:
                    # falling candidate
                    v0 = trapz(self.SV[size2:self.POSITION], dx=self.fs)
                    log.v('Fall candidate with speed: '+str(v0))

                    if v0 <= .7:
                        log.v('Fall detected, checking posture')
                        log.d('Pre-Fall, no posture change detected')
                        self.SEMIDROP = True
                        # check posture
                        if self.YAW[size]+60 < self.YAW[size2]:
                            log.v('*** REAL FALL DETECTED ! (yaw)')
                            log.d('Fall detected: yaw')
                            self.DROP = True
                        elif self.PITCH[size]+60 < self.PITCH[size2]:
                            log.v('*** REAL FALL DETECTED ! (pitch)')
                            log.d('Fall detected: pitch')
                            self.DROP = True
                        elif self.ROLL[size]+60 < self.ROLL[size2]:
                            log.v('*** REAL FALL DETECTED ! (roll)')
                            log.d('Fall detected: roll')
                            self.DROP = True
                        else:
                            self.DROP = False
                            self.SEMIDROP = False
                    else:
                        self.DROP = False
                        self.SEMIDROP = False
                else:
                    self.DROP = False
                    self.SEMIDROP = False
            else:
                self.DROP = False
                self.SEMIDROP = False
        else:
            self.DROP = False
            self.SEMIDROP = False

        if self.POSITION < self.SIZE-1:
            self.POSITION += 1
        else:
            self.POSITION = 0

    ## Getter for the fall status obtained from the last update
    #
    # Return the result of the Fall Detection algorithm from the last
    # @ref updateFall call.
    # @return Status of the fall
    # + @b TRUE : if a fall was detected
    # + @b FALSE : if a fall wasn't detected
    def getFallStatus(self):
        return self.DROP

    ## Getter for the semi fall status obtained from the last update
    #
    # Return the result of the Fall Detection algorithm from the last
    # @ref updateFall call before checking the posture
    # @return Status of the semi fall
    # + @b TRUE : if a semi fall was detected
    # + @b FALSE : if a semi fall wasn't detected
    def getSemiFallStatus(self):
        return self.SEMIDROP
