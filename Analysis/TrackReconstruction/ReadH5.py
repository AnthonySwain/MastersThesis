import h5py
import pandas as pd
import numpy as np
filename = "/home/anthony/MastersThesis/build/OutputTest.h5"

def get_detector_data(filename):
    #Assume filepath is to the data folder, returns panda dataframe of file
    filepath = "/home/anthony/MastersThesis/data" + filename
    with h5py.File(filepath, "r") as f:
        detector_data = f['DetectorOutput']
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

gen_data = get_initial_data("01.03.2023/10000PureConcrete.h5")
print(gen_data)