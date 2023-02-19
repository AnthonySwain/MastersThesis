#Makes a heatmap of the interaction points with colour based off of the angle scattered
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import scipy
from scipy.optimize import minimize

data_frame = pd.read_csv("/home/anthony/sim/Analysis/interactions&angle.csv") #opening the data file

angle = data_frame["angle"].values
x = data_frame["x"].values
y = data_frame["y"].values  
z = data_frame["z"].values

