# Libs for filter design and apply
from numpy import trapz
from scipy.signal import butter, lfilter

# Set Debug
from log import Log
log = Log('ActivityDetection')
log.setVerbose(False)


## Estimates the energy consumption (Kcal) by second
#
# Using an accelerometer and aditional data from the user calculates:
# + Index of activity (IAA) in a second
# + Predicted consumed energy by activity (EE) in a second
# + Predicted consumed energy by basal metabolism (BMR) in a second
#
# @author Dr. Pablo Reyes
# @author Sebastian Sepulveda
# @todo Validate algorithms
class ActivityDetection:
    ## Default value for BMR
    #
    # Default BMR calculated at 2060 Kcal (normal person) divided
    # in the seconds of one day (86400 seconds)
    BMR = .023842593
    ## Predicted consumed energy by activity (EE) in a second
    #
    # Initalized at 0
    EE = 0
    fs = .02

    ## Constructor for Activity Detection
    #
    # Initializes calculations for the user to determinate the BMR
    # @param self The object pointer
    # @param kg Weight of the user, in Kg
    # @param cm Height of the user, in cm
    # @param years Years of the user
    # @param fs Time between samples, in seconds
    def __init__(self, kg=70, cm=170, years=20, fs=.02):
        # basal metabolism per day
        #~ BMR=88.362+(13.397*kg)+(4.799*cm)-(5.677*years)
        BMR = (88.362+(13.397*kg)+(4.799*cm)-(5.677*years))*1000
        log.v('BMR: '+str(BMR))
        # calcule per second
        self.BMR = BMR/86400
        self.fs = fs
        log.v('BMR/s: '+str(self.BMR))

        # design butter lowpass Fp=6.45 Fs=12.35 13th order
        [self.b, self.a] = butter(13, [6.45, 12.35], 'low')

    ## Take the absolute value of a list
    #
    # In Python, the @c abs function can't return the absolute values
    # from a list. This function is a workaround to this limitation.
    # @param self The object pointer
    # @param _list The original list to take the absolutes values
    # @return The absolute values in the original list
    def abs_list(self, _list):
        size = len(_list)-1

        for i in range(0, size):
            _list[i] = abs(_list[i])
        return _list

    ## Update activity detection algorithm with last second data.
    #
    # The function updates the IAA based on the provided accelerations
    # and calculates the energy consuptiom (EE). Updates the data for
    # the algoritm
    # @param self The object pointer
    # @param x list with the last second acceleration data in the X axis
    # @param y list with the last second acceleration data in the Y axis
    # @param z list with the last second acceleration data in the Z axis
    # @todo verify normalization of the IAA
    def updateActivity(self, x, y, z):
        # butter lowpass Fp=6.45 Fs=12.35 13th order
        x = lfilter(self.b, self.a, x)
        y = lfilter(self.b, self.a, y)
        z = lfilter(self.b, self.a, z)

        # integrate absolute accels and add
        IAA = (trapz(self.abs_list(x), dx=self.fs) +
               trapz(self.abs_list(y), dx=self.fs) +
               trapz(self.abs_list(z), dx=self.fs))
        log.v('IAA: '+str(IAA))

        # prediction of consumption of energy in the second
        self.EE = .104+.023*IAA
        log.v('EE: '+str(self.EE))
        log.v('EE_total: '+str(self.EE+self.BMR))

    ## Getter for the last second energy consuption
    #
    # Gets the last energy consumption result from the last
    # @ref updateActivity call
    # @param self The object pointer
    # @return Last second energy consumption, in Calories
    def getEnergyConsumption(self):
        return self.EE+self.BMR

    ## Getter for the EE value
    #
    # Gets the last EE result from the last # @ref updateActivity call
    # @param self The object pointer
    # @return Last second EE
    def getEE(self):
        return self.EE

    ## Getter for the BMR value
    #
    # Gets the calculated BMR for the user
    # @param self The object pointer
    # @return Value of the BMR (per day)
    def getBMR(self):
        return self.BMR
