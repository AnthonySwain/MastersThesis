#This takes away the values from the control piece of concrete (with no steel) and the concrete with steel in
#Couple things - need to make sure the voxel sizes are the same - could just create voxel arrays in here by calling voxel.py
#Confidence intervals is something I really want to put into the code

import numpy as np
import Voxel as Voxel
import pandas as pd
import statistics
import scipy.stats
import ReadH5 as ReadH5

#Note this is filepaths:))
detector_in_corners = ([0.75*1000,0.6*1000,0.5*1000],
                    [0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,-0.6*1000,0.5*1000],
                     [-0.75*1000,0.6*1000,0.5*1000])

detector_out_corners = ([0.75*1000,0.6*1000,-0.5*1000],
                    [0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,-0.6*1000,-0.5*1000],
                     [-0.75*1000,0.6*1000,-0.5*1000])


def compare_control(control_filepath,object_imaging_filepath,qual_fact,voxel_side_length):
    
    control_df1 = ReadH5.pandas_read(control_filepath)
    control_df2 = ReadH5.pandas_read("/ReferenceConcreteBlock/2milli2Interaction.h5")
    imaging_df1 = ReadH5.pandas_read(object_imaging_filepath)
    imaging_df2 = ReadH5.pandas_read("/SteelRodInConcrete50mmRadius/2millioneventsInteraction.h5")
    
    imaging_df = pd.concat([imaging_df1,imaging_df2])
    control_df = pd.concat([control_df1,control_df2])
    
    #A good coder would make sure the dataframes match and exit out if they don't
    Voxel.voxelisation(voxel_side_length,control_filepath,control_df,qual_fact)
    Voxel.voxelisation(voxel_side_length,object_imaging_filepath,imaging_df,qual_fact)
    #Just some data cleaning ready to take the values away from eachother
    
    if qual_fact == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    
    base_file_path = "/home/anthony/MastersThesis/Data"
    
    ctrl3D = pd.read_csv(base_file_path + control_filepath[:-3] + "3D.csv")
    ctrlXY = pd.read_csv(base_file_path + control_filepath[:-3] + "xyplane.csv")
    ctrlYZ = pd.read_csv(base_file_path + control_filepath[:-3] + "yzplane.csv")
    ctrlXZ = pd.read_csv(base_file_path + control_filepath[:-3] + "xzplane.csv")
    
    img3D = pd.read_csv(base_file_path + object_imaging_filepath[:-3] + "3D.csv")
    imgXY = pd.read_csv(base_file_path + object_imaging_filepath[:-3] + "xyplane.csv")
    imgYZ = pd.read_csv(base_file_path + object_imaging_filepath[:-3] + "yzplane.csv")
    imgXZ = pd.read_csv(base_file_path + object_imaging_filepath[:-3] + "xzplane.csv")
    
    #for i in [ctrl3D,ctrlXY,ctrlYZ,ctrlXZ,img3D,imgXY,imgYZ,imgXZ]:    
    
    ctrl3D[angle] = ctrl3D[angle].astype(float)
    ctrl3D[angle] = ctrl3D[angle].fillna(0)
    
    ctrlXY[angle] = ctrlXY[angle].astype(float)
    ctrlXY[angle] = ctrlXY[angle].fillna(0)
    
    ctrlYZ[angle] = ctrlYZ[angle].astype(float)
    ctrlYZ[angle] = ctrlYZ[angle].fillna(0)
    
    ctrlXZ[angle] = ctrlXZ[angle].astype(float)
    ctrlXZ[angle] = ctrlXZ[angle].fillna(0)
    
    img3D[angle] = img3D[angle].astype(float)
    img3D[angle] = img3D[angle].fillna(0)
    
    imgXY[angle] = imgXY[angle].astype(float)
    imgXY[angle] = imgXY[angle].fillna(0)
    
    imgYZ[angle] = imgYZ[angle].astype(float)
    imgYZ[angle] = imgYZ[angle].fillna(0)
    
    imgXZ[angle] = imgXZ[angle].astype(float)
    imgXZ[angle] = imgXZ[angle].fillna(0)

        
    #Setting the base dataframe
    difference3D = img3D 
    differenceXY = imgXY
    differenceYZ= imgYZ
    differenceXZ = imgXZ
   
    #Replacing angle with the difference
    difference3D[angle] = abs(img3D[angle] - ctrl3D[angle])
    differenceXY[angle] = abs(imgXY[angle] - ctrlXY[angle])
    differenceYZ[angle] = abs(imgYZ[angle] - ctrlYZ[angle])
    differenceXZ[angle] = abs(imgXZ[angle] - ctrlXZ[angle])
    
    if qual_fact == False:
        difference3D = difference3D.loc[(difference3D.angle >=0)]
        differenceXY = differenceXY.loc[(differenceXY.angle >=0)]
        differenceYZ = differenceYZ.loc[(differenceYZ.angle >=0)]
        differenceXZ = differenceXZ.loc[(differenceXZ.angle >=0)]
        
    if qual_fact == True:
        difference3D = difference3D.loc[(difference3D.qualfactorangle >=0)]
        differenceXY = differenceXY.loc[(differenceXY.qualfactorangle >=0)]
        differenceYZ = differenceYZ.loc[(differenceYZ.qualfactorangle >=0)]
        differenceXZ = differenceXZ.loc[(differenceXZ.qualfactorangle >=0)]
        
    #Filepaths to write to
    filepath3D = base_file_path + object_imaging_filepath[:-3] + "AgainstControl3D.csv"
    filepathXY = base_file_path + object_imaging_filepath[:-3] + "AgainstControlXY.csv"
    filepathYZ = base_file_path + object_imaging_filepath[:-3] + "AgainstControlYZ.csv"
    filepathXZ = base_file_path + object_imaging_filepath[:-3] + "AgainstControlXZ.csv"

    #Writing data to CSV
    difference3D.to_csv(filepath3D)
    differenceXY.to_csv(filepathXY)
    differenceYZ.to_csv(filepathYZ)
    differenceXZ.to_csv(filepathXZ)
    
    

    return(None)

