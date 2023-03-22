#Track Reconstruction for data. 

# Perform a Chi squared minimisation for incoming, outcoming tracks based off of particle hits on the detector
# enforcing that they intersect at a point (if called upon to do this, takes significantly more computing power)
# assuming single point of scattering 

#This is merely a file of functions to do the above, it is called from FindInteractions.py

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d

def least_squares(hits):
    line_fit = Line.best_fit(hits)
    
    return(line_fit)

def objective_function(params, x1,y1,z1,x2,y2,z2):
    #notes for later tony, d1,d2 are for the position vectors of the lines (but there should be 3 of these as its a vector
    # not just one so this needs to be changed along with where the linest intersect.)
    # Also check the constraint equations for the intersection is correct...

    #The algorithm minimises the distance between the 2 lines and the chi squared for each set of data points
    
    # r = r0 + u*d 
    # r0 - position vector 
    # d - direction vector 
    
    #Unpack parameters // initial guess
    p10,p11,p12,d10,d11,d12,p20,p21,p22,d20,d21,d22 = params
    pos_in = np.array([p10,p11,p12])
    direction_in = np.array([d10,d11,d12])

    pos_out = np.array([p20,p21,p22])
    direction_out = np.array([d20,d21,d22])
    
    in_line = Line (pos_in, direction_in)
    out_line = Line(pos_out, direction_out)
    ##okay so lets use x and y values to predict the z value and compare to the actual z value? 
    #mean squared error line 1

    mse1 = mse(pos_in,direction_in,x1,y1,z1)
    
    #mean squared error line 2
    mse2 = mse(pos_out,direction_out,x2,y2,z2)
    
    #shortest distance between the lines
    distance = (in_line.distance_line(out_line))
    
    # Return the sum of the mean squared errors and the distance as the objective function
    return mse1 + mse2 + distance

def mse(pos_vector, direction_vector, x,y,z):
    # x = x_0 + const * d 
    size = np.size(x)

    const = (x - pos_vector[0] * np.ones(size)) / direction_vector[0]
    
    
    y_predict = pos_vector[1] * np.ones(size) + const*direction_vector[1]
    
    z_predict = pos_vector[2] * np.ones(size) + const*direction_vector[2]

    msey = np.sum(np.square(y-y_predict))
    msez = np.sum(np.square(z-z_predict))

    mse = np.power(np.power(msey,2) + np.power(msez,2), 0.5)

    return (mse)

def fit_lines(pos_hits_in,pos_hits_out):
    #pos_hits_in and out are the 2 sets of datapoints for each line
    #May be useful to vectorise this in the future.

    # Finding lines of best for the in and out hits data (initial guess)
    in_line = least_squares(pos_hits_in)
    pos_in = in_line.point
    direction_in = in_line.direction

    out_line = least_squares(pos_hits_out)  
    pos_out = out_line.point
    direction_out = out_line.direction
    #Initial guess of the parameters (position and direction vectors of each line)
    params0 = [pos_in[0],pos_in[1],pos_in[2],
    direction_in[0],direction_in[1],direction_in[2],
    pos_out[0],pos_out[1],pos_out[2],
    direction_out[0],direction_out[1],direction_out[2]]
    
    # Minimize the objective function using the BFGS algorithm
    x1, y1, z1 = pos_hits_in[:,0],pos_hits_in[:,1],pos_hits_in[:,2]
    x2, y2, z2 = pos_hits_out[:,0],pos_hits_out[:,1],pos_hits_out[:,2]
    result = minimize(objective_function, params0, args=(x1, y1, z1, x2, y2, z2), method='BFGS')
    
    # Return the optimal coefficients
    return result.x

def get_line_coords(line,z_min,z_max,no_points):
    #Converting line equation into a set of points to plot 
    r0 = line.point
    z0 = r0[2]

    d = line.direction
    dz = d[2]

    z = np.linspace(z_min,z_max,no_points)
    const = np.subtract(z,(z0*np.ones(np.shape(z)))) /dz

    x = r0[0]* np.ones(np.shape(z)) + const* d[0]
    y = r0[1]* np.ones(np.shape(z)) + const * d[1]
    

    return(x,y,z)

def residues_get(line,hits):
    residues_square = []
    no_hits = int(np.size(hits)/3)
    print(np.size(hits)/3)
    for i in range(no_hits):
        residues_square.append((line.distance_point(hits[i])**2))

    
    error = np.power( np.sum(residues_square) / (no_hits - 2),1/2)

    return(error)