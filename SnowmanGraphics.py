# File: SnowmanGraphics.py

"""
This module is responisble for drawing the Snowman figure by assembling
a compound with the relevant body parts.
"""

from pgl import GCompound, GOval, GLine, GPolygon
from SnowmanConstants import *
import math

# Derived Constants for placement

BASE_X = -.5 * BASE_SIZE
BASE_Y = -BASE_SIZE
BODY_X = -.5 * BODY_SIZE
BODY_Y = -BASE_SIZE - BODY_SIZE
HEAD_X = -.5 * HEAD_SIZE
HEAD_Y = -BASE_SIZE - BODY_SIZE - HEAD_SIZE
L_ARM_X_1 = -.5 * HEAD_SIZE
L_ARM_X_2 = L_ARM_X_1 - .5 * ARM_LENGTH
R_ARM_X_1 = -L_ARM_X_1
R_ARM_X_2 = -L_ARM_X_2
ARM_Y_1 = -BASE_SIZE - BODY_SIZE + .15 * BODY_SIZE
ARM_Y_2 = ARM_Y_1 - .5 * ARM_LENGTH
L_EYE_X = -.5 * EYE_SEP - EYE_SIZE / 2
R_EYE_X = .5 * EYE_SEP - EYE_SIZE / 2
EYE_Y = -BASE_SIZE - BODY_SIZE - HEAD_SIZE + .25 * HEAD_SIZE
NOSE_TIP = -BASE_SIZE - BODY_SIZE - HEAD_SIZE + .38 * HEAD_SIZE

def createEmptySnowman(gw):
    """
    Creates an empty GCompound to use as the snowman and adds it to
    the window at the correct location. This function then returns
    the GCompound for use in later calls to addSnowmanPart.
    """
    snowman = GCompound()
    x = GWINDOW_WIDTH / 2
    y = GWINDOW_HEIGHT - SNOWMAN_BASE
    gw.add(snowman, x, y)
    return snowman

def addSnowmanPart(snowman, index):
    """
    Adds the body part with the specified index to the snowman.
    """

    def createSnowball(size):
        if size == 'base':
            snowball = GOval(BASE_SIZE, BASE_SIZE)
            snowman.add(snowball, BASE_X, BASE_Y)
        elif size == 'body':
            snowball = GOval(BODY_SIZE, BODY_SIZE)
            snowman.add(snowball, BODY_X, BODY_Y)
        else:
            snowball = GOval(HEAD_SIZE, HEAD_SIZE)
            snowman.add(snowball, HEAD_X, HEAD_Y)

    def createArm(pos):
        if pos == 'left':
            arm = GLine(L_ARM_X_1, ARM_Y_1, L_ARM_X_2, ARM_Y_2)
        else:
            arm = GLine(R_ARM_X_1, ARM_Y_1, R_ARM_X_2, ARM_Y_2)
        snowman.add(arm)

    def createEye(pos):
        eye = GOval(EYE_SIZE, EYE_SIZE)
        eye.setFilled(True)
        if pos == 'left':
            snowman.add(eye, L_EYE_X, EYE_Y)
        else:
            snowman.add(eye, R_EYE_X, EYE_Y)

    def createNose():
        nose = GPolygon()
        nose.addVertex(0, NOSE_TIP)
        nose.addEdge(NOSE_WIDTH * -.5, NOSE_HEIGHT)
        nose.addEdge(NOSE_WIDTH, 0)
        snowman.add(nose)

    # Large snowball forming the base
    if index == 1:
        createSnowball('base')
    # Middle snowball forming the body
    elif index == 2:
        createSnowball('body')
    # Small snowball forming the head
    elif index == 3:
        createSnowball('head')
    # Left arm
    elif index == 4:
        createArm('left')
    # Right arm
    elif index == 5:
        createArm('right')
    # Left eye
    elif index == 6:
        createEye('left')
    # Right eye
    elif index == 7:
        createEye('right')
    # Nose
    else:
        createNose()