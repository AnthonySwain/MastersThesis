import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

import ReadH5 as ReadH5
import TrackReconstruction.TrackReconstruction as trackrecon
import TrackReconstruction.VertexFinder as vfinder

from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d

#Can change this into writing into another dataset in the H5 file with the event no, scattering angle and vertex

#The function reads the H5 file, reconstructs the tracks, finds the scattering angle and vertex point
# and then writes this data into a new dataset in the H5 file. 


no_events = extractdata.how_many_events()

scattering_angle = []
interaction_vertex_x = []
interaction_vertex_y = []
interaction_vertex_z = []

for i in range (no_events):
    print(i)
    hits_data = extractdata.get_hits(i)

    #If one of the detectors wasn't hit in the event, hits_data is returned false, skip that event
    if hits_data == False:
        print("false baby")
        continue

    pos_hits_in = hits_data[0]
    pos_hits_out = hits_data[2]

    #Calculating re-constructed lines
    result = trackrecon.fit_lines(pos_hits_in, pos_hits_out)
    line1 = Line(result[0:3],result[3:6])
    line2 = Line(result[6:9],result[9:12])

    #Finding the vertex of interaction (saying there is a single scattering incident)
    interaction_vertex_angle = vfinder.vertex_angle_find(line1,line2)

    scattering_angle.append(interaction_vertex_angle[0])
    interaction_vertex_x.append(interaction_vertex_angle[1][0])
    interaction_vertex_y.append(interaction_vertex_angle[1][1])
    interaction_vertex_z.append(interaction_vertex_angle[1][2])



data = list(zip(scattering_angle,interaction_vertex_x,interaction_vertex_y,interaction_vertex_z))

df = pd.DataFrame(data,columns=["angle","x","y","z"])
df.to_csv('interactions&angle.csv', index=False)

