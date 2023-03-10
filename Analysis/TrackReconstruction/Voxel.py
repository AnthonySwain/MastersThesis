#Thank you to the kind fellows on the python discord for helping with this:) 

#Splits the data into voxels of a particulare size and assigns each voxel the average scatter angle inside

import pandas as pd
import numpy as np
import math
import ReadH5 as ReadH5
#This is all working in mm!!!!!!!!
voxel_side_length = 50
detector_in_corners = ([0.75*1000,0.6*1000,0.5*1000],
                    [0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,0.6*1000,0.5*1000])

detector_out_corners = ([0.75*1000,0.6*1000,-0.5*1000],
                    [0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,0.6*1000,-0.5*1000])

def voxelisation(voxel_side_length,detector_in_corners,detector_out_corners,df):
    #Dataframe should be in [x,y,z,angle] format:) 
    #Working out the number of voxels in each direction, given the side length:) 
    x_voxel_no = math.ceil((detector_in_corners[0][0] - detector_in_corners[2][0]) / (voxel_side_length))
    y_voxel_no = math.ceil((detector_in_corners[0][1] - detector_in_corners[2][1]) / (voxel_side_length))
    z_voxel_no = math.ceil((detector_in_corners[0][2] - detector_out_corners[0][2]) / (voxel_side_length))
    
    voxelised = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no)),
                             pd.cut(df.Z, np.linspace(detector_out_corners[0][2], detector_in_corners[0][2], z_voxel_no))])['angle'].mean()
    
    x_y_plane = df.groupby([pd.cut(df.X, np.linspace(detector_in_corners[2][0], detector_in_corners[0][0], x_voxel_no)),
                             pd.cut(df.Y, np.linspace(detector_in_corners[2][1], detector_in_corners[0][1], y_voxel_no))])['angle'].mean()
    voxelised.to_csv("vol")
    x_y_plane.to_csv("xyplane")
    return(voxelised)




df = ReadH5.pandas_read("/OutputInteraction.h5")
print(df)
voxelisation(voxel_side_length,detector_in_corners,detector_out_corners,df)

#voxelised = df.groupby([pd.cut(df.x, np.linspace(0, 1, 10)), pd.cut(df.y, np.linspace(0, 1, 10)), pd.cut(df.z, np.linspace(0, 1, 10))])['val'].mean()
#voxelised.to_csv("test.csv")
#print(voxelised)