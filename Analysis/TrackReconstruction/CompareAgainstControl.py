#This takes away the values from the control piece of concrete (with no steel) and the concrete with steel in
#Couple things - need to make sure the voxel sizes are the same - could just create voxel arrays in here by calling voxel.py
#Confidence intervals is something I really want to put into the code

import numpy as np
import Voxel as Voxel
import pandas as pd
import statistics
import scipy.stats
import ReadH5 as ReadH5
from scipy.stats import halfnorm
import os

#Note this is filepaths:))
detector_in_corners = ([0.6*1000,0.1125*1000,0.1125*1000],
                    [0.6*1000,-0.1125*1000,0.1125*1000],
                     [-0.6*1000,-0.1125*1000,0.1125*1000],
                     [-0.6*1000,0.1125*1000,0.1125*1000])

detector_out_corners = ([0.6*1000,0.1125*1000,-0.1125*1000],
                    [0.6*1000,-0.1125*1000,-0.1125*1000],
                     [-0.6*1000,-0.1125*1000,-0.1125*1000],
                     [-0.6*1000,0.1125*1000,-0.1125*1000])



def confidence_values(control1df,control1filename, #First Control dataframe and filepath
                      control2df,control2filename, #Second Control dataframe and filepath
                      imaging,imagingfilename, #Imaging dataframe and filepath (i.e concrete with steel inside)
                      angle_type,binned_clustered, #Type of algorithm to use and what weighting
                      no_stdev,filter_confidence, #How many standard deviations of confidence and the filter level
                      voxel_side_length):  #Sidelength of voxels
              
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "0"

    if binned_clustered == True:
        Voxel.binned_clustered(voxel_side_length,control1filename,control1df,angle_type)
        Voxel.binned_clustered(voxel_side_length,control2filename,control2df,angle_type)
        Voxel.binned_clustered(voxel_side_length,imagingfilename,imaging,angle_type)
        ending = "BinnedClustered.csv"
        
    
    if binned_clustered == False:
        Voxel.voxelisation(voxel_side_length,control1filename,control1df,angle_type)
        Voxel.voxelisation(voxel_side_length,control2filename,control2df,angle_type)
        Voxel.voxelisation(voxel_side_length,imagingfilename,imaging,angle_type)
        ending = "3D.csv"
   
    base_file_path = "/home/anthony/MastersThesis/Data/"
    
    control1dfvoxel = pd.read_csv(base_file_path + control1filename[:-3] + ending)
    
    control2dfvoxel = pd.read_csv(base_file_path + control2filename[:-3] + ending)
    
    imagingvoxel = pd.read_csv(base_file_path + imagingfilename[:-3] + ending) 
    
        
    if binned_clustered == True:
        control1dfvoxel.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z", 3: "0"}, inplace = True)
        control2dfvoxel.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z", 3: "0"}, inplace = True)
        imagingvoxel.rename(columns={"Unnamed: 0": "X", "Unnamed: 1": "Y", "Unnamed: 2": "Z", 3: "0"}, inplace = True)
        
    control1dfvoxel[angle] = control1dfvoxel[angle].astype(float)
    control1dfvoxel[angle] = control1dfvoxel[angle].fillna(0)
    
    
      
    control2dfvoxel[angle] = control2dfvoxel[angle].astype(float)
    control2dfvoxel[angle] = control2dfvoxel[angle].fillna(0)
    
    
    imagingvoxel[angle] = imagingvoxel[angle].astype(float)
    imagingvoxel[angle] = imagingvoxel[angle].fillna(0)
    
    
    #Setting the base dataframes
    difference_control = control1dfvoxel
    mean = control1dfvoxel
    difference = control1dfvoxel
    
    difference_control[angle] = control1dfvoxel[angle] - control2dfvoxel[angle]
    mean[angle] = (control1dfvoxel[angle] + control2dfvoxel[angle])/2
    difference = imagingvoxel[angle] - mean[angle]
    
    
    #Noise calculated between the 2 control concrete dataframes
    difference_angles = (difference_control[angle].to_numpy())
    difference_angles = difference_angles[difference_angles != 0]
    
    
    angle_stdev = statistics.stdev(np.absolute(difference_angles))
    
    
    angle_confidence = (scipy.stats.norm(0,no_stdev*angle_stdev).cdf(np.absolute(difference)) - 0.5)*2
    #angle_confidence[angle_confidence < filter_confidence] = 0
    
    
    confidence = control1dfvoxel
    confidence[angle] = angle_confidence
    
    filepath = base_file_path + imagingfilename[:-3] + "Confidence.csv"
    confidence.to_csv(filepath)
    
    return(None)


