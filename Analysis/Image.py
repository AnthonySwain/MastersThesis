#Makes a heatmap of the interaction points with colour based off of the angle scattered
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize
from skspatial.plotting import plot_3d
import seaborn as sns

data_frame = pd.read_csv("/home/anthony/sim/data/interactions&angle.csv") #opening the data file
angle = data_frame["angle"].values
x = data_frame["x"].values
y = data_frame["y"].values  
z = data_frame["z"].values
data = data_frame.drop(["z"],axis=1)

data = data.loc[data['x'] <= 1000]
data = data.loc[data['y'] <= 1000]
data = data.loc[data['y'] >= -1000]
data = data.loc[data['y'] >= -1000]

def scatter_map(x,y,z,angle):
    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    xylim = 200
    zlim = 1500

    ax.set_xlim([-1*xylim,xylim])
    ax.set_ylim([-1*xylim,xylim])
    ax.set_zlim([-1*zlim,zlim])

    ax.scatter(x,y,z, s=angle*10)#,c=angle,cmap='Greens_r')
    plt.show()

    return(None)

def scat_angle_dist(x,y,z,angle):
    plt.hist(angle, bins = 100)

    plt.xlabel("Scattered angle / radians")
    plt.ylabel("Count")
    plt.show()

    return(None)

def voxel_map(data):
    sns.set()
    data = data.pivot(index = 'x',columns = "y",values = "angle")
    ax = sns.heatmap(data )
    xlim = 600
    ylim = 600

    ax.set_xlim([-1*xlim,xlim])
    ax.set_ylim([-1*ylim,ylim])
    plt.show()
    return(None)

#scat_angle_dist(x,y,z,angle)
#scatter_map(x,y,z,angle)
voxel_map(data)
