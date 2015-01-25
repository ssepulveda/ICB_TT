#!/usr/bin/env python
from time import strftime, gmtime
from datetime import datetime
import csv


## Export data in CSV format
#
# Export data using date and time as name for the file, avoiding overwriting
# data in differents adquisitions.
#
# It also registers in the first colummn the elapsed since the first
# adquisition
#
# @note The data is stored in a "data" folder (must be created first)
class CSVExport:
    ## Constructor
    #
    # Gets time to create the filename and instanciate the start of the
    # adquisition
    # @note The filename format is Year-Moth-Day_Hours-minutes-seconds.csv
    def __init__(self):
        self.name = strftime("data/%Y-%m-%d_%H-%M-%S.csv", gmtime())

    def createFile(self):
        FILE = open(self.name, "wb")
        self.CSV = csv.writer(FILE)
        self.CSV.writerow(["imu", "time", "acc X", "acc Y", "acc Z", "gyro X", "gyro Y", "gyro Z", "compass X", "compass Y", "compass Z", "Q1", "Q2", "Q3", "Q4"])

    def setTitle(self, txt):
        if txt is not "":
            self.name = "data/%s.csv" % txt

    def getTitle(self):
        return self.name

    ## Writes a new line of data
    #
    # @param self The object pointer
    # @param txt The data to export
    def csvWrite(self, txt):
        self.CSV.writerow(txt)
