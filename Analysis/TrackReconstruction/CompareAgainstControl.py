#This takes away the values from the control piece of concrete (with no steel) and the concrete with steel in
#Couple things - need to make sure the voxel sizes are the same - could just create voxel arrays in here by calling voxel.py
#Confidence intervals is something I really want to put into the code

import numpy as np
import Voxel as Voxel
import pandas as pd
import statistics
import scipy.stats

#Note this is filepaths:))
control_concrete_filepath = ""
steel_rod_concrete_filepath = ""

def compare_control(control_filepath,object_imaging_filepath):
    control_df = pd.read_csv(control_filepath)
    imaging_df = pd.read_csv(object_imaging_filepath)

    #A good coder would make sure the dataframes match and exit out if they don't
    
    #Just some data cleaning ready to take the values away from eachother
    control_df['angle'] = control_df['angle'].astype(float)
    control_df['angle'] = control_df['angle'].fillna(0)

    control_df['qualfactorangle'] = control_df['qualfactorangle'].astype(float)
    control_df['qualfactorangle'] = control_df['qualfactorangle'].fillna(0)

    imaging_df['angle'] = imaging_df['angle'].astype(float)
    imaging_df['angle'] = imaging_df['angle'].fillna(0)

    imaging_df['qualfactorangle'] = imaging_df['qualfactorangle'].astype(float)
    imaging_df['qualfactorangle'] = imaging_df['qualfactorangle'].fillna(0)
    
    #Dataframe to plot the difference between the control and 
    difference_df = imaging_df

    difference_df['angle'] = imaging_df['angle'] - control_df['angle']
    difference_df['qualfactorangle'] = imaging_df['qualfactorangle'] - control_df['qualfactorangle'] 

    filepath = object_imaging_filepath[:-4] + "AgainstControl.csv"

    difference_df.to_csv(filepath)


    return(difference_df)

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
    #Compares the imaged object hits to a control concrete block and gives a confidence rating of steel being in certain areas

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