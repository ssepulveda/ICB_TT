# -*- coding: utf-8 -*-
#!/usr/bin/env python
from serialProcess import SerialProcess
from multiprocessing import Queue

# OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

new = [0.0]*7;
cal = [0.0]*7;
first = True;

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)

def display():
    global new, cal, first;
    if not queue.empty():
        tmp = queue.get(True, .1)
        # print len(tmp)
        if len(tmp)>6:
            new = tmp
            if first is True:
                cal = new
                first = False
            else:
                for c in range(0, len(cal)):
                    new[c] = new[c] - cal[c]
                    # print new
            # print ["%0.2f" % i for i in new]

    glClear(GL_COLOR_BUFFER_BIT)
    glPushMatrix()
    # centro de giro
    glTranslatef(0.0, 0.0, 0.0)

    # hombro
    glTranslatef(0.0, 1.0, 0.0)
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glutSolidSphere(.25 ,10 ,10)
    glPopMatrix()

    # brazo
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(new[1], -1.0, 0.0, 0.0)
    glRotatef(new[2], 0.0, -1.0, 0.0)
    glRotatef(new[3], 0.0, 0.0, 1.0)
    glTranslatef(0.0, -1.0, 0.0)
    glPushMatrix()
    glScalef(0.2, 2.0, 0.2)
    glColor3f(0.0, 1.0, 0.0)
    glutSolidCube(1.0)
    glPopMatrix()

    # codo
    glTranslatef(0.0,-1.0, 0.0)
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glutSolidSphere(.25 ,10 ,10)
    glPopMatrix()

    # antebrazo
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(new[5], -1.0, 0.0, 0.0)
    glRotatef(new[5], 0.0, -1.0, 0.0)
    glRotatef(new[6], 0.0, 0.0, 1.0)
    glTranslatef(0.0, -1.0, 0.0)
    glPushMatrix()
    glScalef(0.2, 2.0, 0.2)
    glColor3f(0.0, 0.0, 1.0)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()
    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(65.0, float(w)/float(h), 1.0, 20.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5.0)

def keyboard(*args):
   if args[0] == 'c':
        global first
        first = True

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("title")
    init()
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':
    queue = Queue(512)
    data = SerialProcess(queue)
    #~ data.openPort("/dev/ttyACM0", 115200)
    data.openPort("/dev/ttyUSB0", 115200)
    data.start()
    main()
