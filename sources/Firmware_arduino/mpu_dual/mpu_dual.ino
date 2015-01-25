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

MPU9150Lib MPU0;
MPU9150Lib MPU1;

  int mpu0 = 0;
  int mpu1 = 0;

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
  Serial.print("Arduino9150 starting using device "); Serial.println(0);
  Wire.begin();
  MPU0.selectDevice(1);
  MPU0.init(MPU_UPDATE_RATE, MPU_MAG_MIX_GYRO_AND_MAG, MAG_UPDATE_RATE, MPU_LPF_RATE);
 
  Serial.print("Arduino9150 starting using device "); Serial.println(1);
  MPU1.selectDevice(0);
  MPU1.init(MPU_UPDATE_RATE, MPU_MAG_MIX_GYRO_AND_MAG, MAG_UPDATE_RATE, MPU_LPF_RATE);
}

void loop()
{
  MPU0.selectDevice(1);
  if (MPU0.read()) {
    Serial.print(MPU0.m_fusedEulerPose[VEC3_X] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU0.m_fusedEulerPose[VEC3_Y] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU0.m_fusedEulerPose[VEC3_Z] * RAD_TO_DEGREE);
    mpu0 = 1; 
    } else {
      mpu0 = 0;
    }
    
  MPU1.selectDevice(0);
  if (MPU1.read()) {
    Serial.print(',');
    Serial.print(MPU1.m_fusedEulerPose[VEC3_X] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU1.m_fusedEulerPose[VEC3_Y] * RAD_TO_DEGREE);
    Serial.print(',');
    Serial.print(MPU1.m_fusedEulerPose[VEC3_Z] * RAD_TO_DEGREE);
    mpu1 = 1;
    }
    
    if (mpu0 == 1 && mpu1 == 1){
      Serial.println();
    }
}

