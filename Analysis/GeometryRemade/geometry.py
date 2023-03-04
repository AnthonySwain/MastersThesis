import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# https://stackoverflow.com/questions/72182976/plotly-how-to-plot-cylinder
def cylinder(x, y, z, r, dz):
    """Create a cylindrical mesh located at x, y, z, with radius r and height dz"""
    center_z = np.linspace(0, dz, 15)
    theta = np.linspace(0, 2*np.pi, 15)
    theta_grid, z_grid = np.meshgrid(theta, center_z)
    x_grid = r * np.cos(theta_grid) + x
    y_grid = r * np.sin(theta_grid) + y
    z_grid = z_grid + z
    return x_grid, y_grid, z_grid

def circle(x, y, z, r):
    """Create a circular mesh located at x, y, z with radius r"""
    r_discr = np.linspace(0, r, 2)
    theta_discr = np.linspace(0, 2*np.pi, 15)
    r_grid, theta_grid = np.meshgrid(r_discr, theta_discr)
    x_circle = r_grid * np.cos(theta_grid) + x
    y_circle = r_grid * np.sin(theta_grid) + y
    z_circle = np.zeros_like(x_circle) + z
    return x_circle, y_circle, z_circle

# cylinder mesh
x_cyl, y_cyl, z_cyl = cylinder(0, 0, -425, 50, 950)
# bottom cap
x_circle1, y_circle1, z_circle1 = circle(0, 0, -425, 50)
# top cap
x_circle2, y_circle2, z_circle2 = circle(0, 0, 950-425, 50)

colorscale = [[0, '#0a0a0a'],
             [1, '#0a0a0a']]


x_concrete_half = 1*1000
y_concrete_half = 0.5*1000
z_concrete_half = 0.5*1000


x_detector_half = 0.75*1000
y_detector_half = 0.6*1000
z_detector_half = 0.0005*1000

#They are all 0 in x,y so just care about z
detector_center1 = (0.525)*1000
detector_center2 = (0.725)*1000
detector_center3 = (-0.525)*1000
detector_center4 = (-0.725)*1000

x=[1.2]
y=[2.4]
z=[0]

fig = go.Figure(data=[
     go.Scatter3d(x=x, y=y, z=z,
                  mode='markers',
                  marker=dict(size=2)
                 ),
     
     go.Mesh3d(
        #the concrete (centered at 0,0,0)
        # 8 vertices of a cube, 
        x=[x_concrete_half, x_concrete_half, -x_concrete_half, -x_concrete_half, x_concrete_half, x_concrete_half, -x_concrete_half, -x_concrete_half],
        y=[y_concrete_half, -y_concrete_half, -y_concrete_half, y_concrete_half, y_concrete_half, -y_concrete_half, -y_concrete_half, y_concrete_half],
        z=[z_concrete_half, z_concrete_half, z_concrete_half, z_concrete_half, -z_concrete_half, -z_concrete_half, -z_concrete_half, -z_concrete_half],

        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.5,
        color='#b2b2b8',
        flatshading = True
    ),
     go.Mesh3d(
        #detector1
        # 8 vertices of a cube, 
        x=[x_detector_half, x_detector_half, -x_detector_half, -x_detector_half, x_detector_half, x_detector_half, -x_detector_half, -x_detector_half],
        y=[y_detector_half, -y_detector_half, -y_detector_half, y_detector_half, y_detector_half, -y_detector_half, -y_detector_half, y_detector_half],
        z=[z_detector_half+detector_center1, z_detector_half+detector_center1, z_detector_half+detector_center1, z_detector_half+detector_center1, -z_detector_half+detector_center1, -z_detector_half+detector_center1, -z_detector_half+detector_center1, -z_detector_half+detector_center1],

        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.4,
        color='#DC143C',
        flatshading = True
    ),
     go.Mesh3d(
        #detector2
        # 8 vertices of a cube, 
        x=[x_detector_half, x_detector_half, -x_detector_half, -x_detector_half, x_detector_half, x_detector_half, -x_detector_half, -x_detector_half],
        y=[y_detector_half, -y_detector_half, -y_detector_half, y_detector_half, y_detector_half, -y_detector_half, -y_detector_half, y_detector_half],
        z=[z_detector_half+detector_center2, z_detector_half+detector_center2, z_detector_half+detector_center2, z_detector_half+detector_center2, -z_detector_half+detector_center2, -z_detector_half+detector_center2, -z_detector_half+detector_center2, -z_detector_half+detector_center2],

        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.4,
        color='#DC143C',
        flatshading = True
    ),
     go.Mesh3d(
        #detector3
        # 8 vertices of a cube, 
        x=[x_detector_half, x_detector_half, -x_detector_half, -x_detector_half, x_detector_half, x_detector_half, -x_detector_half, -x_detector_half],
        y=[y_detector_half, -y_detector_half, -y_detector_half, y_detector_half, y_detector_half, -y_detector_half, -y_detector_half, y_detector_half],
        z=[z_detector_half+detector_center3, z_detector_half+detector_center3, z_detector_half+detector_center3, z_detector_half+detector_center3, -z_detector_half+detector_center3, -z_detector_half+detector_center3, -z_detector_half+detector_center3, -z_detector_half+detector_center3],

        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.4,
        color='#DC143C',
        flatshading = True
    ),
     
     go.Mesh3d(
        #detector4
        # 8 vertices of a cube, 
        x=[x_detector_half, x_detector_half, -x_detector_half, -x_detector_half, x_detector_half, x_detector_half, -x_detector_half, -x_detector_half],
        y=[y_detector_half, -y_detector_half, -y_detector_half, y_detector_half, y_detector_half, -y_detector_half, -y_detector_half, y_detector_half],
        z=[z_detector_half+detector_center4 , z_detector_half+detector_center4 , z_detector_half+detector_center4 , z_detector_half+detector_center4 , -z_detector_half+detector_center4 , -z_detector_half+detector_center4 , -z_detector_half+detector_center4 , -z_detector_half+detector_center4 ],

        i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=0.4,
        color='#DC143C',
        flatshading = True
    ),
    # The cylinder
    go.Surface(x=z_cyl, y=x_cyl, z=y_cyl, colorscale=colorscale, showscale=False, opacity=1),
    go.Surface(x=z_circle1, y=x_circle1, z=y_circle1, showscale=False, opacity=1),
    go.Surface(x=z_circle2, y=x_circle2, z=y_circle2, showscale=False, opacity=1),
])         
                       
#fig =px.scatter_3d(x=0.5,y=-0.5,z=2.0)

fig.show()