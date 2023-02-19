#Plotting the initally created muon distributions to ensure they follow the distributions of cosmic ray muons

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

data_frame = pd.read_csv("/home/anthony/sim/build/Initial_Muon_Dist.csv") #opening the data file

PDGnumb = data_frame["PDGnumb"].values
PosX = data_frame["PosX"].values
PosY = data_frame["PosY"].values
PosZ = data_frame["PosZ"].values
Momentum = data_frame["Momentum[GeV]"].values
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

def zenith_angle(theta):
    plt.hist(theta, bins = 50)
    plt.xlabel("Zenith angle / radians")
    plt.ylabel("Count")
    plt.show()
    return(None)

zenith_angle(theta)

ratio = ratio_created(PDGnumb)
print(ratio)
print(1/ratio)