def compare_control(control_filepath,object_imaging_filepath,angle_type,voxel_side_length):
    #Outdated
    control_df1 = ReadH5.pandas_read(control_filepath)
    control_df2 = ReadH5.pandas_read("/ReferenceConcreteBlock/2milli2Interaction.h5")
    imaging_df1 = ReadH5.pandas_read(object_imaging_filepath)
    imaging_df2 = ReadH5.pandas_read("/SteelRodInConcrete50mmRadius/2millioneventsInteraction.h5")
    
    imaging_df = pd.concat([imaging_df1,imaging_df2])
    control_df = pd.concat([control_df1,control_df2])
    
    #A good coder would make sure the dataframes match and exit out if they don't
    Voxel.voxelisation(voxel_side_length,control_filepath,control_df,angle_type)
    Voxel.voxelisation(voxel_side_length,object_imaging_filepath,imaging_df,angle_type)
    #Just some data cleaning ready to take the values away from eachother
    
    if angle_type == 1:
       angle = "angle"
    
    if angle_type == 2:
        angle= "qualfactorangle"
    
    if angle_type == 3:
        angle = "0"
    if angle_type == 4:
        angle = "MDweighted"
    
    base_file_path = "/home/anthony/MastersThesis/Data"
    
    ctrl3D = pd.read_csv(base_file_path + control_filepath[:-3] + "3D.csv")
    
    img3D = pd.read_csv(base_file_path + object_imaging_filepath[:-3] + "3D.csv")

    #for i in [ctrl3D,ctrlXY,ctrlYZ,ctrlXZ,img3D,imgXY,imgYZ,imgXZ]:    
    
    ctrl3D[angle] = ctrl3D[angle].astype(float)
    ctrl3D[angle] = ctrl3D[angle].fillna(0)
    
    img3D[angle] = img3D[angle].astype(float)
    img3D[angle] = img3D[angle].fillna(0)

        
    #Setting the base dataframe
    difference3D = img3D 

   
    #Replacing angle with the difference
    difference3D[angle] = (img3D[angle] - ctrl3D[angle])

    
   # if qual_fact == False:
    difference3D[angle] = difference3D[angle].clip(lower=0)
   
    #print(difference3D)
   #if qual_fact == True:
   #     difference3D = difference3D[(difference3D.qualfactorangle >=0)] =0
   #     differenceXY = differenceXY[(differenceXY.qualfactorangle >=0)] =0
    #    differenceYZ = differenceYZ[(differenceYZ.qualfactorangle >=0)] =0
    #    differenceXZ = differenceXZ[(differenceXZ.qualfactorangle >=0)] =0
        
    #Filepaths to write to
    filepath3D = base_file_path + object_imaging_filepath[:-3] + "AgainstControl3D.csv"

    #Writing data to CSV
    difference3D.to_csv(filepath3D)

    

    return(difference3D,ctrl3D)

def confidence_rating_basic(control_filepath,object_imaging_filepath,qual_fact,voxel_side_length):
    #OUTDATED
    #Compares the imaged object hits to a control concrete block and gives a confidence rating of steel being in certain areas

    #One concern is that the scattering throughout the uniform block of concrete won't be uniform which could cause issues because of the acceptance...
    #An basic approach would just to be to find the standard dev of angles across the whole block and then compare to the control above and assign 
    if qual_fact == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    #Getting the data that shows the differences 
    difference_df, control_df = compare_control(control_filepath,object_imaging_filepath,qual_fact,voxel_side_length)
    confidence_df = difference_df
    difference_angles = (difference_df[angle].to_numpy())
    #
    # difference_qual = (difference_df['qualfactorangle'].to_numpy())

    #inefficient as it's already been read in compare_control but for ease of use / it doesn't take long to open
    
    control_df[angle] = control_df[angle].astype(float)
    control_df[angle] = control_df[angle].fillna(0)



    angle_values = control_df[angle].to_numpy()
    #angle_stdev = statistics.stdev(angle_values)
    angle_stdev = statistics.stdev(difference_angles)


    #Confidence 
    angle_confidence = scipy.stats.norm(0,5*angle_stdev).cdf(difference_angles)



    confidence_df[angle] = angle_confidence
    base_file_path = "/home/anthony/MastersThesis/Data"
    filepath = base_file_path + object_imaging_filepath[:-4] + "Confidence.csv"

    confidence_df.to_csv(filepath)

    return(None)



