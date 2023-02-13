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

#For plotting a cylinder
def data_for_cylinder_along_z(center_x,center_y,radius,half_height_z):
    z = np.linspace(-half_height_z, half_height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid

#Extracting hits
hits_data = extractdata.get_hits()
pos_hits_in = hits_data[0]
pos_hits_out = hits_data[2]

#Calculating re-constructed lines
result = trackrecon.fit_lines(pos_hits_in, pos_hits_out)
line1 = Line(result[0:3],result[3:6])
line2 = Line(result[6:9],result[9:12])

#Finding the vertex of interaction (saying there is a single scattering incident)
interaction_vertex = vfinder.vertex_angle_find(line1,line2)

reality = extractdata.get_real()


#Plotting a figure to check all is well.

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Limits of the axes
xylim = 200
zlim = 1500

ax.set_xlim([-1*xylim,xylim])
ax.set_ylim([-1*xylim,xylim])
ax.set_zlim([-1*zlim,zlim])


#Points that made the lines
ax.scatter(pos_hits_in[:,0],pos_hits_in[:,1],pos_hits_in[:,2])
ax.scatter(pos_hits_out[:,0],pos_hits_out[:,1],pos_hits_out[:,2])
ax.scatter(reality[:,0],reality[:,1],reality[:,2], s=5)

#Plotting interaction vertex
#ax.scatter(interaction_vertex[1][0],interaction_vertex[1][1],interaction_vertex[1][2],s=10)
#ax.scatter(interaction_vertex[2][0],interaction_vertex[2][1],interaction_vertex[2][2],s=10)
ax.scatter(interaction_vertex[1][0],interaction_vertex[1][1],interaction_vertex[1][2],s=10)
#the first 2 are the cloest distances of approach of the 2 tracking lines

#Plotting the lines
#r = r_0 + const * d 
x1,y1,z1 = trackrecon.get_line_coords(line1)
x2,y2,z2 = trackrecon.get_line_coords(line2)

ax.plot(x1,y1,z1)
ax.plot(x2,y2,z2)

#Plotting a transparent image of the steel overthe top of this to get an idea of whats happening
#i really hope its all in cm lol
Xc,Yc,Zc = data_for_cylinder_along_z(0,0,50,500)
ax.plot_surface(Xc, Yc, Zc, alpha=0.5)

plt.show()