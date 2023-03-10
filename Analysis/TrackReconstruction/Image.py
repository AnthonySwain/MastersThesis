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
import math
import ReadH5 as ReadH5
#from wolframclient.evaluation import WolframLanguageSession
#from wolframclient.language import wl, wlexpr
def data_clean(data):
    data = data[["X","Y","Z","angle"]]
    data = data.loc[(data.X > -750) &
                            (data.X < 750) &
                            (data.Y > -600) &
                            (data.Y < 600) &
                            (data.Z > -1000) &
                            (data.Z < 1000) &
                            #(data.angle < math.pi) &
                            (data.angle >= 0)]

    angle = data["angle"].values
    x = data["X"].values
    y = data["Y"].values  
    z = data["Z"].values
               
    return (x,y,z,angle)


data_frame1steel = ReadH5.pandas_read("/08.03.2023/Steel/50000PureSteelSlab2Interaction.h5")
data_frame2steel = ReadH5.pandas_read("/08.03.2023/Steel/50000PureSteelSlab1Interaction.h5")
data_frame1concrete = ReadH5.pandas_read("/08.03.2023/Concrete/50000PureConcreteSlab1Interaction.h5")
data_frame2concrete = ReadH5.pandas_read("/08.03.2023/Concrete/50000PureConcreteSlab1Interaction.h5")
data_frame1lead = ReadH5.pandas_read("/08.03.2023/Lead/50000PureLeadSlab1Interaction.h5")
data_frame2lead = ReadH5.pandas_read("/08.03.2023/Lead/50000PureLeadSlab2Interaction.h5")

data_vacuum= data_clean(ReadH5.pandas_read("/08.03.2023/Lead/50000PureLeadSlab2Interaction.h5"))

data_frame_air = ReadH5.pandas_read("/08.03.2023/Air/50000AirInteraction.h5")


data_frame_air2 = ReadH5.pandas_read("/08.03.2023/Air/50000Air2Interaction.h5")

data_air = pd.concat([data_frame_air,data_frame_air2])
data_steel = pd.concat([data_frame1steel,data_frame2steel])
data_concrete= pd.concat([data_frame1concrete,data_frame2concrete])
data_lead = pd.concat([data_frame1lead,data_frame2lead  ])
#print(data_frame)
#data_frame = pd.read_csv("/home/anthony/MastersThesis/Data/04.03.2023/50000PureConcreteInteractions.csv") #opening the data file


#data = data_frame.drop(["Z"],axis=1)
#xyz = data_frame.drop(["angle"],axis=1)
#data = data.loc[data['X'] <= 1000]
#data = data.loc[data['Y'] <= 1000]
#data = data.loc[data['X'] >= -1000]
#data = data.loc[data['Y'] >= -1000]



def scatter_map(x,y,z,angle):
    # creating figures
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_xlim(-500, 500)
    ax1.set_ylim(-500, 500)
    ax1.set_zlim(-2000, 2000)
    ax1.scatter(x,y,z, s=angle*10)#,c=angle,cmap='Greens_r')
    plt.show()

    return(None)

def scat_angle_dist(angle1,angle2,angle3,angle4,angle5):
    fig, ax = plt.subplots()
    
    angle1 = angle1 * (10**3)
    angle2 = angle2 * (10**3)
    angle3 = angle3 * (10**3)
    angle4 = angle4 * (10**3)
    

    #ax = plt.hist(angle1, bins = 2000, label = 'Steel', alpha = 0.5)
    #ax = plt.hist(angle2, bins = 2000, label = 'Concrete', alpha = 0.5)  
    #ax = plt.hist(angle3, bins = 2000, label = 'Lead',alpha = 0.5 )
    #ax = plt.hist(angle4, bins = 2000, label = 'Air',alpha = 1)
    ax = plt.hist(angle5, bins = 20, label = 'Vacuum',alpha = 1 )
    plt.title("Scatter angle PDF, 50mm material | Sample size = 100,000")
    plt.xlabel("Scattered angle [mrad]")
    angle1 = pd.Series(angle1)
    angle2 = pd.Series(angle2)
    angle3 = pd.Series(angle3)
    angle4 = pd.Series(angle4)
    angle5 = pd.Series(angle5)
    
    
    #ax = angle4.plot(kind = 'kde', label = 'Air')
    #ax = angle2.plot(kind = 'kde', label = 'Concrete')
    #ax = angle1.plot(kind = 'kde', label = 'Steel')
    #ax = angle3.plot(kind = 'kde', label = 'Lead')
    
    #ax.legend()
    plt.xlim(-2,math.pi/64 * 10**3)
    plt.ylim(0,10000)
    plt.ylabel("Density")
    plt.show()

    return(None)

def voxel_map(data):
    sns.set()
    
    data = data.pivot(index = 'x',columns = "y",values = "angle")
    ax = sns.heatmap(data)
    
    plt.show()
    return(None)

def ct_esque(xyz,x,y,z,angle):
    xyz=pd.DataFrame(xyz).to_numpy()

    no_bins = 10
    hist, binedges = np.histogramdd(xyz, weights = angle, normed=False, bins = no_bins)
    print(np.shape(binedges))

    
    fig = plt.figure(figsize=(4, 10))
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
    #B,Z = np.meshgrid(binedges[1][:-1],binedges[2][:-1])
    for ct in bin_count: 
        
        cs = ax1.contourf(X,Y,hist[:,:,ct], 
                        zdir='z', 
                        offset=binedges[2][ct], 
                        levels=10, 
                        cmap=plt.cm.RdYlBu_r, 
                        alpha=0.05)
        
        #cs2 = ax1.contourf(X,Y,hist[:,:,ct], 
         #               zdir='z', 
          #              offset=binedges[2][ct], 
           #             levels=10, 
            #            cmap=plt.cm.RdYlBu_r, 
             #           alpha=0.05)
        
    ax1.set_aspect('equal')

    ax1.set_xlim(-500, 500)
    ax1.set_ylim(-500, 500)
    ax1.set_zlim(-2000, 2000)
    plt.colorbar(cs)
    #plt.colorbar(cs2)
    plt.show()
    return(None)



#clean_interaction = data_clean(data_frame)
clean_air = data_clean(data_air)
clean_concrete = data_clean(data_concrete)
clean_steel = data_clean(data_steel)
clean_lead = data_clean(data_lead)
#print(np.size(clean_no_interaction[0]))
#interaction_angle = clean_interaction[3]
vacuum_angle = data_vacuum[3]
air_angle = clean_air[3]
steel_angle = clean_steel[3]
concrete_angle = clean_concrete[3]
lead_angle = clean_lead[3]
#angle_diff = abs(interaction_angle - no_interaction_angle)


scat_angle_dist(steel_angle,concrete_angle,lead_angle,air_angle,vacuum_angle)

#scatter_map(x,y,z,angle)
#voxel_map(data)
#ct_esque(xyz,x,y,z,angle)
#we_try_again(data_frame)
#
