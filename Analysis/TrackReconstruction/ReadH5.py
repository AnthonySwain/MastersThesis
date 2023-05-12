#File of functions for reading various H5 files for ease of use

import h5py
import pandas as pd
import numpy as np
import sys

#Pre-made functions to read H5 files and return a panda dataframe of the datafile 

def get_detector_data(filename):
    #Assume filepath is to the data folder, returns panda dataframe of file
    filepath = "/home/anthony/MastersThesis/Data" + filename
    with h5py.File(filepath, "r") as f:
        detector_data = f['DetectorOutput']
        detector_data_panda = pd.DataFrame(np.array(detector_data))
    return(detector_data_panda)

def get_detector_data_between_indices(filename,start_index,final_index):
    #Assume filepath is to the data folder, returns panda dataframe of file
    filepath = "/home/anthony/MastersThesis/Data" + filename
    with h5py.File(filepath, "r") as f:
        detector_data = f['DetectorOutput'][np.arange(start_index,final_index)]
        detector_data_panda = pd.DataFrame(np.array(detector_data))
    return(detector_data_panda)

def get_truth_data(filename):
    #Assume filepath is to the data folder, returns panda dataframe of file
    filepath = "/home/anthony/MastersThesis/Data" + filename
    with h5py.File(filepath, "r") as f:
        truth_data = f['StepData']
        truth_data_panda = pd.DataFrame(np.array(truth_data))
    return(truth_data_panda)

def get_initial_data(filename):
    #Assume filepath is to the data folder, returns panda dataframe of file
    filepath = "/home/anthony/MastersThesis/Data/" + filename
    with h5py.File(filepath, "r") as f:
        gen_data = f['InitialMuons']
        gen_data_panda = pd.DataFrame(np.array(gen_data))
    return(gen_data_panda)

def pandas_read(filename,key):
    filepath = "/home/anthony/MastersThesis/Data" + filename
    interaction_data = pd.read_hdf(filepath,key=key)
    return(interaction_data)

def get_no_events(filename):
    #Assume filepath is to the data folder, returns panda dataframe of file
    filepath = "/home/anthony/MastersThesis/Data" + filename
    with h5py.File(filepath, "r") as f:
        no_events = f['DetectorOutput'][-1,'event_no']
        
    return(no_events)

#So I want to load the events columns, and get the index of every 10,000 events 
#So i then know how much to load between 

def get_event_index(filename,how_many_events):
    #How many events is how often to get the indicies for
    # e.g. get the indicies of every 10,000 events 
    filepath = "/home/anthony/MastersThesis/Data" + filename
    index = []
    with h5py.File(filepath, "r") as f:
        events = f['DetectorOutput'][:,'event_no']
        events = np.array(events)
        #print(np.shape(events))
        #print(events)
        indices = np.where(events%how_many_events ==0)[0]
        index = []
        
        for i in range(indices.shape[0]):
        
            if i == 0:
                continue
            
            if indices[i-1] == indices[i]-1:
                continue
            
            else:
                index.append(indices[i-1])
        index.append(np.shape(events)[0]-1)
    return(index)