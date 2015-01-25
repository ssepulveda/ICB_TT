# -*- coding: utf-8 -*-
# QtCore for connect signal, thread
from PyQt4 import QtCore
from baseThread import BaseThread

# folder access
import sys
import os

# Set Debug
from log import Log
log = Log("Cube")
log.setVerbose(True)

# OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# textures
from Image import *

# integration and maths
from numpy import trapz
from math import sin, cos


## Displays the orientation as a 3D cube
#
class Cube(BaseThread):
    # glut window reference
    window = 0
    Y = 0
    P = 0
    R = 0
    LAX = [0.0]*10
    LAY = [0.0]*10
    LAZ = [0.0]*10
    X = 0
    Y = 0
    Z = 0

    ## Constructor
    #
    # @param data Pass SerialThread object to connect signal
    def __init__(self, data):
        BaseThread.__init__(self)
        # connect to signal from data thread
        self.data = data
        QtCore.QObject.connect(self.data, QtCore.SIGNAL('newData()'),
                               self.updateData)
        self.R2 = 0
	
	## Gets data from serial thread
	#
	# @param self The object pointer.
    def updateData(self):
        # get angles
        [self.P, self.R, self.Y] = self.data.getEulerDMP()
        # get linear acceleration
        #~ [x, y, z] = self.data.getLinearAccel()

	## Main function
	#
	# Inits and configures all the GLUT parameters to and defines the
	# associated functions to each event
	# @param self The object pointer.
    def run(self):
        # init GLUT
        glutInit(sys.argv)
        # set GLUT display mode
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        # set GLUT window size
        glutInitWindowSize(640, 480)
        # set position of GLUT window
        glutInitWindowPosition(200, 200)
        # show GLUT window
        self.window = glutCreateWindow('FONDEF: prueba 3D')
        # register draw function
        glutDisplayFunc(self.display)
        # redraw scene when idle
        glutIdleFunc(self.display)
        # reshape function register
        glutReshapeFunc(self.reshape)
        # register keylisterner function
        glutKeyboardFunc(self.KeyPressed)
        # init window
        self.InitGL(640, 480)
        glutMainLoop()

	## Inits OpenGL
	#
	# @param self The object pointer.
	# @param Width size of the Window
	# @param Height size of the Window
    def InitGL(self, Width, Height):
        # clear backgound R,G,B,A
        glClearColor(0, 0, 0, 0)
        # clear depth buffer
        glClearDepth(1)
        # The Type Of Depth Test To Do
        glDepthFunc(GL_LESS)
        # Enables Depth Testing
        glEnable(GL_DEPTH_TEST)
        # Enables Smooth Color Shading
        glShadeModel(GL_SMOOTH)
        # textures
        #~ self.LoadTextures()
        #~ glEnable(GL_TEXTURE_2D)

	## Draws the arms with the rotation data
	#
	# @param self The object pointer.
    def display(self):
        # clear screen (depth buffer)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Forearm
        glPushMatrix()
        #~ glTranslatef(-1, 0, 0)
        # rotate
        glRotatef(-self.P, 1, 0, 0)
        glRotatef(self.Y, 0, 1, 0)
        glRotatef(self.R, 0, 0, 1)
        #~ glTranslatef(-1, 0, 0)
        # draw object
        self.drawForearm()
        # apply modifications
        glPopMatrix()

        # Arm
        """
        glPushMatrix()
        #glTranslatef(0, 0, 0)
        # rotate
        #~ glRotatef(self.P2, 1, 0, 0)
        #~ glRotatef(self.Y2, 0, 1, 0)
        glRotatef(self.R2, 0, 1, 0)
        glRotatef(self.R2, 0, 0, 1)
        self.R2 += .5
        glTranslatef(1, 0, 0)
        # draw object
        self.drawArm()
        # apply modifications
        glPopMatrix()
        """

        # Swap Buffers
        glutSwapBuffers()

    def newPosition(self, yaw, pitch, roll, r):
        # asuming this can be represented as spherical coordinates
        # http://en.wikipedia.org/wiki/
        # Spherical_coordinate_system#Cylindrical_coordinates
        i = yaw  # inclinacion
        a = pitch  # azimuth
        x = r*sin(i)*cos(a)
        y = r*sin(i)*sin(a)
        z = r*cos(i)
        return [x, y, z]

	## 
	#
	# @param self The object pointer.
	# @param Width size of the Window
	# @param Height size of the Window
    def reshape(self, Width, Height):
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #~ gluPerspective(450, float(Width)/float(Height), .1, 100)
        gluPerspective(45, float(Width)/float(Height), .1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -6)

	## Callback for keypress events
	#
	# @param self The object pointer.
	# @param args Pointer to the args for accesing input data
    def KeyPressed(self, *args):
        if args[0] == '\33':
            # escape key, terminate app
            self.data.closePort()
            sys.exit()
        else:
            # not described
            print (str(args[0]))

	## Draws cube for the foreaarm representation
	#
	# @param self The object pointer.
    def drawForearm(self):
        glBegin(GL_QUADS)
        # Top, green
        glColor3f(0, 1, 0)
        glVertex3f(1, .2, -1)
        glVertex3f(-1, .2, -1)
        glVertex3f(-1, .2, 1)
        glVertex3f(1, .2, 1)
        # Bottom, orange
        glColor3f(1, .5, 0)
        glVertex3f(1, -.2, 1)
        glVertex3f(-1, -.2, 1)
        glVertex3f(-1, -.2, -1)
        glVertex3f(1, -.2, -1)
        # Front, red (initial view)
        glColor3f(1, 0, 0)
        glVertex3f(1, .2, 1)
        glVertex3f(-1, .2, 1)
        glVertex3f(-1, -.2, 1)
        glVertex3f(1, -.2, 1)
        # Back, yellow
        glColor3f(1, 1, 0)
        glVertex3f(1, -.2, -1)
        glVertex3f(-1, -.2, -1)
        glVertex3f(-1, .2, -1)
        glVertex3f(1, .2, -1)
        # Lateral (left), blue
        glColor3f(0, 0, 1)
        glVertex3f(-1, .2, 1)
        glVertex3f(-1, .2, -1)
        glVertex3f(-1, -.2, -1)
        glVertex3f(-1, -.2, 1)
        # Lateral (right), pink
        glColor3f(1, 0, 1)
        glVertex3f(1, .2, -1)
        glVertex3f(1, .2, 1)
        glVertex3f(1, -.2, 1)
        glVertex3f(1, -.2, -1)
        glEnd()

	## Draws cube for the arm representation
	#
	# @param self The object pointer.
    def drawArm(self):
        glBegin(GL_QUADS)
        # Top, green
        glColor3f(0, 1, 0)
        glVertex3f(1, .2, -1)
        glVertex3f(-1, .2, -1)
        glVertex3f(-1, .2, 1)
        glVertex3f(1, .2, 1)
        # Bottom, orange
        glColor3f(1, .5, 0)
        glVertex3f(1, -.2, 1)
        glVertex3f(-1, -.2, 1)
        glVertex3f(-1, -.2, -1)
        glVertex3f(1, -.2, -1)
        # Front, red (initial view)
        glColor3f(1, 0, 0)
        glVertex3f(1, .2, 1)
        glVertex3f(-1, .2, 1)
        glVertex3f(-1, -.2, 1)
        glVertex3f(1, -.2, 1)
        # Back, yellow
        glColor3f(1, 1, 0)
        glVertex3f(1, -.2, -1)
        glVertex3f(-1, -.2, -1)
        glVertex3f(-1, .2, -1)
        glVertex3f(1, .2, -1)
        # Lateral (left), pink
        glColor3f(1, 0, 1)
        glVertex3f(-1, .2, 1)
        glVertex3f(-1, .2, -1)
        glVertex3f(-1, -.2, -1)
        glVertex3f(-1, -.2, 1)
        # Lateral (right), blue
        glColor3f(0, 0, 1)
        glVertex3f(1, .2, -1)
        glVertex3f(1, .2, 1)
        glVertex3f(1, -.2, 1)
        glVertex3f(1, -.2, -1)
        glEnd()

	## Add textures for the cube
	#
	# Applies a png image as a texture for the faces of the cube
	# @note experimental
	# @param self The object pointer.
    def LoadTextures(self):
        image = open(os.path.join(sys.path[0], 'resources/MPU_front.png'))
        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

if __name__ == "__main__":
    # imports for self running
    from PyQt4 import QtGui
    from serialThread import SerialThread
    # QtThread won't work without QApplication
    app = QtGui.QApplication(sys.argv)
    # init data thread
    data = SerialThread('MPU-9150')
    #~ data.openPort('/dev/ttyACM0', 115200)
    data.openPort('/dev/ttyUSB0', 115200)
    data.start()
    # self init cube
    cube = Cube(data)
    cube.start()
    # start (and exit) QApplication for executing
    sys.exit(app.exec_())
