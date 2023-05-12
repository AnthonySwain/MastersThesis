#Plots scatter angle distributions from data of interactions
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
    #Cleans the data getting rid of calculated interactions outside the volume between the two sets of detectors
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
    xyz = data.drop(["angle"],axis=1)
               
    return (x,y,z,angle,xyz)


data_frame1steel = ReadH5.pandas_read("/100mmSample/Steel/SteelInteraction.h5")
data_frame1concrete = ReadH5.pandas_read("/1mmSample/Concrete/ConcreteInteraction.h5")
data_frame1lead = ReadH5.pandas_read("/1mmSample/Lead/LeadInteraction.h5")
data_frame_air = ReadH5.pandas_read("/50mmSample/Air/50000AirInteraction.h5")

data_air = data_frame_air
data_steel = data_frame1steel
data_concrete= data_frame1concrete
data_lead = data_frame1lead
#print(data_frame)
#data_frame = pd.read_csv("/home/anthony/MastersThesis/Data/04.03.2023/50000PureConcreteInteractions.csv") #opening the data file


#data = data_frame.drop(["Z"],axis=1)

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

def scat_angle_dist(angle1,angle2,angle3,angle4):
    #fig, ax = plt.subplots()
    
    #angle1 = angle1 * (10**3)
    #angle2 = angle2 * (10**3)
    #angle3 = angle3 * (10**3)
    #angle4 = angle4 * (10**3)
    

    #ax = plt.hist(angle1, bins = 2000, label = 'Steel', alpha = 0.5)
    #ax = plt.hist(angle2, bins = 2000, label = 'Concrete', alpha = 0.5)  
    #ax = plt.hist(angle3, bins = 2000, label = 'Lead',alpha = 0.5 )
    #ax = plt.hist(angle4, bins = 2000, label = 'Air',alpha = 1)
    #ax = plt.hist(angle5, bins = 20, label = 'Vacuum',alpha = 1 )
    plt.title("Scatter angle PDF, 1mm material | Sample size = 50,000")
    plt.xlabel("Scattered angle / radians")
    angle1 = pd.Series(angle1)
    angle2 = pd.Series(angle2)
    angle3 = pd.Series(angle3)
    angle4 = pd.Series(angle4)
    
    
    
    #ax = angle4.plot(kind = 'kde', label = 'Air')
    ax = angle2.plot(kind = 'kde', label = 'ConcreteBlock')
    ax = angle1.plot(kind = 'kde', label = 'SteelRod')
    #ax = angle3.plot(kind = 'kde', label = 'Lead')
    
    ax.legend()
    plt.xlim(0,math.pi/16)
    plt.ylim(0,50)
    plt.ylabel("Density")
    plt.show()

    return(None)


#clean_interaction = data_clean(data_frame)
clean_air = data_clean(data_air)
clean_concrete = data_clean(data_concrete)
clean_steel = data_clean(data_steel)
clean_lead = data_clean(data_lead)
#print(np.size(clean_no_interaction[0]))
#interaction_angle = clean_interaction[3]

air_angle = clean_air[3]
steel_angle = clean_steel[3]
concrete_angle = clean_concrete[3]
lead_angle = clean_lead[3]
#angle_diff = abs(interaction_angle - no_interaction_angle)


#df_steel_rod = ReadH5.pandas_read("/50mmRadius SteelRod/SteelRodInteraction.h5")
df_concrete_block = ReadH5.pandas_read("/ReferenceConcreteBlock/2milliInteraction.h5")

#clean_rod = data_clean(df_steel_rod)
clean_block = data_clean(df_concrete_block)

scat_angle_dist(steel_angle,clean_block[3],lead_angle,air_angle)

#scatter_map(x,y,z,angle)
#voxel_map(data)
#ct_esque(xyz,x,y,z,angle)
#we_try_again(data_frame)
#