def confidence_rating_basic(control_filepath,object_imaging_filepath):
    #Compares the imaged object hits to a control concrete block and gives a confidence rating of steel being in certain areas

    #One concern is that the scattering throughout the uniform block of concrete won't be uniform which could cause issues because of the acceptance...
    #An basic approach would just to be to find the standard dev of angles across the whole block and then compare to the control above and assign 
    
    #Getting the data that shows the differences 
    difference_df = compare_control(control_filepath,object_imaging_filepath)
    confidence_df = difference_df
    difference_angles = abs(difference_df['angle'].to_numpy())
    difference_qual = abs(difference_df['qualfactorangle'].to_numpy())

    #inefficient as it's already been read in compare_control but for ease of use / it doesn't take long to open
    control_df = pd.read_csv(control_filepath)
    control_df['angle'] = control_df['angle'].astype(float)
    control_df['angle'] = control_df['angle'].fillna(0)

    control_df['qualfactorangle'] = control_df['qualfactorangle'].astype(float)
    control_df['qualfactorangle'] = control_df['qualfactorangle'].fillna(0)

    angle_values = control_df['angle'].to_numpy()
    angle_stdev = statistics.stdev(angle_values)
    
    qualfact_values = control_df['qualfactorangle'].to_numpy()
    qual_factor_stdev = statistics.stdev(qualfact_values)

    #Confidence 
    angle_confidence = scipy.stats.norm(0,angle_stdev).cdf(difference_angles)
    qualfact_confidence = scipy.stats.norm(0,qual_factor_stdev).cdf(difference_qual)


    confidence_df['angle'] = angle_confidence
    confidence_df['qualfactorangle'] = qualfact_confidence

    filepath = object_imaging_filepath[:-4] + "Confidence.csv"

    confidence_df.to_csv(filepath)

    return(None)

def confidence_rating_less_basic(control_filepath,object_imaging_filepath):
    # NOT FINISHED
    # Compares the imaged object hits to a control concrete block and gives a confidence rating of steel being in certain areas

    #One concern is that the scattering throughout the uniform block of concrete won't be uniform which could cause issues because of the acceptance...
    #An basic approach would just to be to find the standard dev of angles across the whole block and then compare to the control above and assign 

    #A less_basic approach would be to take the same idea but instead of taking stdev across the whole control block of concrete. Compare sections of the control and imaging block
    #this would hopefully reduce the effect of the non-uniformities 

    #Getting the data that shows the differences 
    difference_df = compare_control(control_filepath,object_imaging_filepath)
    confidence_df = difference_df
    difference_angles = abs(difference_df['angle'].to_numpy())
    difference_qual = abs(difference_df['qualfactorangle'].to_numpy())

    #inefficient as it's already been read in compare_control but for ease of use / it doesn't take long to open
    control_df = pd.read_csv(control_filepath)
    control_df['angle'] = control_df['angle'].astype(float)
    control_df['angle'] = control_df['angle'].fillna(0)

    control_df['qualfactorangle'] = control_df['qualfactorangle'].astype(float)
    control_df['qualfactorangle'] = control_df['qualfactorangle'].fillna(0)

    angle_values = control_df['angle'].to_numpy()
    angle_stdev = statistics.stdev(angle_values)
    
    qualfact_values = control_df['qualfactorangle'].to_numpy()
    qual_factor_stdev = statistics.stdev(qualfact_values)

    #Confidence 
    angle_confidence = scipy.stats.norm(0,angle_stdev).cdf(difference_angles)
    qualfact_confidence = scipy.stats.norm(0,qual_factor_stdev).cdf(difference_qual)


    confidence_df['angle'] = angle_confidence
    confidence_df['qualfactorangle'] = qualfact_confidence

    filepath = object_imaging_filepath[:-4] + "Confidence.csv"

    confidence_df.to_csv(filepath)

    return(None)

control_concrete_filepath = "/ReferenceConcreteBlock/2milliInteraction.h5"
object_imaging_filepath = "/SteelRodInConcrete50mmRadius/2millionevents2Interaction.h5"

base_file_path = "/home/anthony/MastersThesis/Data"

filepath3D = base_file_path + object_imaging_filepath[:-3] + "AgainstControl3D.csv"
filepathXY = base_file_path + object_imaging_filepath[:-3] + "AgainstControlXY.csv"
filepathYZ = base_file_path + object_imaging_filepath[:-3] + "AgainstControlYZ.csv"
filepathXZ = base_file_path + object_imaging_filepath[:-3] + "AgainstControlXZ.csv"


qual_fact = False
voxel_side_length = 50 #mm

compare_control(control_concrete_filepath,object_imaging_filepath,qual_fact,voxel_side_length)

#Voxel.image_heatmap_2D_x_z(filepathXZ,detector_in_corners,qual_fact)
#Voxel.image_heatmap_2D_x_y(filepathXY ,qual_fact)
#Voxel.image_heatmap_2D_y_z(filepathYZ ,qual_fact)
#Voxel.image_heatmap_3D(filepath3D,detector_in_corners,qual_fact)
Voxel.heatmap_slices(filepath3D,qual_fact)

#I think sum gives the best contrast as it takes density into account, but I need to make sure
#That if finding the difference between the sum of each that each dataset has the same number of muons accepted

#i also think that finding the mean is actually masking where the bar really is when showing 2D planes
#Need to split the 3D dataset into 2D planes and iterate through them