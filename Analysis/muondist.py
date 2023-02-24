#Plotting the initally created muon distributions to ensure they follow the distributions of cosmic ray muons

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize
import seaborn as sns

data_frame = pd.read_csv("/home/anthony/sim/data/Initial_Muon_Dist.csv") #opening the data file

PDGnumb = data_frame["PDGnumb"].values
PosX = data_frame["PosX"].values
PosY = data_frame["PosY"].values
PosZ = data_frame["PosZ"].values
momentum = data_frame["Momentum[GeV]"].values
theta = data_frame["theta"].values
phi = data_frame["phi"].values




#Plots we want: 
#Plane of where the muons created (evenly distributed hopefully)
#Differential intensity at different angles (see EcoMug article for insipiration)

#Data: ratio of muons to anti muons
def ratio_created(PDGnumb):
    muon = np.count_nonzero(PDGnumb == 13)
    anti_muon = np.count_nonzero(PDGnumb == -13)
    ratio = anti_muon / muon
    return(ratio)

#Zenith angle created at
def zenith_angle(theta):
    plt.hist(theta, bins = 100)
    plt.xlabel("Zenith angle / radians")
    plt.ylabel("Count")
    plt.show()
    return(None)

#Azimuth angle created at 
def azimuth_angle(phi):
    plt.hist(phi, bins = 100)
    plt.xlabel("Azimuth / radians")
    plt.ylabel("Count")
    plt.show()
    return(None)

def differential_intensity(theta, momentum):
#Calculates the differential intensity and plots.
#Assuming 10,000 muons m^2 / min 
    diff_intensity = 0
    return(None)

def position_created(x,y):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=100)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap.T, interpolation = 'gaussian',extent=extent, origin='lower')
    plt.show()
    return(None)

position_created(PosX,PosY)
#zenith_angle(theta)
#azimuth_angle(phi)

ratio = ratio_created(PDGnumb)
print(ratio)
print(1/ratio)