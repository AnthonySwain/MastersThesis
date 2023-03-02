import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize
import math

from skspatial.objects import Line, Points, Vector

from skspatial.plotting import plot_3d

def vertex_angle_find(line1,line2):
    #Finds the intersection of the re-constructed tracks.
    angle = float
    vertex = [float,float,float]
    #The lines don't actually intersect but they nearly do - say intersection if halfway between
    #the shortest distance between the lines 

    #shortest distance between the 2 lines
    short_distance = line1.distance_line(line2)

    line1pos = line1.point
    line1dir = line1.direction

    line2pos = line2.point
    line2dir = line2.direction

    #if the lines are modelled as r = a + b*lambda, we need to find lambda1, lambda2 to find the point at which they are the closest
    #so lambda2*dir2 - lambda1*dir1 = short_distance * (cross product of direction vectors) - (point1 - point2)
    # is the equation that we need to solve, this is kinda an over-solution as 3 equations for 2 unknowns - just use 2 of the equations

    direction_cross = np.cross(line1dir,line2dir)
    direction_cross_normalised = direction_cross / np.linalg.norm(direction_cross)
    
    # line2dir[0] * x - line1dir[0] * y = short_dist (cross of direction vectors) + (pos1[0] - pos2[0])
    
    #Setting up the simaltaneous equations
    a0 = [line2dir[0],-line1dir[0]]
    b0 = (short_distance * direction_cross_normalised[0]) + (line1pos[0]-line2pos[0])

    a1 = [line2dir[1],-line1dir[1]]
    b1 = (short_distance * direction_cross_normalised[1]) + (line1pos[1]-line2pos[1])

    a2 = [line2dir[2],-line1dir[2]]
    b2 = (short_distance * direction_cross_normalised[2]) + (line1pos[2]-line2pos[2])

    a = np.array([a0,a2])
    b = np.array([b0,b2])

    #Solving the simaltaneous equations
    x = np.linalg.solve(a,b)
    lambda1 = x[1]
    lambda2 = x[0]

    #Finding the points of closest distance 
    vertex1 = line1pos + line1dir*lambda1
    vertex2 = line2pos + line2dir*lambda2

    #The middle of these points
    intersection = (vertex1 + vertex2) /2 


    #Find the angle between the lines


    angle = line1dir.angle_between(line2dir)
    if angle > math.pi/2:
        angle = math.pi - angle
    
    #Something weird has happened if this happens... #Put better error finder here.
    if angle > math.pi/2:
        return (0.0,intersection)

    return (angle, intersection)


