#!/usr/bin/env python
import time, math
from log import Log

# Set debug
log = Log("SensorFusion")
DEG2RAD = 0.0174532925

## Algorithms and functions for 9DOF fusion
#
# Uses data from accelerometers, gyroscopes and magnetometers to
# do sensor fusion and obtain orientation of the device in a quaternion
# representation.
# @author Sebastian Sepulveda
class SensorFusion:

    ## Constructor
    #
    # Initializes variables for the algorithm
    # @param self The object pointer
    def __init__(self):
        ## Last quaternion holder
        self.q=[0.0001]*4
        ## Last Linear accerlation
        self.linearAcceleration=[0.0]*3
        ## Gains of the algorithm
        self.Kp=2.0
        ## Gains of the algorithm
        self.Ki=0.005
        
        ## Time between updates
        self.lastUpdate = time.time()
        self.exInt = 0.0
        self.eyInt = 0.0
        self.ezInt = 0.0

        log.i("Init sensor fusion thread")
        
    ## Update the orientatation with sensors data
    #
    # Sensor fusion algorithm ported by Fabio Varesano to Python from
    # the Sebastian Madgwick 9DOF fusion.
    #
    # Data must be inputed as:
    # + Accelerations in g (gravities)
    # + Gyroscope in radians per second (rad/sec)
    # + Magnetometer in Gauss (Gs)
    #
    # @param self The object pointer
    # @param gyroscope Gyroscope data as [X,Y,Z] in rad/sec
    # @param accelerometer Accelerometer data as [X,Y,Z] in g (gravities)
    # @param magnetometer Magnetometer data as [X,Y,Z] in Gs
    #
    # @author Fabio Varesano
    # @author Sebastian Madgwick
    def update9DOF(self, gyroscope, accelerometer, magnetometer):
        gx = gyroscope[0]*DEG2RAD
        gy = gyroscope[1]*DEG2RAD
        gz = gyroscope[2]*DEG2RAD
        ax = accelerometer[0]
        ay = accelerometer[1]
        az = accelerometer[2]
        mx = magnetometer[0]
        my = magnetometer[1]
        mz = magnetometer[2]
        q0=self.q[0]
        q1=self.q[1]
        q2=self.q[2]
        q3=self.q[3]
        
        # auxiliary variables to reduce number of repeated operations
        q0q0 = q0*q0
        q0q1 = q0*q1
        q0q2 = q0*q2
        q0q3 = q0*q3
        q1q1 = q1*q1
        q1q2 = q1*q2
        q1q3 = q1*q3
        q2q2 = q2*q2
        q2q3 = q2*q3
        q3q3 = q3*q3
        
        # normalise the measurements
        now = time.time()
        halfT = (now - self.lastUpdate) / 2.0
        self.lastUpdate = now
        
        # normalize accelerometer
        norm = math.sqrt(ax*ax + ay*ay + az*az)
        if norm > 0:
            ax = ax / norm
            ay = ay / norm
            az = az / norm
        
        # normalize magnetometer
        norm = math.sqrt(mx*mx + my*my + mz*mz)
        if norm > 0:
            mx = mx / norm
            my = my / norm
            mz = mz / norm
        
        # compute reference direction of flux
        hx = 2*mx*(0.5 - q2q2 - q3q3) + 2*my*(q1q2 - q0q3) + 2*mz*(q1q3 + q0q2)
        hy = 2*mx*(q1q2 + q0q3) + 2*my*(0.5 - q1q1 - q3q3) + 2*mz*(q2q3 - q0q1)
        hz = 2*mx*(q1q3 - q0q2) + 2*my*(q2q3 + q0q1) + 2*mz*(0.5 - q1q1 - q2q2)         
        bx = math.sqrt((hx*hx) + (hy*hy))
        bz = hz
        
        # estimated direction of gravity and flux (v and w)
        vx = 2*(q1q3 - q0q2)
        vy = 2*(q0q1 + q2q3)
        vz = q0q0 - q1q1 - q2q2 + q3q3
        wx = 2*bx*(0.5 - q2q2 - q3q3) + 2*bz*(q1q3 - q0q2)
        wy = 2*bx*(q1q2 - q0q3) + 2*bz*(q0q1 + q2q3)
        wz = 2*bx*(q0q2 + q1q3) + 2*bz*(0.5 - q1q1 - q2q2)  
        
        # error is sum of cross product between reference direction of fields and direction measured by sensors
        ex = (ay*vz - az*vy) + (my*wz - mz*wy)
        ey = (az*vx - ax*vz) + (mz*wx - mx*wz)
        ez = (ax*vy - ay*vx) + (mx*wy - my*wx)
        
        # integral error scaled integral gain
        self.exInt = self.exInt + ex*self.Ki
        self.eyInt = self.eyInt + ey*self.Ki
        self.ezInt = self.ezInt + ez*self.Ki
        
        # adjusted gyroscope measurements
        #"""
        gx = gx + self.Kp*ex + self.exInt 
        gy = gy + self.Kp*ey + self.eyInt
        gz = gz + self.Kp*ez + self.ezInt
        #"""
        
        # added halfT * 2.0 as suggested by Robert Bouwens <bouwens [dot] mehl [at] bluewin [dot] ch>
        gx = gx + self.Kp*ex + self.exInt * halfT * 2.0
        gy = gy + self.Kp*ey + self.eyInt * halfT * 2.0
        gz = gz + self.Kp*ez + self.ezInt * halfT * 2.0
        
        # integrate quaternion rate and normalise
        iq0 = (-q1*gx - q2*gy - q3*gz)*halfT
        iq1 = (q0*gx + q2*gz - q3*gy)*halfT
        iq2 = (q0*gy - q1*gz + q3*gx)*halfT
        iq3 = (q0*gz + q1*gy - q2*gx)*halfT  
        
        q0 += iq0
        q1 += iq1
        q2 += iq2
        q3 += iq3
        
        # normalise quaternion
        norm = math.sqrt(q0*q0 + q1*q1 + q2*q2 + q3*q3)
        if norm > 0:
            q0 = q0 / norm
            q1 = q1 / norm
            q2 = q2 / norm
            q3 = q3 / norm
        
        # return data
        self.q[0] = q0
        self.q[1] = q1
        self.q[2] = q2
        self.q[3] = q3
        
        # calculate linear acceleration
        self.LinearAcceleration(self.q, ax,ay,az)
        
    ## Compensate the accelerometer readings from gravity.
    #
    # Removes the offset generated by the earth's gravity
    # @param self The object pointer
    # @param q Quaternion representing the orientation
    # @param acc Readings coming from an accelerometer, in g
    # @return 3D vector with the Linear acceleration, in g
    # @author Fabio Varesano
    def LinearAcceleration(self,q,ax,ay,az):
        g=self.Gravity(q)
        
        self.linearAcceleration=[ax - g[0], ay - g[1], az - g[2]]

    ## Determinates the expected direction of the gravity
    #
    # Calculated the expected directions of the gravity in x, y and z
    # frame of reference
    # @param self The object pointer
    # @param q Quaternion representing the orientation
    # @return g vector with expected direction of the gravity
    def Gravity(self,q):
        g = [0.0, 0.0, 0.0]
        # get expected direction of gravity
        g[0] = 2 * (q[1] * q[3] - q[0] * q[2])
        g[1] = 2 * (q[0] * q[1] + q[2] * q[3])
        g[2] = q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3]

        return g

    ## Getter for the Quaternions
    #
    # Return last calculated quaternion from the last call of
    # @ref updateAHRS
    # @param self The object pointer
    # @return Last calculated quaternion
    def getQ(self):
        return self.q

    ## Getter for the Linear Acceleration
    #
    # Return last calculated linear acceleration from the last call of
    # @ref updateAHRS
    # @param self The object pointer
    # @return Last calculated Linear Acceleration
    def getLinearAcceleration(self):
        return self.linearAcceleration

    ## Getter for the Gravity direction
    #
    # Return last calculated gravity direction from the last call of
    # @ref updateAHRS
    # @param self The object pointer
    # @return Last calculated Gravity Direction
    def getGravityDirection(self):
        return self.Gravity(self.q)
    
    ## Getter for Orientation as Yaw, Pith, Roll
    #
    # Return last calculated orientation expresed as yaw, pitch and roll
    # from the last call of @ref updateAHRS
    # @param self The object pointer
    # @param deg
    # + @b TRUE : Return angles in degrees
    # + @b FALSE : Return angles in radians
    # @return Vector with yaw, pitch and roll
    # @author Fabio Varesano
    def getYawPitchRoll(self, deg = False):
        q=self.q
        ypr=[0.0]*3
        
        gx = 2 * (q[1]*q[3] - q[0]*q[2])
        gy = 2 * (q[0]*q[1] + q[2]*q[3])
        gz = q[0]*q[0] - q[1]*q[1] - q[2]*q[2] + q[3]*q[3]
        
        ypr[0]=math.atan2(2 * q[1] * q[2] - 2 * q[0] * q[3], 2 * q[0]*q[0] + 2 * q[1] * q[1] - 1)
        ypr[1]=math.atan(gx / math.sqrt(gy*gy + gz*gz))
        ypr[2]=math.atan(gy / math.sqrt(gx*gx + gz*gz))
        
        if deg == True:
            return map(math.degrees, ypr)
        else:
            return ypr
    
    ## Getter for Orientation as Euler angles
    #
    # Return last calculated orientation expresed as euler angles
    # from the last call of @ref updateAHRS
    # @param self The object pointer
    # @param deg
    # + @b TRUE : Return angles in degrees
    # + @b FALSE : Return angles in radians
    # @return Vector with Euler angles
    # @author Fabio Varesano
    def getEuler(self, deg = False):
        q=self.q
        
        euler = [0.0]*3
        euler[0] = math.atan2(2 * q[1] * q[2] - 2 * q[0] * q[3], 2 * q[0]*q[0] + 2 * q[1] * q[1] - 1); # yaw
        euler[1] = -math.asin(2 * q[1] * q[3] + 2 * q[0] * q[2]); # pitch
        euler[2] = math.atan2(2 * q[2] * q[3] - 2 * q[0] * q[1], 2 * q[0] * q[0] + 2 * q[3] * q[3] - 1); # roll
        
        if deg != False:
            return map(math.degrees, euler)
        return euler
