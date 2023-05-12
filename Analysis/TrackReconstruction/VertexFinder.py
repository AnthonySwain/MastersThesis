#Function file to be called from FindInteractions.py
#Function takes two lines, finds the cloest approach and assigns the central point of the line that connects the closest points as the vertex of the single scattering action
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
    #Function takes two lines, finds the cloest approach and assigns the central point of the 
    #line that connects the closest points as the vertex of the single scattering action

    #Returns scattering vertex, angle and various weightings. 
    
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
    distance = np.linalg.norm(vertex1 - vertex2)

    #Find the angle between the lines


    angle = line1dir.angle_between(line2dir)
    scattered_angle_x_1 = line1dir.angle_between([1,0,0]) 
    scattered_angle_y_1 = line1dir.angle_between([0,1,0]) 

    scattered_angle_x_2= line2dir.angle_between([1,0,0]) 
    scattered_angle_y_2 = line2dir.angle_between([0,1,0])

    if scattered_angle_x_1 > math.pi/2:
        scattered_angle_x_1 = math.pi - scattered_angle_x_1
    
    if scattered_angle_y_1 > math.pi/2:
        scattered_angle_y_1 = math.pi - scattered_angle_y_1

    if scattered_angle_x_2 > math.pi/2:
        scattered_angle_x_2 = math.pi - scattered_angle_x_2

    if scattered_angle_y_2 > math.pi/2:
        scattered_angle_y_2 = math.pi - scattered_angle_y_2
    #Making sure the angle is in the right quadrant
    if angle > math.pi/2:
        angle = math.pi - angle

    xscat = abs(scattered_angle_x_1-scattered_angle_x_2)
    yscat = abs(scattered_angle_y_1-scattered_angle_y_2)
    
    
    #Putting a quality factor to vertex points based on closest intersect of the lines
    #(i.e divide scattering angle by closest intersect) the closer the incoming and outgoing muon track lines
    #are, the better constructed the line and more believeable it is. For lines that are further apart - likely
    #to represent multiple scattering events which the track reconstruction algorithm doesn’t account for
    #so it would give less weighting to them which could reduce the noise in the reconstructed images.
    
    #Maybe include a bit of softening
    qual_angle =  angle/distance    
    
    
        

    return (angle, intersection,qual_angle,xscat,yscat)


