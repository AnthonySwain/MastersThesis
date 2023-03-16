#Calls upon TrackReconstruction.py and VertexFinder.py to create H5 file of scattered angle and point of scattering based off of a single interaction model

import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
#from scipy.optimize import minimize
import math
import ReadH5 as ReadH5
import sys
import TrackReconstruction as trackrecon
import VertexFinder as vfinder
import IntroduceError as IntroduceError
import h5py


from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d

#Calls upon functions in track reconsruction which constructs the incoming and outgoing tracks of the particle
# then calls upon functions in vertex finder to find the scatter angle and vertex of interaction


def with_intersection(filename):
    #Redundant due to how long it takes to run / minimal improvement
    detector_data = ReadH5.get_detector_data(filename)
    #How many events are in that dataframe
    no_events = detector_data['event_no'].iloc[-1]

    #Data to input scattering data, pre-allocating the number of rows
    scattering_data = pd.DataFrame(
                                {"event_no" : pd.Series(dtype='int'),
                                    "X" : pd.Series(dtype='float'),
                                    "Y" : pd.Series(dtype='float'),
                                    "Z" : pd.Series(dtype='float'),
                                    "angle" : pd.Series(dtype='float')})

    #So the idea is to split the data into events and then into in and out detectors for the concrete.
    for i in np.arange(0,no_events):
        
        hits_data = detector_data.loc[detector_data.event_no == i]
        
        in_detector_hits = hits_data.loc[(hits_data['volume_ref'].isin([0,1]))]

        out_detector_hits = hits_data.loc[(hits_data['volume_ref'].isin([10,11]))]

        #If one of the in or out detectors wasn't hit in the event, hits_data is returned false, skip that event
        if in_detector_hits.empty or out_detector_hits.empty or (len(in_detector_hits.index) == 1) or (len(out_detector_hits.index) == 1):
            print(i,"Missed!")
            scattering_data.loc[i] = [i,0,0,0,float("NaN")]
            #Write something to the dataframe like false or smth
            continue
        print(i)
        
        pos_hits_in = in_detector_hits[['PosX','PosY','PosZ']].to_numpy()
        pos_hits_out = out_detector_hits[['PosX','PosY','PosZ']].to_numpy()

        #Calculating re-constructed lines
        result = trackrecon.fit_lines(pos_hits_in, pos_hits_out)
        line1 = Line(result[0:3],result[3:6])
        line2 = Line(result[6:9],result[9:12])

        #Finding the vertex of interaction (saying there is a single scattering incident)
        interaction_vertex_angle = vfinder.vertex_angle_find(line1,line2)

        scattering_angle = float(interaction_vertex_angle[0])
        interaction_vertex_x = float(interaction_vertex_angle[1][0])
        interaction_vertex_y = float(interaction_vertex_angle[1][1])
        interaction_vertex_z = float(interaction_vertex_angle[1][2])
        
        scattering_data.loc[i] = [i, interaction_vertex_x, interaction_vertex_y, interaction_vertex_z, scattering_angle]

    #Make this a H5 file, in the end should just append it to the original H5 file.
    interaction_filename = "/home/anthony/MastersThesis/Data" + filename[:-3] + "InteractionIntersect.h5"
    
    scattering_data.to_hdf(interaction_filename, key='Interactions', format = 'table', index=False)
    #scattering_data.to_csv('Interaction2.csv',index=False)
    return(None)

