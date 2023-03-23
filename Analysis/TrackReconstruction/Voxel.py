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
import sys

#This is all working in mm!!!!!!!!

detector_in_corners = ([0.75*1000,0.6*1000,0.5*1000],
                    [0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,0.6*1000,0.5*1000])

detector_out_corners = ([0.75*1000,0.6*1000,-0.5*1000],
                    [0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,0.6*1000,-0.5*1000])

def voxelisation(voxel_side_length,filename,df,angle_type):
    detector_in_corners = ([0.75*1000,0.6*1000,0.5*1000],
                    [0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,0.6*1000,0.5*1000])

    detector_out_corners = ([0.75*1000,0.6*1000,-0.5*1000],
                    [0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,0.6*1000,-0.5*1000])
    
    
    
    
    if angle_type == 1:
        angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "momentumweighted"
    if angle_type == 4:
        angle = "MDweighted"
        
    df = df.loc[(df.X > -750) &
                            (df.X < 750) &
                            (df.Y > -600) &
                            (df.Y < 600) &
                            (df.Z > -1000) &
                            (df.Z < 1000) &
                            #(data.angle < math.pi) &
                            (df.angle >= 0)]
    #print(df)
    #Dataframe should be in [x,y,z,angle] format:) 
    #Working out the number of voxels in each direction, given the side length:) 
    x_voxel_no = math.ceil((detector_in_corners[0][0] - detector_in_corners[2][0]) / (voxel_side_length))
    y_voxel_no = math.ceil((detector_in_corners[0][1] - detector_in_corners[2][1]) / (voxel_side_length))
    z_voxel_no = math.ceil((detector_in_corners[0][2] - detector_out_corners[0][2]) / (voxel_side_length))
    
    voxelised = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])[angle].sum()
       
    
    Vol = "/home/anthony/MastersThesis/Data" + filename[:-3] + "3D.csv"

    voxelised.to_csv(Vol)

    return(None)


def image_heatmap_3D(filepath,detector_corners,qual_angle):
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    
    
    df = pd.read_csv(filepath)
    
    #df.rename(columns={0: 'x',  1: 'y', 2: 'z',3: 'angle'}, inplace=True)
    
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    
    
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
    print(df)
    x_val = df.loc[:,"X"].to_numpy()
    y_val = df.loc[:,"Y"].to_numpy()
    z_val = df.loc[:,"Z"].to_numpy()
    angles = df.loc[:,angle].to_numpy()

    
    
    fig = go.Figure(data=go.Volume(
    x=x_val,
    y=y_val,
    z=z_val,
    value=angles,
    #isomin=0.0,
    #isomax=0.8,
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=20, # needs to be a large number for good volume rendering
    ))
    
    fig.update_layout(
        scene = dict(
           xaxis = dict(nticks=8, range=[-detector_corners[0][0],detector_corners[0][0]],),
                        yaxis = dict(nticks=8, range=[-detector_corners[0][1],detector_corners[0][1]],),
                        zaxis = dict(nticks=8, range=[-detector_corners[0][2],detector_corners[0][2]],)))
    #fig.update_layout(scene_xaxis_showticklabels=False,
    #              scene_yaxis_showticklabels=False,
    #              scene_zaxis_showticklabels=False)
    
    fig.show()
    plt.savefig(filepath[:-4]+"3D.png")
    
    
    return(None)
#image_heatmap_2D_x_y()

def heatmap_slices(filepath,angle_type):
    #Slices through the concrete in the xy plane, a bit like a CT scan.
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "momentumweighted"
    if angle_type == 4:
        angle = "MDweighted"
    
    
    df = pd.read_csv(filepath)
    
    #df.rename(columns={0: 'x',  1: 'y', 2: 'z',3: 'angle'}, inplace=True)
    
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    
    print("test")
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
    print("test2")
   
    z_val = df.loc[:,"Z"].to_numpy()
    z_val=np.unique(z_val)
    for i in z_val:
        df_plot = df.loc[(df.Z == i)]
        df_plot.drop(columns = ['Z'],inplace=True)
        print(df_plot)
        
        pivot = df_plot.pivot(values = angle,columns='X',index='Y')
        sns.heatmap(pivot,cmap = 'bwr').axis('equal')
        plt.title("Z= " +str(i)+ " mm")
        
        plt.savefig("/home/anthony/MastersThesis/Data/DumpFolder/xyZ=" +str(i)+".png")
        plt.close()
        #plt.show()
    return(None)

