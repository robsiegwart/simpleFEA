'''
Plotting methods.
'''

import matplotlib.pyplot as plt
from numpy import array, dot, average, radians, sin, cos, arctan, pi


def init_plot(extents):
    '''Initialize a matplotlib figure'''
    fig,ax = plt.subplots()
    fig.set_size_inches(6,6)
    ax.set_aspect('equal')
    ax.grid(True)
    margin = max(extents['width'], extents['height'])*0.3
    ax.set_xlim(extents['x_min'] - margin, extents['x_max'] + margin)
    ax.set_ylim(extents['y_min'] - margin, extents['y_max'] + margin)
    return fig,ax

def plot_nodes(ax, elements):
    '''Add nodes to an axes'''
    for E in elements:
        for N in E.nodes:
            ax.plot(
                N.x, N.y,
                markersize=8,
                marker='o',
                markeredgecolor='cyan',
                markerfacecolor='white',
                markeredgewidth=2
            )
            ax.annotate('N{}'.format(N.num),(N.x, N.y))
    return ax

def plot_elements(ax, elements):
    '''Add elements to an axes'''
    for E in elements:
        R = E.plotter()
        x = R.get('x')
        y = R.get('y')
        num = R.get('num')
        ax.plot(x, y, lw=4, color='cyan')
        ax.annotate('E{}'.format(num),(average(x),average(y)))
    return ax

def get_annotation_length(extents_dict):
    '''
    Calculates the base length for annotation items.
    
    This value is some fraction of the bounding box of the model.
    '''
    return 0.1*max((extents_dict.get('x_max')-extents_dict.get('x_min')),
                (extents_dict.get('y_max')-extents_dict.get('y_min')))

def add_force_arrows(ax, extents_dict, forces_list):
    l = get_annotation_length(extents_dict)
    for f in forces_list:
        n = f.node
        ax.arrow(n.x, n.y, 3*l*f.u[0], 3*l*f.u[1], color='red', width=1)
        ax.annotate('F{}'.format(f.mag),(n.x+3*l*f.u[0],n.y+3*l*f.u[1]))

def add_displacement_arrows(ax, extents_dict, disp_list):
    ''' Add a displacement boundary condition to a 2D plot. '''
    l = get_annotation_length(extents_dict)
    for d in disp_list:
        n = d.node
        if n.x is not None:
            ax = add_bc_icon(ax,n.x,n.y,l,0)
        if n.y is not None:
            ax = add_bc_icon(ax,n.x,n.y,l,radians(-90))

def add_bc_icon(ax, x, y, length, rotation):
    ''' Add a triangle indicator to a 2D plot. '''
    tri_xy = array([ [0,0],
                     [ -length*sin(radians(30)), -length*cos(radians(30)) ],
                     [ length*sin(radians(30)),  -length*cos(radians(30)) ] ])

    line_xy = array([[0,0],
                     [0,-length*cos(radians(1))]])
    
    rot = array([ [cos(rotation), -sin(rotation)],
                  [sin(rotation), cos(rotation)] ])

    for row in range(tri_xy.shape[0]):
        tri_xy[row,:] = dot(rot,tri_xy[row,:])
    
    for row in range(line_xy.shape[0]):
        line_xy[row,:] = dot(rot,line_xy[row,:])

    tri_xy += array([x,y])
    line_xy += array([x,y])

    tri = plt.Polygon(tri_xy,fill=False)
    ax.add_patch(tri)
    ax.plot(line_xy[:,0], line_xy[:,1], color='black')
    return ax

def show_plot():
    plt.show()