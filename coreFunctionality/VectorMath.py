'''
Created on May 1, 2014

@author: Matthias
'''

import math
import numpy as np


    
    
def getPointDistance ( point1, point2 ):
    return getVectorMagnitude(createVector(point1, point2))
    
def createVector ( pointStart, pointEnd ):
    vector = []
    for i,j in zip(pointEnd, pointStart):
        vector.append(int(i)-int(j))
    return vector

def getVectorMagnitude( vector ):
    return math.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)

def unit_vector( vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle

def angle2DVector(vec):
    x = float(vec[0])
    y = float(vec[1])
    if x == 0 and y > 0:
        return math.pi * 0.5
    elif x == 0 and y < 0:
        return math.pi * 1.5
    elif y == 0 and x > 0:
        return 0
    elif y == 0 and x < 0:
        return math.pi
    elif x > 0 and y > 0:
        return math.atan(abs(y)/abs(x))
    elif x < 0 and y > 0:
        return math.pi * 0.5 + math.atan(abs(x)/abs(y))
    elif x < 0 and y < 0:
        return math.pi + math.atan(abs(y)/abs(x))
    elif x > 0 and y < 0:
        return math.pi * 1.5 + math.atan(abs(x)/abs(y))
    
def angleBetween2D(v1,v2):
    
    av1 = angle2DVector(v1)
    av2 = angle2DVector(v2)
    angle = av2 - av1
    return angle
    
def mapToDomain (value, min1, max1, min2, max2 ):
    return  ( ( float(value) - float(min1) ) / ( float(max1) - float(min1) ) )*( float(max2) - float(min2) ) + float(min2)
            
def radToDeg(angle):
    return angle * 180 / math.pi