def binned_clustered(voxel_side_length,filename,df,qual_angle):
    detector_in_corners = ([0.75*1000,0.6*1000,0.5*1000],
                    [0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,0.6*1000,0.5*1000])

    detector_out_corners = ([0.75*1000,0.6*1000,-0.5*1000],
                    [0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,0.6*1000,-0.5*1000])
    
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    
    df = df.loc[(df.X > -750) &
                            (df.X < 750) &
                            (df.Y > -600) &
                            (df.Y < 600) &
                            (df.Z > -1000) &
                            (df.Z < 1000) &
                            #(data.angle < math.pi) &
                            (df.angle >= 0)]
    #print(df)
    #Dataframe should be in [x,y,z,angle] format:) 
    #Working out the number of voxels in each direction, given the side length:) 
    x_voxel_no = math.ceil((detector_in_corners[0][0] - detector_in_corners[2][0]) / (voxel_side_length))
    y_voxel_no = math.ceil((detector_in_corners[0][1] - detector_in_corners[2][1]) / (voxel_side_length))
    z_voxel_no = math.ceil((detector_in_corners[0][2] - detector_out_corners[0][2]) / (voxel_side_length))
    
    voxelised = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))]).apply(metric)  
    BinnedClustered = "/home/anthony/MastersThesis/Data" + filename[:-3] + "BinnedClustered.csv"
    voxelised.to_csv(BinnedClustered)
    return(None)


def metric(sub_vol_df):

    #We don't care about only 1 interaction
    if (sub_vol_df.shape[0]) <=1:
        return(0)
    
    coords = (sub_vol_df[['X','Y','Z']].to_numpy())
    angleweight = sub_vol_df[['momentumweighted']].to_numpy()
    
    angleweight_multiplied = angleweight * angleweight.T
    
    diff = coords - coords[:,np.newaxis]
    
    metric = np.linalg.norm(diff,axis=-1)
    
    weighted_metric = metric/angleweight_multiplied
    flattened = weighted_metric.flatten()
    median = np.median(flattened[flattened != 0])
    

    return(median)

voxel_side_length = 50#(mm)
#filename = "/50mmSample/Lead/50000PureLeadSlab1Interaction.h5"
#filename = "/SteelRodInConcrete50mmRadius/2millionevents2Interaction.h5"
#filename = "/ReferenceConcreteBlock/2milliInteraction.h5"
filename = "/SteelRodInConcreteMomentumBased/SteelRodInConcrete2Interaction.h5"
key = "POCA"
#df = ReadH5.pandas_read("/08.03.2023/Steel/50000PureSteelSlab1Interaction.h5")
#df2 = ReadH5.pandas_read("/SteelRodInConcrete50mmRadius/2millioneventsInteraction.h5")
df = ReadH5.pandas_read(filename,key)

#df = pd.concat([df,df2])
base_filepath = "/home/anthony/MastersThesis/Data/"

angle_type = 3
voxelisation(voxel_side_length,filename,df,angle_type)
#binned_clustered(voxel_side_length,filename,df,qualfact)
print("hi")
#image_heatmap_2D_x_z(base_filepath + filename[:-3] + "xzplane.csv",detector_in_corners,qualfact)
#image_heatmap_2D_x_y(base_filepath + filename[:-3] + "xyplane.csv",qualfact)
#image_heatmap_2D_y_z(base_filepath + filename[:-3] + "yzplane.csv",qualfact)
#image_heatmap_3D(base_filepath + filename[:-3] + "3D.csv",detector_in_corners,qualfact)
heatmap_slices(base_filepath + filename[:-3] + "3D.csv",angle_type)
