#Thank you to the kind fellows on the python discord for helping with this:) 

#Splits the data into voxels of a particulare size and assigns each voxel the average scatter angle inside
#Has PoCA or binned clustering algorithms implemented with optimsiations sa noted in the thesis. 
#Plots a heatmap based on value for the voxels in all xy,xz or yz planes

import pandas as pd
import numpy as np
import math
import ReadH5 as ReadH5
import seaborn as sns
import matplotlib.pyplot as plt
import math
import plotly.graph_objects as go
import sys
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from scipy import ndimage
from scipy.signal import convolve2d

import os
#This is all working in mm!!!!!!!!

detector_in_corners = ([0.6*1000,0.1125*1000,0.1125*1000],
                    [0.6*1000,-0.1125*1000,0.1125*1000],
                     [-0.6*1000,-0.1125*1000,0.1125*1000],
                     [-0.6*1000,0.1125*1000,0.1125*1000])

detector_out_corners = ([0.6*1000,0.1125*1000,-0.1125*1000],
                    [0.6*1000,-0.1125*1000,-0.1125*1000],
                     [-0.6*1000,-0.1125*1000,-0.1125*1000],
                     [-0.6*1000,0.1125*1000,-0.1125*1000])

def voxelisation(voxel_side_length,filename,df,angle_type):
    detector_in_corners = ([0.6*1000,0.1125*1000,0.1125*1000],
                    [0.6*1000,-0.1125*1000,0.1125*1000],
                     [-0.6*1000,-0.1125*1000,0.1125*1000],
                     [-0.6*1000,0.1125*1000,0.1125*1000])

    detector_out_corners = ([0.6*1000,0.1125*1000,-0.1125*1000],
                    [0.6*1000,-0.1125*1000,-0.1125*1000],
                     [-0.6*1000,-0.1125*1000,-0.1125*1000],
                     [-0.6*1000,0.1125*1000,-0.1125*1000])
        
    if angle_type == 1:
        angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "momentumweighted"
    if angle_type == 4:
        angle = "MDweighted"
        
    if angle_type == 5:
        angle = "momentumweighted"
        
    df = df.loc[(df.X > -750) &
                            (df.X < 750) &
                            (df.Y > -112.5) &
                            (df.Y < 112.5) &
                            (df.Z > -112.5) &
                            (df.Z < 112.5) &
                            #(data.angle < math.pi) &
                            (df.angle >= 0)]
    #print(df)
    #Dataframe should be in [x,y,z,angle] format:) 
    #Working out the number of voxels in each direction, given the side length:) 
    x_voxel_no = math.ceil((detector_in_corners[0][0] - detector_in_corners[2][0]) / (voxel_side_length))
    y_voxel_no = math.ceil((detector_in_corners[0][1] - detector_in_corners[2][1]) / (voxel_side_length))
    z_voxel_no = math.ceil((detector_in_corners[0][2] - detector_out_corners[0][2]) / (voxel_side_length))
    
    x_coords = np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no*4)
    y_coords = np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no*4)
    z_coords = np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no*4)
    
    
    
    
    voxelised = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])[angle].median()
       
    
    Vol = "/home/anthony/MastersThesis/Data" + filename[:-3] + "3D.csv"

    voxelised.to_csv(Vol)

    return(None)


def image_heatmap_3D(filepath,detector_corners,angle_type):
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "momentumweighted"
    if angle_type == 4:
        angle = "MDweighted"
        
    if angle_type == 5:
        angle == "momentumweighted"
    
    
    df = pd.read_csv(filepath)
    df.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z","0": angle}, inplace = True)

    #df.rename(columns={0: 'x',  1: 'y', 2: 'z',3: 'angle'}, inplace=True)
    
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0.00001)
    df[angle] = df[angle].abs()
    
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
    #print(df)
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
    surface_count=5, # needs to be a large number for good volume rendering
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

