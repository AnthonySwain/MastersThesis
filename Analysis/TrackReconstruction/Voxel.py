#Thank you to the kind fellows on the python discord for helping with this:) 

#Splits the data into voxels of a particulare size and assigns each voxel the average scatter angle inside
#Plots a heatmap based on value for the voxels in all xy,xz or yz planes

import pandas as pd
import numpy as np
import math
import ReadH5 as ReadH5
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#This is all working in mm!!!!!!!!

detector_in_corners = ([0.75*1000,0.6*1000,0.5*1000],
                    [0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,0.6*1000,0.5*1000])

detector_out_corners = ([0.75*1000,0.6*1000,-0.5*1000],
                    [0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,0.6*1000,-0.5*1000])

def voxelisation(voxel_side_length,detector_in_corners,detector_out_corners,filename):
    df = ReadH5.pandas_read(filename)
    #Dataframe should be in [x,y,z,angle] format:) 
    #Working out the number of voxels in each direction, given the side length:) 
    x_voxel_no = math.ceil((detector_in_corners[0][0] - detector_in_corners[2][0]) / (voxel_side_length))
    y_voxel_no = math.ceil((detector_in_corners[0][1] - detector_in_corners[2][1]) / (voxel_side_length))
    z_voxel_no = math.ceil((detector_in_corners[0][2] - detector_out_corners[0][2]) / (voxel_side_length))
    
    voxelised = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])['angle'].mean()
    #print(voxelised)
    x_y_plane = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no))])['angle'].mean()
    
    y_z_plane = df.groupby([pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])['angle'].mean()
    

    x_z_plane = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])['angle'].mean()
    
    #print(x_y_plane[0])
    #sns.heatmap(x_y_plane)
    Vol = "/home/anthony/MastersThesis/Data" + filename[:-3] + "3D.csv"
    xyplane = "/home/anthony/MastersThesis/Data" + filename[:-3] + "xyplane.csv"
    xzplane = "/home/anthony/MastersThesis/Data" + filename[:-3] + "xzplane.csv"
    yzplane = "/home/anthony/MastersThesis/Data" + filename[:-3] + "yzplane.csv"

    voxelised.to_csv(Vol)
    x_y_plane.to_csv(xyplane)
    x_z_plane.to_csv(xzplane)
    y_z_plane.to_csv(yzplane)

    return(None)

def image_heatmap_2D_x_y(filepath):
    df = pd.read_csv(filepath)

    df['x'] = df['x'].str.strip('(]')
    df['y'] = df['y'].str.strip('(]')
    df['angle'] = df['angle'].astype(float)
    df['angle'] = df['angle'].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"x"] = math.ceil(np.average(np.fromstring(df.loc[index,"x"],sep=",")))
        df.loc[index,"y"] = math.ceil(np.average(np.fromstring(df.loc[index,"y"],sep=",")))

    x_val = df.loc[:,"x"]
    y_val = df.loc[:,"y"]
    angles = df.loc[:,"angle"]
    
    pivot = df.pivot(values = 'angle',columns='x',index='y')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    plt.show()
    
    return(None)
def image_heatmap_2D_x_z(filepath):
    df = pd.read_csv(filepath)

    df['x'] = df['x'].str.strip('(]')
    df['z'] = df['z'].str.strip('(]')
    df['angle'] = df['angle'].astype(float)
    df['angle'] = df['angle'].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"x"] = math.ceil(np.average(np.fromstring(df.loc[index,"x"],sep=",")))
        df.loc[index,"z"] = math.ceil(np.average(np.fromstring(df.loc[index,"z"],sep=",")))

    x_val = df.loc[:,"x"]
    y_val = df.loc[:,"z"]
    angles = df.loc[:,"angle"]
    
    pivot = df.pivot(values = 'angle',columns='x',index='z')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    plt.show()
    
    return(None)
def image_heatmap_2D_y_z(filepath):
    df = pd.read_csv(filepath)

    df['y'] = df['y'].str.strip('(]')
    df['z'] = df['z'].str.strip('(]')
    df['angle'] = df['angle'].astype(float)
    df['angle'] = df['angle'].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"y"] = math.ceil(np.average(np.fromstring(df.loc[index,"y"],sep=",")))
        df.loc[index,"z"] = math.ceil(np.average(np.fromstring(df.loc[index,"z"],sep=",")))

    x_val = df.loc[:,"y"]
    y_val = df.loc[:,"z"]
    angles = df.loc[:,"angle"]
    
    pivot = df.pivot(values = 'angle',columns='y',index='z')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    plt.show()
    
    return(None)

def image_heatmap_3D(filepath):
    df = pd.read_csv(filepath)
    print("hey")
    df['y'] = df['y'].str.strip('(]')
    df['z'] = df['z'].str.strip('(]')
    df['x'] = df['x'].str.strip('(]')
    df['angle'] = df['angle'].astype(float)
    #df['angle'] = df['angle'].fillna(0)
    for index, row in df.iterrows():
        df.loc[index,"x"] = math.ceil(np.average(np.fromstring(df.loc[index,"x"],sep=",")))
        df.loc[index,"y"] = math.ceil(np.average(np.fromstring(df.loc[index,"y"],sep=",")))
        df.loc[index,"z"] = math.ceil(np.average(np.fromstring(df.loc[index,"z"],sep=",")))
        
    x_val = df.loc[:,"x"].to_numpy()
    y_val = df.loc[:,"y"].to_numpy()
    z_val = df.loc[:,"z"].to_numpy()
    angles = df.loc[:,"angle"].to_numpy()

    print("hi")
    fig = go.Figure(data=go.Volume(
    x=x_val.flatten(),
    y=y_val.flatten(),
    z=z_val.flatten(),
    value=angles.flatten(),
    isomin=0.1,
    isomax=0.8,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=5, # needs to be a large number for good volume rendering
    ))
    fig.show()
    
    
    
    return(None)
#image_heatmap_2D_x_y()
voxel_side_length = 10
filename = "/SteelSlab/SteelInteraction.h5"
#voxelisation(voxel_side_length,detector_in_corners,detector_out_corners,filename)
#image_heatmap_2D_x_z("/home/anthony/MastersThesis/Data/SteelSlab/SteelInteractionxzplane.csv")
#image_heatmap_2D_x_y("/home/anthony/MastersThesis/Data/SteelSlab/SteelInteractionxyplane.csv")
image_heatmap_3D("/home/anthony/MastersThesis/Data/SteelSlab/SteelInteraction3D.csv")
#voxelised = df.Sgroupby([pd.cut(df.x, np.linspace(0, 1, 10)), pd.cut(df.y, np.linspace(0, 1, 10)), pd.cut(df.z, np.linspace(0, 1, 10))])['val'].mean()
#voxelised.to_csv("test.csv")
#print(voxelised)