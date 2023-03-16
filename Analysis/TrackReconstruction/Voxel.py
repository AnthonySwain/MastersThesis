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

def voxelisation(voxel_side_length,detector_in_corners,detector_out_corners,filename,df,qual_angle):
    
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    print(angle)
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
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])[angle].mean()
    
    x_y_plane = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no))])[angle].mean()
    
    y_z_plane = df.groupby([pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])[angle].mean()
    

    x_z_plane = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])[angle].mean()
    
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

def image_heatmap_2D_x_y(filepath,qual_angle):
    
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
        
    df = pd.read_csv(filepath)
    
    df['X'] = df['X'].str.strip('(]')
    df['Y'] = df['Y'].str.strip('(]')
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))

    x_val = df.loc[:,"X"]
    y_val = df.loc[:,"Y"]
    angles = df.loc[:,angle]
    
    pivot = df.pivot(values = angle,columns='X',index='Y')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    plt.show()
    
    return(None)
def image_heatmap_2D_x_z(filepath, detector_corners,qual_angle):
    
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
        
    xticksww = np.linspace(-detector_corners[0][0],detector_corners[0][0],29)
    xticksww = np.around(xticksww,-1)
    
    zticks = np.linspace(-detector_corners[0][2],detector_corners[0][2],19)
    zticks = np.around(zticks,-1)
    
    
    
    df = pd.read_csv(filepath)
    
    #df.rename(columns={0: 'X',  1: 'Z', 2: 'angle'}, inplace=True)
    print(df)
    df['X'] = df['X'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))

    x_val = df.loc[:,"X"]
    y_val = df.loc[:,"Z"]
    angles = df.loc[:,angle]
    
    #object_outline
    #outline_x = [1000,1000,-1000,-1000]
    #outline_z = [-75,75,75,-75]
    
    
    pivot = df.pivot(values = angle,columns='X',index='Z')
    #plt.plot(outline_x, outline_z, linestyle='dashed', color='black')
    #sns.heatmap(pivot,cmap = 'Spectral_r',yticklabels = zticks, xticklabels=xticksww).axis('equal')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    #, yticklabels = zticks,
    plt.show()
    
    return(None)
def image_heatmap_2D_y_z(filepath,qual_angle):
    
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    
    
    
    df = pd.read_csv(filepath)
    

    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))

    x_val = df.loc[:,"Y"]
    y_val = df.loc[:,"Z"]
    angles = df.loc[:,angle]
    
    pivot = df.pivot(values = angle,columns='Y',index='Z')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    plt.show()
    
    return(None)
def image_heatmap_3D(filepath,detector_corners,qual_angle):
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    yticks = np.linspace(-detector_corners[0][1],detector_corners[0][1],17)
    
    df = pd.read_csv(filepath)
    print("1")
    #df.rename(columns={0: 'x',  1: 'y', 2: 'z',3: 'angle'}, inplace=True)
    
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    print("2")
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    print("3")
    
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
    
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
    
    
    
    return(None)
#image_heatmap_2D_x_y()

voxel_side_length = 25#(mm)
#filename = "/50mmSample/Lead/50000PureLeadSlab1Interaction.h5"
filename = "/SteelRodInConcrete50mmRadius/2millionevents2Interaction.h5"
#df = ReadH5.pandas_read("/08.03.2023/Steel/50000PureSteelSlab1Interaction.h5")
df2 = ReadH5.pandas_read("/SteelRodInConcrete50mmRadius/2millioneventsInteraction.h5")
df = ReadH5.pandas_read(filename)

df = pd.concat([df,df2])


qualfact = True
voxelisation(voxel_side_length,detector_in_corners,detector_out_corners,filename,df,qualfact)
image_heatmap_2D_x_z("/home/anthony/MastersThesis/Data/SteelRodInConcrete50mmRadius/2millionevents2Interactionxzplane.csv",detector_in_corners,qualfact)
image_heatmap_2D_x_y("/home/anthony/MastersThesis/Data/SteelRodInConcrete50mmRadius/2millionevents2Interactionxyplane.csv",qualfact)
image_heatmap_2D_y_z("/home/anthony/MastersThesis/Data/SteelRodInConcrete50mmRadius/2millionevents2Interactionyzplane.csv",qualfact)
image_heatmap_3D("/home/anthony/MastersThesis/Data/SteelRodInConcrete50mmRadius/2millionevents2Interaction3D.csv",detector_in_corners,qualfact)
