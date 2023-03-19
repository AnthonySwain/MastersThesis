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

def compare_control(control_filepath,object_imaging_filepath,qual_fact,voxel_side_length):
    
    control_df = ReadH5.pandas_read(control_filepath)
    imaging_df = ReadH5.pandas_read(object_imaging_filepath)

    #A good coder would make sure the dataframes match and exit out if they don't
    ctrl3D,ctrlXY,ctrlYZ,ctrlXZ = Voxel.voxelisation(voxel_side_length,control_filepath,control_df,qual_fact)
    img3D,imgXY,imgYZ,imgXZ = Voxel.voxelisation(voxel_side_length,object_imaging_filepath,imaging_df,qual_fact)
    #Just some data cleaning ready to take the values away from eachother
    
    if qual_fact == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
        
    for i in [ctrl3D,ctrlXY,ctrlYZ,ctrlXZ,img3D,imgXY,imgYZ,imgXZ]:    
        i[angle] = i[angle].astype(float)
        i[angle] = i[angle].fillna(0)

        
    #Setting the base dataframe
    difference3D = img3D 
    differenceXY = imgXY
    differenceYZ= imgYZ
    differenceXZ = imgXZ

    #Replacing angle with the difference
    difference3D[angle] = img3D[angle] - ctrl3D[angle]
    differenceXY[angle] = imgXY[angle] - ctrlXY[angle]
    differenceYZ[angle] = imgYZ[angle] - ctrlYZ[angle]
    differenceXZ[angle] = imgXZ[angle] - ctrlXZ[angle]
        
    #Filepaths to write to
    filepath3D = object_imaging_filepath[:-3] + "AgainstControl3D.csv"
    filepathXY = object_imaging_filepath[:-3] + "AgainstControlXY.csv"
    filepathYZ = object_imaging_filepath[:-3] + "AgainstControlYZ.csv"
    filepathXZ = object_imaging_filepath[:-3] + "AgainstControlXZ.csv"

    #Writing data to CSV
    difference3D.to_csv(filepath3D)
    differenceXY.to_csv(filepathXY)
    differenceYZ.to_csv(filepathYZ)
    differenceXZ.to_csv(filepathXZ)
    
    base_file_path = "/home/anthony/MastersThesis/Data"

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
steel_rod_concrete_filepath = "/SteelRodInConcrete50mmRadius/2millionevents2Interaction.h5"
qual_fact = True
voxel_side_length = 25 #mm

compare_control(control_concrete_filepath,steel_rod_concrete_filepath,qual_fact,voxel_side_length)
