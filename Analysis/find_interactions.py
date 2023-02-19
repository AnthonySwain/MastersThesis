import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

import extractdata as extractdata
import trackreconstruction as trackrecon
import vertexfinder as vfinder

from skspatial.objects import Line, Points
from skspatial.plotting import plot_3d

no_events = extractdata.how_many_events()

scattering_angle = []
interaction_vertex_x = []
interaction_vertex_y = []
interaction_vertex_z = []

for i in range (no_events):
    hits_data = extractdata.get_hits(i)
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

