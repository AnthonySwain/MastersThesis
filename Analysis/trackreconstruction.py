
#Track Reconstruction for data. 

# Outline of the problem: 
# Get Data from files (ideally this will be in a seperate file that I 
# can call later but for now it will able be in this file)

# Perform a Chi squared minimisation for incoming, outcoming tracks based off of particle hits on the detector
# enforcing that they intersect at a point
# (the point is a large scattering event / accumulation of coulomb scatterings) 

#For ease I am not going to enfore this intersection, mainly because I am not sure how at the moment 

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d


def get_real():
    #Extracting data from the reality of the particle travel
    df = pd.read_csv("/home/anthony/sim/build/datatest2.csv")#opening the data file
    pos_in_X = df["PosX"].values
    pos_in_Y = df["PosY"].values
    pos_in_Z = df["PosZ"].values 
    reality = (pos_in_X,pos_in_Y,pos_in_Z)
    reality = np.stack(reality, axis=1)
    return(reality)

def get_hits():
    #Getting position and times of the hits from the data file. 
    #In_hits should contain the incoming hits and times
    #Out_hits should contain the outgoing hits and times

    data_frame = pd.read_csv("/home/anthony/sim/build/DetectorHits.csv") #opening the data file

    #Splitting data into position and time for in and out detector and returning an arary of this.
    in_detector = data_frame.query("volume_name == 'InDetector'")
    out_detector = data_frame.query("volume_name == 'OutDetector'")

    pos_in_X = in_detector["PosX"].values
    pos_in_Y = in_detector["PosY"].values
    pos_in_Z = in_detector["PosZ"].values
    time_in = in_detector["time"].values

    in_hits = (pos_in_X,pos_in_Y,pos_in_Z)
    in_times = np.stack(time_in, axis=0)
    in_hits = np.stack(in_hits, axis=1)
    

    pos_out_X = out_detector["PosX"].values
    pos_out_Y = out_detector["PosY"].values
    pos_out_Z = out_detector["PosZ"].values
    time_out = out_detector["time"].values

    out_hits = (pos_out_X,pos_out_Y,pos_out_Z)
    out_times = np.stack(time_out, axis=0)
    out_hits = np.stack(out_hits, axis=1)

    return(in_hits, in_times, out_hits, out_times)

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

def get_line_coords(line):
    #Converting line equation into a set of points to plot 
    r0 = line.point
    z0 = r0[2]

    d = line.direction
    dz = d[2]

    z = np.linspace(-1500,1500,3000)
    const = np.subtract(z,(z0*np.ones(np.shape(z)))) /dz

    y = r0[1]* np.ones(np.shape(z)) + const * d[1]
    x = r0[0]* np.ones(np.shape(z)) + const* d[0]

    return(x,y,z)

#Extracting hits
hits_data = get_hits()
pos_hits_in = hits_data[0]
pos_hits_out = hits_data[2]

result = fit_lines(pos_hits_in, pos_hits_out)

line1 = Line(result[0:3],result[3:6])

line2 = Line(result[6:9],result[9:12])

reality = get_real()


#Plotting a figure to check all is well.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Limits of the axes
xylim = 200
zlim = 1500

ax.set_xlim([-1*xylim,xylim])
ax.set_ylim([-1*xylim,xylim])
ax.set_zlim([-1*zlim,zlim])


#Points that made the lines
ax.scatter(pos_hits_in[:,0],pos_hits_in[:,1],pos_hits_in[:,2])
ax.scatter(pos_hits_out[:,0],pos_hits_out[:,1],pos_hits_out[:,2])
ax.scatter(reality[:,0],reality[:,1],reality[:,2], s=5)

#r = r_0 + const * d 

x1,y1,z1 = get_line_coords(line1)
x2,y2,z2 = get_line_coords(line2)

ax.plot(x1,y1,z1)
ax.plot(x2,y2,z2)

plt.show()