def heatmap_slices_zx(filepath,angle_type,neighbour_average,filter_confidence,directory):
    #Slices through the concrete in the xy plane, a bit like a CT scan.
    #Neighbour average, bool, specifies whether to perform a nearest neighbour average of voxels
    #Filter confidence, any values less than this in the neighbour average will be set to 0
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "0"
    if angle_type == 4:
        angle = "MDweighted"
        
    if angle_type == 5:
        angle = "momentumweighted"
    
    
    df = pd.read_csv(filepath)
    df.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z","0": angle}, inplace = True)
    #df.rename(columns={0: 'X',  1: 'Y', 2: 'Z',3: angle}, inplace=True)
    
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    df[angle] = df[angle].abs()
    
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
       
    y_val = df.loc[:,"Y"].to_numpy()
    y_val=np.unique(y_val)
    for i in y_val:
        df_plot = df.loc[(df.Y == i)]
        df_plot.drop(columns = ['Y'],inplace=True)
                
        pivot = df_plot.pivot(values = angle,columns='X',index='Z')
        
        if neighbour_average == True:
            values = pivot.to_numpy()
            result = eight_neighbor_average_convolve2d(values)
            
            result1d = result.flatten('F')
            normalised = normalise(result1d)
            
            #Any values less than filter value are set to 0 
            #normalised[normalised < filter_confidence] = 0
            
            df_plot[angle] = normalised
            pivot = df_plot.pivot(values = angle,columns='Z',index='X')
        
        sns.heatmap(pivot,cmap = 'Spectral_r',xticklabels=7, yticklabels=6).axis('equal')
        plt.title("Y= " +str(i)+ " mm")
        plt.xlabel("Z / mm")
        plt.ylabel("X / mm")
        plt.autoscale()
        
        plt.savefig(directory+ "/zx_Y=" +str(i)+".png",bbox_inches='tight')
        plt.close()
        #plt.show()
    return(None)

def heatmap_slices_zy(filepath,angle_type,neighbour_average,filter_confidence,directory):
    #Slices through the concrete in the xy plane, a bit like a CT scan.
    #Neighbour average, bool, specifies whether to perform a nearest neighbour average of voxels
    #Filter confidence, any values less than this in the neighbour average will be set to 0
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "0"
    if angle_type == 4:
        angle = "MDweighted"
    
    if angle_type == 5:
        angle = "momentumweighted"
    
    
    df = pd.read_csv(filepath)
    df.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z","0": angle}, inplace = True)
    #df.rename(columns={0: 'X',  1: 'Y', 2: 'Z',3: angle}, inplace=True)
    
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    df[angle] = df[angle].abs()
    
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
       
    x_val = df.loc[:,"X"].to_numpy()
    x_val=np.unique(x_val)
    for i in x_val:
        df_plot = df.loc[(df.X == i)]
        df_plot.drop(columns = ['X'],inplace=True)
                
        pivot = df_plot.pivot(values = angle,columns='Z',index='Y')
        
        if neighbour_average == True:
            values = pivot.to_numpy()
            result = eight_neighbor_average_convolve2d(values)
            
            result1d = result.flatten('F')
            normalised = normalise(result1d)
            
            #Any values less than 0.5 are set to 0 
            #normalised[normalised < filter_confidence] = 0
            
            df_plot[angle] = normalised
            pivot = df_plot.pivot(values = angle,columns='Z',index='Y')
        
        sns.heatmap(pivot,cmap = 'Spectral_r',xticklabels=2, yticklabels=2).axis('equal')
        plt.title("X= " +str(i)+ " mm")
        plt.xlabel("Z / mm")
        plt.ylabel("Y / mm")
        plt.autoscale()
        plt.savefig(directory+ "/zy_X=" +str(i)+".png",bbox_inches='tight')
        plt.close()
        #plt.show()
    return(None)