def without_intersection(filename,error):
    #Filename of the H5 file, Quality check  refines scattering angle based off of confidence of a single scattering event
    event_chunk = 9999
    #Get the indicies for the every x event numbers given
    index = ReadH5.get_event_index(filename,event_chunk)
    #print(index)
    index[0]=0
       
    k = 1 #K keeps track of which set of 10,000 rows to read (the first 10,000 2nd 10,000 ect...ect...)
    detector_data = ReadH5.get_detector_data_between_indices(filename,index[k-1],index[k])
    print(len(detector_data))
    
    if error == True:
        #this is mm
        top_hat_width = 4
        standard_dev =  2   
        
        rows = (len(detector_data))
        noise = IntroduceError.gaussian(standard_dev, (rows,3))
        noise = IntroduceError.top_hat(top_hat_width,(rows,3))
        
        detector_data['PosX'] = detector_data['PosX'] - noise[:,0]
        detector_data['PosY'] = detector_data['PosY'] - noise[:,1]
        detector_data['PosZ'] = detector_data['PosZ'] - noise[:,2]
        

    #Create file_name for output
    interaction_filename = "/home/anthony/MastersThesis/Data" + filename[:-3] + "Interaction.h5"
    
    #How many events are in that dataframe
    no_events = ReadH5.get_no_events(filename)
    
    #Data to input scattering data, pre-allocating the number of rows
    scattering_data = pd.DataFrame(
                                {"event_no" : pd.Series(dtype='int'),
                                    "X" : pd.Series(dtype='float'),
                                    "Y" : pd.Series(dtype='float'),
                                    "Z" : pd.Series(dtype='float'),
                                    "angle" : pd.Series(dtype='float'),
                                    "qualfactorangle" : pd.Series(dtype='float')})
    #index = np.arange(0,no_events),
    print(scattering_data)
    #So the idea is to split the data into events and then into in and out detectors for the concrete.
    for i in np.arange(0,no_events):
        
        hits_data = detector_data.loc[detector_data.event_no == i]
        
        in_detector_hits = hits_data.loc[(hits_data['volume_ref'].isin([0,1]))]

        out_detector_hits = hits_data.loc[(hits_data['volume_ref'].isin([10,11]))]
        
        

        #If one of the in or out detectors wasn't hit in the event, hits_data is returned false, skip that event
        if (i%event_chunk == 0):
            print(i)
            if i == 0:
                continue
            print(i)
            k+=1
            if k >= np.size(index):
                break
            scattering_data.to_hdf(interaction_filename, key='Interactions', append=True, format = 'table', index=False)
            
            #Reset the dataframe
            scattering_data = pd.DataFrame(
                                {"event_no" : pd.Series(dtype='int'),
                                    "X" : pd.Series(dtype='float'),
                                    "Y" : pd.Series(dtype='float'),
                                    "Z" : pd.Series(dtype='float'),
                                    "angle" : pd.Series(dtype='float'),
                                    "qualfactorangle" : pd.Series(dtype='float')})
            
            detector_data = ReadH5.get_detector_data_between_indices(filename,index[k-1],index[k])
            print("NEWDATASET")
            if error == True:
                #this is mm                
                rows = (len(detector_data))
                noise = IntroduceError.gaussian(standard_dev, (rows,3))
                noise = IntroduceError.top_hat(top_hat_width,(rows,3))
                
                detector_data['PosX'] = detector_data['PosX'] - noise[:,0]
                detector_data['PosY'] = detector_data['PosY'] - noise[:,1]
                detector_data['PosZ'] = detector_data['PosZ'] - noise[:,2]
            
        if in_detector_hits.empty or out_detector_hits.empty or (len(in_detector_hits.index) == 1) or (len(out_detector_hits.index) == 1):
            scattering_data.loc[i] = [i,0,0,0,math.nan,math.nan]
            #Write something to the dataframe like false or smth
            continue
            
        
        pos_hits_in = in_detector_hits[['PosX','PosY','PosZ']].to_numpy()
        pos_hits_out = out_detector_hits[['PosX','PosY','PosZ']].to_numpy()

        #Calculating re-constructed lines
        
        line1 = trackrecon.least_squares(pos_hits_in)
        line2 = trackrecon.least_squares(pos_hits_out)
        #residues = trackrecon.residues_get(line1,pos_hits_in)
        #print((residues))
        #print((trackrecon.residues_get(line2,pos_hits_out)))
        
        #Finding the vertex of interaction (saying there is a single scattering incident)
        interaction_vertex_angle = vfinder.vertex_angle_find(line1,line2)

        scattering_angle = float(interaction_vertex_angle[0])
        interaction_vertex_x = float(interaction_vertex_angle[1][0])
        interaction_vertex_y = float(interaction_vertex_angle[1][1])
        interaction_vertex_z = float(interaction_vertex_angle[1][2])
        qual_angle = float(interaction_vertex_angle[2])
        
        scattering_data.loc[i] = [i, interaction_vertex_x, interaction_vertex_y, interaction_vertex_z, scattering_angle,qual_angle]
        
        #every event_chunk data points, write to H5 file
        print(i)
        
    #Outputting remaining data into the frame
    scattering_data.to_hdf(interaction_filename, key='Interactions', append=True, format = 'table', index=False)
    
    #scattering_data.to_csv('Interaction2.csv',index=False)

    return(None)
#filename = "/Concretewithrod/SteelRodInConcrete.h5"
filename = "/SteelRodInConcrete50mmRadius/2millionevents.h5"
#filename = "/50mmSample/Lead/50000PureLeadSlab1.h5"
#with_intersection(filename)
without_intersection(filename,False)