#This file is solely for adding error to the detector measurements to represent a more lifelike detector
#File to be called when finding interactions, data set is loaded, error applied 

import numpy as np

def top_hat(width,size):
    #Imitates a tophat error in the detector hits
    noise = np.random.Generator.uniform(low = -width/2, high = width/2, size=size)
    return(noise)

def gaussian(standard_dev,size):
    #Imitates a gaussian error in the detector hits
    noise = np.random.normal(0,standard_dev,size=size)
    
    return(noise)