def heatmap_slices_xy(filepath,angle_type,neighbour_average,filter_confidence,directory):
    #Slices through the concrete in the xy plane, a bit like a CT scan.
    #Neighbour average, bool, specifies whether to perform a nearest neighbour average of voxels
    #Filter confidence, any values less than this in the neighbour average will be set to 0
    
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "0"
    if angle_type == 4:
        angle = "MDweighted"
        
    if angle_type == 5:
        angle = "momentumweighted"
    
    
    df = pd.read_csv(filepath)
    
    df.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z","0": angle}, inplace = True)
    #df.rename(columns={0: 'X',  1: 'Y', 2: 'Z',3: angle}, inplace=True)
    #print(df)
    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df['X'] = df['X'].str.strip('(]')
    
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    df[angle] = df[angle].abs()
    
    for index, row in df.iterrows():
        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))
    
       
    z_val = df.loc[:,"Z"].to_numpy()
    z_val=np.unique(z_val)
    for i in z_val:
        df_plot = df.loc[(df.Z == i)]
        df_plot.drop(columns = ['Z'],inplace=True)
                
        pivot = df_plot.pivot(values = angle,columns='X',index='Y')
        
        if neighbour_average == True:
            values = pivot.to_numpy()
            result = eight_neighbor_average_convolve2d(values)
            
            result1d = result.flatten('F')
            normalised = normalise(result1d)
            
            #Any values less than 0.5 are set to 0 
            normalised[normalised < filter_confidence] = 0
            
            df_plot[angle] = normalised
            pivot = df_plot.pivot(values = angle,columns='X',index='Y')
        
       
        fig, ax = plt.subplots(figsize = (12, 4))
        sns.heatmap(pivot,cmap = 'Spectral_r',xticklabels=4, yticklabels=4, square = True)
        #sns.jointplot(x=df['X'], y=df['X'], data=df[angle] , height = 10 , kind="hist" ,color="#FF6600" , marginal_kws={'lw':5})
        plt.title("Z= " +str(i)+ " mm")
        
        plt.xlabel("X / mm")
        plt.ylabel("Y / mm")
        plt.autoscale()
        plt.savefig(directory + "/xy_Z=" +str(i)+".png",bbox_inches='tight')
        plt.close()
        
        #plt.show()
    return(None)

def binned_clustered(voxel_side_length,filename,df,angle_type):
    detector_in_corners = ([0.5*1000,0.1125*1000,0.1125*1000],
                    [0.5*1000,-0.1125*1000,0.1125*1000],
                     [-0.5*1000,-0.1125*1000,0.1125*1000],
                     [-0.5*1000,0.1125*1000,0.1125*1000])

    detector_out_corners = ([0.5*1000,0.1125*1000,-0.1125*1000],
                    [0.5*1000,-0.1125*1000,-0.1125*1000],
                     [-0.5*1000,-0.1125*1000,-0.1125*1000],
                     [-0.5*1000,0.1125*1000,-0.1125*1000])
    
    if angle_type == 1:
        angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "momentumweighted"
    if angle_type == 4:
        angle = "MDweighted"
        
    if angle_type == 5:
        angle = "momentumweighted"
    
    df = df.loc[(df.X > -500) &
                            (df.X < 500) &
                            (df.Y > -112.5) &
                            (df.Y < 112.5) &
                            (df.Z > -112.5) &
                            (df.Z < 112.5) &
                            #(data.angle < math.pi) &
                            (df.angle >= 0)]
    #print(df)
    #print(df)
    #Dataframe should be in [x,y,z,angle] format:) 
    #Working out the number of voxels in each direction, given the side length:) 
   
    x_voxel_no = math.ceil((detector_in_corners[0][0] - detector_in_corners[2][0]) / (voxel_side_length))
    y_voxel_no = math.ceil((detector_in_corners[0][1] - detector_in_corners[2][1]) / (voxel_side_length))
    z_voxel_no = math.ceil((detector_in_corners[0][2] - detector_out_corners[0][2]) / (voxel_side_length))
    
    xticks = pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no))
    yticks = pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no))
    zticks = pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))
    
    
    #x_coords = np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)
    #y_coords = np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)
    #z_coords = np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no)
    
   # for i in x_coords:
   #     for j in y_coords:
   #         for k in z_coords:
   #             df.loc[len(df)] = [0,i,j,k,0,0,0,0]
                #df.loc[len(df)] = [0,i*1.0001,j*1.0001,k*1.001,0,0,0,0]
                
    #print(x_voxel_no, "xvox")
    #print(y_voxel_no, "yvox")
    #print(z_voxel_no, "zvox")
    voxelised = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))]).apply(metric)  
    
    
    voxelised = voxelised.reindex(pd.MultiIndex.from_product([xticks.cat.categories, yticks.cat.categories, zticks.cat.categories])).fillna(0)
    voxelised.rename(index={0: "X", 1: "Y", 2: "Z", 3: "0"}, inplace = True)
    #print(voxelised)
    
    
    BinnedClustered = "/home/anthony/MastersThesis/Data" + filename[:-3] + "BinnedClustered.csv"
    voxelised.to_csv(BinnedClustered)
    return(None)

