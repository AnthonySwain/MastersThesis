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
from matplotlib.colors import LinearSegmentedColormap

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

data_frame = pd.read_csv("/home/anthony/sim/data/interactions&angle.csv") #opening the data file
data_frame = data_frame[["x","y","z","angle"]]
data_frame = data_frame.loc[(data_frame.x > -500) &
                            (data_frame.x < 500) &
                            (data_frame.y > -500) &
                            (data_frame.y < 500) &
                            (data_frame.z > -2000) &
                            (data_frame.z < 2000)]

angle = data_frame["angle"].values
x = data_frame["x"].values
y = data_frame["y"].values  
z = data_frame["z"].values

data = data_frame.drop(["z"],axis=1)

xyz = data_frame.drop(["angle"],axis=1)


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
    xyz=pd.DataFrame(xyz).to_numpy()

    no_bins = 20
    hist, binedges = np.histogramdd(xyz, weights = angle, normed=False, bins = no_bins)
    print(np.shape(hist))
    #data = data.pivot(index = 'x',columns = "y",values = "angle")
    ax = sns.heatmap(hist)
    
    plt.imshow(hist)
    ax.set_xlim(-500, 500)
    ax.set_ylim(-500, 500)
    ax.set_zlim(-2000, 2000)

    plt.show()
    return(None)

def ct_esque(xyz,x,y,z,angle):
    xyz=pd.DataFrame(xyz).to_numpy()

    no_bins = 10
    hist, binedges = np.histogramdd(xyz, weights = angle, normed=False, bins = no_bins)
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot(x,y,z,'k.',alpha=0.3)
    #Use one less than bin edges to give rough bin location
    X, Y = np.meshgrid(binedges[0][:-1],binedges[1][:-1])
   
    #Y,Z = np.meshgrid(binedges[1][:-1],binedges[2][:-1])
    
    #Loop over range of slice locations
    #Create code to loop through bins
    bin_count = np.linspace(0,no_bins-1,40,dtype = 'int')
    
    # get colormap
    ncolors = 256
    color_array = plt.get_cmap('gist_rainbow')(range(ncolors))

    # change alpha values
    color_array[:,-1] = np.linspace(1.0,0.0,ncolors)

    # create a colormap object
    map_object = LinearSegmentedColormap.from_list(name='rainbow_alpha',colors=color_array)

    # register this new colormap with matplotlib
    plt.register_cmap(cmap=map_object)

    X, Y = np.meshgrid(binedges[0][:-1],binedges[1][:-1])
    B,Z = np.meshgrid(binedges[1][:-1],binedges[2][:-1])
    for ct in bin_count: 
        
        cs = ax1.contourf(X,Y,hist[:,:,ct], 
                        zdir='z', 
                        offset=binedges[2][ct], 
                        levels=10, 
                        cmap=plt.cm.RdYlBu_r, 
                        alpha=0.05)
    

    ax1.set_xlim(-500, 500)
    ax1.set_ylim(-500, 500)
    ax1.set_zlim(-2000, 2000)
    plt.colorbar(cs)
    #plt.colorbar(cs2)
    plt.show()
    return(None)

def we_try_again(data_frame):
    datadata = pd.DataFrame(data_frame).to_numpy()
    print(datadata)
    #This method is based off of this post:
    # https://mathematica.stackexchange.com/questions/268402/build-a-3d-heat-map-plot-from-4d-data
    #This does involvce importing the mathematica library and using it in python, so lets see what we can do...

    session = WolframLanguageSession()
    #dist = wl.SmoothKernelDistribution[Most /@ datadata])
    session.stop()
    return(None)

#scat_angle_dist(x,y,z,angle)
#scatter_map(x,y,z,angle)
#voxel_map(data)
#ct_esque(xyz,x,y,z,angle)
we_try_again(data_frame)