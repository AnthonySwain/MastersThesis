import h5py
filename = "/home/anthony/MastersThesis/build/OutputTest.h5"

def get_detector_data(filename):
    #Assume filepath is to the data folder
    filepath = "/home/anthony/MastersThesis/data" + filename
    with h5py.File(filepath, "r") as f:
        detector_data = f['DetectorOutput']
    return(detector_data)

def get_truth_data():
    #Assume filepath is to the data folder
    filepath = "/home/anthony/MastersThesis/data" + filename
    with h5py.File(filepath, "r") as f:
        truth_data = f['StepData']
    return(None)

def get_initial_data():
    #Assume filepath is to the data folder
    filepath = "/home/anthony/MastersThesis/data" + filename
    with h5py.File(filepath, "r") as f:
        gen_data = f['InitialMuons']
    return(gen_data)