def metric(sub_vol_df):
    #Metric Used in Binned Clustering Algorithm
    #We don't care about only 1 interaction
    if (sub_vol_df.shape[0]) <=2:
        return(0)
    
    else:
        coords = (sub_vol_df[['X','Y','Z']].to_numpy())
        angleweight = sub_vol_df[['momentumweighted']].to_numpy()
        
        angleweight_multiplied = angleweight * angleweight.T
        
        diff = coords - coords[:,np.newaxis]
        
        metric = np.linalg.norm(diff,axis=-1)
        
        weighted_metric = metric/angleweight_multiplied
        flattened = weighted_metric.flatten()
        median = np.median(flattened[flattened != 0])
        

        return(1/median)

def eight_neighbor_average_convolve2d(x):
    #https://gis.stackexchange.com/questions/254753/calculate-the-average-of-neighbor-pixels-for-raster-edge
    #Function to average the values of nearest pixels
    kernel = np.ones((3, 3))
    #kernel[1, 1] = 0

    neighbor_sum = convolve2d(
        x, kernel, mode='same',
        boundary='fill', fillvalue=0)

    num_neighbor = convolve2d(
        np.ones(x.shape), kernel, mode='same',
        boundary='fill', fillvalue=0)

    return neighbor_sum / num_neighbor

def normalise(data):
    #Normalises array to go between 0 and 1
    normalised_data = (data-np.min(data))/(np.max(data)-np.min(data))
    
    return(normalised_data)

#neighbour_average = [True,False]
#binned_clustered_algo = True
#angle_type = 3
key = "POCA"

#base_data_directory = "/home/anthony/MastersThesis/Data/"
#ParentFolderPath = "/home/anthony/MastersThesis/Figures/MassOutput/NoConfidenceValues"
#interaction_name = ["RealisticConcreteBeam15mmRadius","RealisticConcreteBeam10mmRadius","RealisticConcreteBeam5mmRadius","Disconnected10cmGap","RustedBeam15mm"]
#interaction_name = ["Disconnected10cmGap","RustedBeam15mm"]

def make_heatmaps(base_data_directory,interaction_name,VoxelSize,STDcheck,filter,binned_clustered_algo,angle_type,key,ParentFolderPath):
    #Makes the figures on mass
    #ParentFolderPath is where the output files will go 
    try: 
        os.mkdir(ParentFolderPath) 
    except OSError as error: 
        print(ParentFolderPath)
        
    ParticleDetectorUncertantity = ["ExactPrecision","Gaussian","TopHat"]
    
    for i in interaction_name:
        try: 
            os.mkdir(ParentFolderPath + "/" + i) 
        except OSError as error: 
            print(error)
            
        for j in ParticleDetectorUncertantity:
            data_dir = base_data_directory + i + "/" + j + "/"
            print(j)
            if j == "Gaussian" or j == "TopHat":
                df1 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "InteractionUncertantity.h5",key)
                df2 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "2InteractionUncertantity.h5",key)
                df3 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "3InteractionUncertantity.h5",key)
                df4 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "4InteractionUncertantity.h5",key)
                imagingfilename = "/" + i + "/" + j + "/" + i + "InteractionUncertantity.h5"
                imaging = pd.concat([df1,df2,df3,df4])
            
            else:
                df1 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "Interaction.h5",key)
                df2 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "2Interaction.h5",key)
                df3 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "3Interaction.h5",key)
                df4 = ReadH5.pandas_read("/" + i + "/" + j + "/" + i + "4Interaction.h5",key)
                imagingfilename = "/" + i + "/" + j + "/" + i + "Interaction.h5"
                imaging = pd.concat([df1,df2,df3,df4])
            
            
            binned_clustered(VoxelSize,imagingfilename,imaging,angle_type) 
            try: 
                os.mkdir(ParentFolderPath + "/" + i + "/" + j) 
            except OSError as error: 
                print(error)


            for l in neighbour_average:
                if l == True:
                    neighbour_path = "NeighbourAverage"           
                else: 
                    neighbour_path = "NotNeighbourAverage"
                    
                try:
                    os.mkdir(ParentFolderPath + "/" + i + "/" + j + "/" + neighbour_path)
                    print("done")
                except OSError as error: 
                    print(error)
                    
                Directory_slicesXY = ParentFolderPath + "/" + i + "/" + j + "/" + neighbour_path +"/XYHeatMapSlices"
                Directory_slicesZX = ParentFolderPath + "/" + i + "/" + j + "/" + neighbour_path +"/ZXHeatMapSlices"
                Directory_slicesZY = ParentFolderPath + "/" + i + "/" + j + "/"+ neighbour_path +"/ZYHeatMapSlices"
                
                try: 
                    os.mkdir(Directory_slicesXY) 
                except OSError as error: 
                    print(error)
                    
                try: 
                    os.mkdir(Directory_slicesZX) 
                except OSError as error: 
                    print(error)
                    
                try: 
                    os.mkdir(Directory_slicesZY) 
                except OSError as error: 
                    print(error)
                base_filepath = "/home/anthony/MastersThesis/Data"
                heatmap_slices_xy(base_filepath + imagingfilename[:-3] + "BinnedClustered.csv",angle_type,l,0,Directory_slicesXY)
                heatmap_slices_zy(base_filepath + imagingfilename[:-3] + "BinnedClustered.csv",angle_type,l,0,Directory_slicesZY)
                heatmap_slices_zx(base_filepath + imagingfilename[:-3] + "BinnedClustered.csv",angle_type,l,0,Directory_slicesZX)
    return(None)

