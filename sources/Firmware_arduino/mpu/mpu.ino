////////////////////////////////////////////////////////////////////////////
//
//  This file is part of MPU9150Lib
//
//  Copyright (c) 2013 Pansenti, LLC
//

#include <Wire.h>
#include "I2Cdev.h"
#include "MPU9150Lib.h"
#include "CalLib.h"
#include <dmpKey.h>
#include <dmpmap.h>
#include <inv_mpu.h>
#include <inv_mpu_dmp_motion_driver.h>
#include <EEPROM.h>
#include "MPUVector3.h"

//  DEVICE_TO_USE selects whether the IMU at address 0x68

#define  DEVICE_TO_USE    0

MPU9150Lib MPU;

//  MPU_UPDATE_RATE defines the rate (in Hz) at which the MPU updates the sensor data and DMP output

#define MPU_UPDATE_RATE  (50)

//  MAG_UPDATE_RATE defines the rate (in Hz) at which the MPU updates the magnetometer data
//  MAG_UPDATE_RATE should be less than or equal to the MPU_UPDATE_RATE

#define MAG_UPDATE_RATE  (10)

//  MPU_MAG_MIX defines the influence that the magnetometer has on the yaw output.
//  The magnetometer itself is quite noisy so some mixing with the gyro yaw can help
//  significantly. Some example values are defined below:

#define  MPU_MAG_MIX_GYRO_ONLY          0                   // just use gyro yaw
#define  MPU_MAG_MIX_MAG_ONLY           1                   // just use magnetometer and no gyro yaw
#define  MPU_MAG_MIX_GYRO_AND_MAG       10                  // a good mix value 
#define  MPU_MAG_MIX_GYRO_AND_SOME_MAG  50                  // mainly gyros with a bit of mag correction 

//  MPU_LPF_RATE is the low pas filter rate and can be between 5 and 188Hz

#define MPU_LPF_RATE   40

//  SERIAL_PORT_SPEED defines the speed to use for the debug serial port

#define  SERIAL_PORT_SPEED  115200

void setup()
{
  Serial.begin(SERIAL_PORT_SPEED);
  Serial.print("Arduino9150 starting using device "); Serial.println(DEVICE_TO_USE);
  Wire.begin();
  MPU.selectDevice(DEVICE_TO_USE);                        // only really necessary if using device 1
  MPU.init(MPU_UPDATE_RATE, MPU_MAG_MIX_GYRO_AND_MAG, MAG_UPDATE_RATE, MPU_LPF_RATE);   // start the MPU
//  MPU.init(MPU_UPDATE_RATE, MPU_MAG_MIX_GYRO_ONLY, MAG_UPDATE_RATE, MPU_LPF_RATE);   // start the MPU
}

void loop()
{  
  MPU.selectDevice(DEVICE_TO_USE);                         // only needed if device has changed since init but good form anyway
  if (MPU.read()) {                                        // get the latest data if ready yet
    /*
    MPU.printQuaternion(MPU.m_rawQuaternion);              // print the raw quaternion from the dmp
    MPU.printVector(MPU.m_rawMag);                         // print the raw mag data
    MPU.printVector(MPU.m_rawAccel);                       // print the raw accel data
    MPU.printAngles(MPU.m_dmpEulerPose);                   // the Euler angles from the dmp quaternion
    MPU.printVector(MPU.m_calAccel);                       // print the calibrated accel data
    MPU.printVector(MPU.m_calMag);                         // print the calibrated mag data
    MPU.printAngles(MPU.m_fusedEulerPose);                 // print the output of the data fusion
    Serial.print(" Pressure: ");
    Serial.print(pressure, DEC);
    */  
    
    /*
    Serial.print(MPU.m_rawQuaternion[QUAT_W]);
    Serial.print(',');
    Serial.print(MPU.m_rawQuaternion[QUAT_X]);
    Serial.print(',');
    Serial.print(MPU.m_rawQuaternion[QUAT_Y]);
    Serial.print(',');
    */
    
    Serial.print(MPU.m_fusedEulerPose[VEC3_X] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU.m_fusedEulerPose[VEC3_Y] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU.m_fusedEulerPose[VEC3_Z] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU.m_calAccel[VEC3_X]);
    Serial.print(',');
    Serial.print(MPU.m_calAccel[VEC3_Y]);
    Serial.print(',');
    Serial.print(MPU.m_calAccel[VEC3_Z]);
    Serial.print(',');
  
    Serial.print(MPU.m_rawGyro[VEC3_X]);
    Serial.print(',');
    Serial.print(MPU.m_rawGyro[VEC3_Y]);
    Serial.print(',');
    Serial.print(MPU.m_rawGyro[VEC3_Z]);
    Serial.print(',');
  
    Serial.print(MPU.m_rawMag[VEC3_X]);
    Serial.print(',');
    Serial.print(MPU.m_rawMag[VEC3_Y]);
    Serial.print(',');
    Serial.print(MPU.m_rawMag[VEC3_Z]);
    Serial.println();
  }
}

