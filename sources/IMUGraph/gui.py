# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Thu Mar 27 09:19:38 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(625, 520)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cBox_Speed = QtGui.QComboBox(self.centralwidget)
        self.cBox_Speed.setObjectName(_fromUtf8("cBox_Speed"))
        self.gridLayout.addWidget(self.cBox_Speed, 3, 2, 1, 1)
        self.pButton_Stop = QtGui.QPushButton(self.centralwidget)
        self.pButton_Stop.setObjectName(_fromUtf8("pButton_Stop"))
        self.gridLayout.addWidget(self.pButton_Stop, 5, 2, 1, 1)
        self.cBox_Port = QtGui.QComboBox(self.centralwidget)
        self.cBox_Port.setObjectName(_fromUtf8("cBox_Port"))
        self.gridLayout.addWidget(self.cBox_Port, 3, 0, 1, 1)
        self.plt1 = PlotWidget(self.centralwidget)
        self.plt1.setObjectName(_fromUtf8("plt1"))
        self.gridLayout.addWidget(self.plt1, 0, 0, 1, 1)
        self.plt5 = PlotWidget(self.centralwidget)
        self.plt5.setObjectName(_fromUtf8("plt5"))
        self.gridLayout.addWidget(self.plt5, 1, 2, 1, 1)
        self.plt4 = PlotWidget(self.centralwidget)
        self.plt4.setObjectName(_fromUtf8("plt4"))
        self.gridLayout.addWidget(self.plt4, 0, 2, 1, 1)
        self.plt2 = PlotWidget(self.centralwidget)
        self.plt2.setObjectName(_fromUtf8("plt2"))
        self.gridLayout.addWidget(self.plt2, 1, 0, 1, 1)
        self.pButton_Start = QtGui.QPushButton(self.centralwidget)
        self.pButton_Start.setMinimumSize(QtCore.QSize(0, 0))
        self.pButton_Start.setObjectName(_fromUtf8("pButton_Start"))
        self.gridLayout.addWidget(self.pButton_Start, 5, 0, 1, 1)
        self.plt3 = PlotWidget(self.centralwidget)
        self.plt3.setObjectName(_fromUtf8("plt3"))
        self.gridLayout.addWidget(self.plt3, 2, 0, 1, 1)
        self.plt6 = PlotWidget(self.centralwidget)
        self.plt6.setObjectName(_fromUtf8("plt6"))
        self.gridLayout.addWidget(self.plt6, 2, 2, 1, 1)
        self.pButton_Cube = QtGui.QPushButton(self.centralwidget)
        self.pButton_Cube.setObjectName(_fromUtf8("pButton_Cube"))
        self.gridLayout.addWidget(self.pButton_Cube, 7, 0, 1, 1)
        self.chBox_export = QtGui.QCheckBox(self.centralwidget)
        self.chBox_export.setObjectName(_fromUtf8("chBox_export"))
        self.gridLayout.addWidget(self.chBox_export, 7, 2, 1, 1)
        self.cBox_IMU = QtGui.QComboBox(self.centralwidget)
        self.cBox_IMU.setObjectName(_fromUtf8("cBox_IMU"))
        self.gridLayout.addWidget(self.cBox_IMU, 4, 0, 1, 1)
        self.pButton_Reset = QtGui.QPushButton(self.centralwidget)
        self.pButton_Reset.setObjectName(_fromUtf8("pButton_Reset"))
        self.gridLayout.addWidget(self.pButton_Reset, 4, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 625, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.actionLinear_Acceleration = QtGui.QAction(MainWindow)
        self.actionLinear_Acceleration.setCheckable(True)
        self.actionLinear_Acceleration.setObjectName(_fromUtf8("actionLinear_Acceleration"))
        self.actionEuler_Rotation = QtGui.QAction(MainWindow)
        self.actionEuler_Rotation.setCheckable(True)
        self.actionEuler_Rotation.setObjectName(_fromUtf8("actionEuler_Rotation"))
        self.actionLinear_Acceleration_2 = QtGui.QAction(MainWindow)
        self.actionLinear_Acceleration_2.setCheckable(True)
        self.actionLinear_Acceleration_2.setObjectName(_fromUtf8("actionLinear_Acceleration_2"))
        self.actionG_force = QtGui.QAction(MainWindow)
        self.actionG_force.setCheckable(True)
        self.actionG_force.setChecked(True)
        self.actionG_force.setObjectName(_fromUtf8("actionG_force"))
        self.actionMeters_seg_2 = QtGui.QAction(MainWindow)
        self.actionMeters_seg_2.setCheckable(True)
        self.actionMeters_seg_2.setObjectName(_fromUtf8("actionMeters_seg_2"))
        self.actionRad_seg = QtGui.QAction(MainWindow)
        self.actionRad_seg.setCheckable(True)
        self.actionRad_seg.setChecked(True)
        self.actionRad_seg.setObjectName(_fromUtf8("actionRad_seg"))
        self.actionDeg_seg = QtGui.QAction(MainWindow)
        self.actionDeg_seg.setCheckable(True)
        self.actionDeg_seg.setObjectName(_fromUtf8("actionDeg_seg"))
        self.actionYawn_Pitch_Roll = QtGui.QAction(MainWindow)
        self.actionYawn_Pitch_Roll.setCheckable(True)
        self.actionYawn_Pitch_Roll.setChecked(True)
        self.actionYawn_Pitch_Roll.setObjectName(_fromUtf8("actionYawn_Pitch_Roll"))
        self.actionEuler_Angles = QtGui.QAction(MainWindow)
        self.actionEuler_Angles.setCheckable(True)
        self.actionEuler_Angles.setObjectName(_fromUtf8("actionEuler_Angles"))
        self.actionScan_Serial_ports = QtGui.QAction(MainWindow)
        self.actionScan_Serial_ports.setObjectName(_fromUtf8("actionScan_Serial_ports"))
        self.menuFile.addAction(self.actionScan_Serial_ports)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "FONDEF MPU-9010 Testing", None))
        self.pButton_Stop.setText(_translate("MainWindow", "Stop", None))
        self.pButton_Start.setText(_translate("MainWindow", "Start", None))
        self.pButton_Cube.setText(_translate("MainWindow", "Start Cube", None))
        self.chBox_export.setText(_translate("MainWindow", "Export to CSV", None))
        self.pButton_Reset.setText(_translate("MainWindow", "Reset Plots", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionLinear_Acceleration.setText(_translate("MainWindow", "Linear Acceleration", None))
        self.actionEuler_Rotation.setText(_translate("MainWindow", "Euler Rotation", None))
        self.actionLinear_Acceleration_2.setText(_translate("MainWindow", "Linear Acceleration", None))
        self.actionG_force.setText(_translate("MainWindow", "G force", None))
        self.actionMeters_seg_2.setText(_translate("MainWindow", "meters/seg^2", None))
        self.actionRad_seg.setText(_translate("MainWindow", "Rad/seg", None))
        self.actionDeg_seg.setText(_translate("MainWindow", "Deg/seg", None))
        self.actionYawn_Pitch_Roll.setText(_translate("MainWindow", "Yawn Pitch Roll", None))
        self.actionEuler_Angles.setText(_translate("MainWindow", "Euler Angles", None))
        self.actionScan_Serial_ports.setText(_translate("MainWindow", "Scan Serial ports...", None))

from pyqtgraph import PlotWidget