#voxel_side_length = 8#mm
#binned_clustered = True
key = "POCA"

base_filepath = "/home/anthony/MastersThesis/Data/"
control1filename = "/JustConcreteBeam/JustBeam1Interaction.h5"

#df1 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam1Interaction.h5",key)
#df2 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam2Interaction.h5",key)
#df3 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam3Interaction.h5",key)
#df4 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam4Interaction.h5",key)

#control1df = pd.concat([df1,df2,df3,df4])

#control2filename = "/JustConcreteBeam2/JustBeam1Interaction.h5"

#df1 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam1Interaction.h5",key)
#df2 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam2Interaction.h5",key)
#df3 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam3Interaction.h5",key)
#df4 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam4Interaction.h5",key)

#control2df = pd.concat([df1,df2,df3,df4])

#df1 = ReadH5.pandas_read("/DisconnectedRebar10cmGap/Gaussian/Disconnected10cmGapInteractionUncertantity.h5",key)
#df2 = ReadH5.pandas_read("/DisconnectedRebar10cmGap/Gaussian/Disconnected10cmGap2InteractionUncertantity.h5",key)
#df3 = ReadH5.pandas_read("/DisconnectedRebar10cmGap/Gaussian/Disconnected10cmGap3InteractionUncertantity.h5",key)
#df4 = ReadH5.pandas_read("/DisconnectedRebar10cmGap/Gaussian/Disconnected10cmGap4InteractionUncertantity.h5",key)
#imagingfilename = "/DisconnectedRebar10cmGap/Gaussian/Disconnected10cmGapInteractionUncertantity.h5"




#df1 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadiusInteraction.h5",key)
#df2 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadius2Interaction.h5",key)
#df3 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadius3Interaction.h5",key)
#df4 = ReadH5.pandas_read("/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadius4Interaction.h5",key)
#imagingfilename = "/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticConcreteBeam15mmRadiusInteraction.h5"


#df1 = ReadH5.pandas_read("/RealisticConcreteBeam10mmRadius/RealisticBeam10mmRad1Interaction.h5",key)
#df2 = ReadH5.pandas_read("/RealisticConcreteBeam10mmRadius/RealisticBeam10mmRad2Interaction.h5",key)
#df3 = ReadH5.pandas_read("/RealisticConcreteBeam10mmRadius/RealisticBeam10mmRad3Interaction.h5",key)
#df4 = ReadH5.pandas_read("/RealisticConcreteBeam10mmRadius/RealisticBeam10mmRad4Interaction.h5",key)
#imagingfilename = "/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticBeamInteraction.h5"

#df1 = ReadH5.pandas_read("/RealisticConcreteBeam5mmRadius/RealisticBeam5mmRad1Interaction.h5",key)
#df2 = ReadH5.pandas_read("/RealisticConcreteBeam5mmRadius/RealisticBeam5mmRad2Interaction.h5",key)
#df3 = ReadH5.pandas_read("/RealisticConcreteBeam5mmRadius/RealisticBeam5mmRad3Interaction.h5",key)
#df4 = ReadH5.pandas_read("/RealisticConcreteBeam5mmRadius/RealisticBeam5mmRad4Interaction.h5",key)
#imagingfilename = "/RealisticConcreteBeam15mmRadius/ExactPrecision/RealisticBeamInteraction.h5"

#imaging = pd.concat([df1,df2,df3,df4])

VoxelSize = [15,12.5]
STDcheck = [5]
FilterOutBelow = [0]
neighbour_average = [True,False]
binned_clustered = True
angle_type = 3
key = "POCA"

