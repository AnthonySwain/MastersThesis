import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d


def get_real():
    #Extracting data from the reality of the particle travel
    df = pd.read_csv("/home/anthony/sim/build/datatest2.csv")#opening the data file
    pos_in_X = df["PosX"].values
    pos_in_Y = df["PosY"].values
    pos_in_Z = df["PosZ"].values 
    reality = (pos_in_X,pos_in_Y,pos_in_Z)
    reality = np.stack(reality, axis=1)
    return(reality)

def how_many_events():
    #Finds how many events were in the data file
    data_frame = pd.read_csv("/home/anthony/sim/build/DetectorHits.csv") #opening the data file
    event_no = data_frame["event_no"].values
    events = event_no[-1] +1
    return(events)

def get_hits(event_no):
    #Getting position and times of the hits from the data file for the specified event
    #In_hits should contain the incoming hits and times
    #Out_hits should contain the outgoing hits and times

    data_frame = pd.read_csv("/home/anthony/sim/build/DetectorHits.csv") #opening the data file

    #Splitting data into position and time for in and out detector and returning an arary of this.
    event_no = data_frame.query(f"event_no == {event_no}")
    in_detector = event_no.query("volume_name == 'InDetector'")
    out_detector = event_no.query("volume_name == 'OutDetector'")

    pos_in_X = in_detector["PosX"].values
    pos_in_Y = in_detector["PosY"].values
    pos_in_Z = in_detector["PosZ"].values
    time_in = in_detector["time"].values

    in_hits = (pos_in_X,pos_in_Y,pos_in_Z)
    in_times = np.stack(time_in, axis=0)
    in_hits = np.stack(in_hits, axis=1)
    

    pos_out_X = out_detector["PosX"].values
    pos_out_Y = out_detector["PosY"].values
    pos_out_Z = out_detector["PosZ"].values
    time_out = out_detector["time"].values

    out_hits = (pos_out_X,pos_out_Y,pos_out_Z)
    out_times = np.stack(time_out, axis=0)
    out_hits = np.stack(out_hits, axis=1)

    return(in_hits, in_times, out_hits, out_times)