#make_heatmaps(base_data_directory,interaction_name,15,5,0,binned_clustered,angle_type,key,ParentFolderPath)





def just_rebar_imaging():
    #Also to make figures on mass (but of just the rebar - im pretty sure this is the same as the make heatmaps function..)
    df1 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadiusInteraction.h5",key)
    df2 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadius2Interaction.h5",key)
    df3 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadius3Interaction.h5",key)
    df4 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadius4Interaction.h5",key)
    imagingfilename = "/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadiusInteraction.h5"
    
    df1 = pd.concat([df1,df2,df3,df4])
    

    #imagingfilename = "/NOCONCRETEREBAR/JustRebar15mmRadius1milliInteraction.h5"

    base_filepath = "/home/anthony/MastersThesis/Data/"
            
    angle_type = [1,2,5,4]

    directory = "/home/anthony/MastersThesis/Figures/ConcreteANDRebar"
    try: 
        os.mkdir(directory) 
    except OSError as error: 
        print(error)
        
    for i in angle_type:
        voxelisation(15,imagingfilename,df1,i) 
        save_directory = "/home/anthony/MastersThesis/Figures/ConcreteANDRebar/15mmVoxelMedian"
        try: 
            os.mkdir(save_directory) 
        except OSError as error: 
            print(error)
        
        save_directory_angle = save_directory + "/" + str(i)
        
        try: 
            os.mkdir(save_directory_angle) 
        except OSError as error: 
            print(error)
        
        for j in [True,False]:
            
            if j == True:
                neighbour_path = "/NeighbourAverage"           
            else: 
                neighbour_path = "/NotNeighbourAverage"
                
            try: 
                os.mkdir(save_directory_angle + neighbour_path) 
            except OSError as error: 
                print(error)
            Directory_slicesXY = save_directory_angle + neighbour_path + "/XYHeatMapSlices"
            Directory_slicesZX = save_directory_angle + neighbour_path + "/ZXHeatMapSlices"
            Directory_slicesZY = save_directory_angle + neighbour_path + "/ZYHeatMapSlices"
            
            try: 
                os.mkdir(Directory_slicesXY) 
            except OSError as error: 
                print(error)
                
            try: 
                os.mkdir(Directory_slicesZX) 
            except OSError as error: 
                print(error)
                
            try: 
                os.mkdir(Directory_slicesZY) 
            except OSError as error: 
                print(error)
                
            heatmap_slices_xy(base_filepath + imagingfilename[:-3] + "3D.csv",i,j,0,Directory_slicesXY)
            heatmap_slices_zy(base_filepath + imagingfilename[:-3] + "3D.csv",i,j,0,Directory_slicesZY)
            heatmap_slices_zx(base_filepath + imagingfilename[:-3] + "3D.csv",i,j,0,Directory_slicesZX)
    return(None)

just_rebar_imaging()