base_data_directory = "/home/anthony/MastersThesis/Data/"
ParentFolderPath = "/home/anthony/MastersThesis/Figures/MassOutput"
interaction_name = ["RealisticConcreteBeam15mmRadius","RealisticConcreteBeam10mmRadius","RealisticConcreteBeam5mmRadius","Disconnected10cmGap","RustedBeam15mm"]

def make_heatmaps(base_data_directory,interaction_name,VoxelSize,STDcheck,filter,binned_clustered,angle_type,key,ParentFolderPath):
    df1 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam1Interaction.h5",key)
    df2 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam2Interaction.h5",key)
    df3 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam3Interaction.h5",key)
    df4 = ReadH5.pandas_read("/JustConcreteBeam/JustBeam4Interaction.h5",key)

    control1df = pd.concat([df1,df2,df3,df4])

    control2filename = "/JustConcreteBeam2/JustBeam1Interaction.h5"

    df1 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam1Interaction.h5",key)
    df2 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam2Interaction.h5",key)
    df3 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam3Interaction.h5",key)
    df4 = ReadH5.pandas_read("/JustConcreteBeam2/JustBeam4Interaction.h5",key)

    control2df = pd.concat([df1,df2,df3,df4])
    
    #Makes the figures on mass
    #ParentFolderPath is where the output files will go 
    try: 
        os.mkdir(ParentFolderPath) 
    except OSError as error: 
        print(ParentFolderPath)
        
    ParticleDetectorUncertantity = ["ExactPrecision","Gaussian","TopHat"]
    
    for i  in interaction_name:
        try: 
            os.mkdir(ParentFolderPath + "/" + i) 
        except OSError as error: 
            print(error)
            
        for j in ParticleDetectorUncertantity:
            data_dir = base_data_directory + i + "/" + j + "/"
            
            if j == "Gaussian" or "TopHat":
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
                
            try: 
                os.mkdir(ParentFolderPath + "/" + i + "/" + j) 
            except OSError as error: 
                print(error)


            confidence_values(control1df,control1filename,
                            control2df,control2filename,
                            imaging,imagingfilename,
                            angle_type,binned_clustered,
                            STDcheck,filter,VoxelSize)

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
                    
                Voxel.heatmap_slices_xy(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type,l,0.7,Directory_slicesXY)
                Voxel.heatmap_slices_zy(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type,l,0.7,Directory_slicesZY)
                Voxel.heatmap_slices_zx(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type,l,0.7,Directory_slicesZX)
        return(None)

make_heatmaps(base_data_directory,interaction_name,15,5,0,binned_clustered,angle_type,key,ParentFolderPath)
'''    
for i in VoxelSize:
    for j in STDcheck: 
        for k in FilterOutBelow:
            ParentFolderPath = "/home/anthony/MastersThesis/Data/ParameterTesting/" + str(i) + "mmVoxel_" + str(j) + "STD_" + str(k) + "Filter"
            
            try: 
                os.mkdir(ParentFolderPath) 
            except OSError as error: 
                print(error)
                
            confidence_values(control1df,control1filename,
                             control2df,control2filename,
                              imaging,imagingfilename,
                              angle_type,binned_clustered,
                              j,k,i) #Finds the confidence for the given parameters
            
            for l in neighbour_average:
                if l == True:
                    neighbour_path = "NeighbourAverage"
                    
                else: 
                    neighbour_path = "NotNeighbourAverage"
                
                try: 
                    os.mkdir(ParentFolderPath + "/" + neighbour_path) 
                except OSError as error: 
                    print(error)
                    
                Directory_slices = ParentFolderPath + "/" + neighbour_path +"/XYHeatMapSlices"
                try: 
                    os.mkdir(Directory_slices) 
                except OSError as error: 
                    print(error)
                
                Voxel.heatmap_slices_xy(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type,l,k,Directory_slices)
'''         
            



#Voxel.heatmap_slices_xy(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type)
#Voxel.heatmap_slices_zy(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type)
#Voxel.heatmap_slices_zx(base_filepath + imagingfilename[:-3] + "Confidence.csv",angle_type)
