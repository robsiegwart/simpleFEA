'''
Project-level classes.
'''

import itertools
from tabulate import tabulate
from simpleFEA.loads import Force, Displacement
from simpleFEA.plotting import (
    init_plot,
    plot_elements,
    plot_nodes,
    add_displacement_arrows,
    add_force_arrows,
    show_plot
)


class Model:
    '''
    A finite element model consisting of a mesh (nodes, elements) plus loads
    and materials.

    Represents the subset (if any) of nodes, elements used for solution.

    Only elements are added. Nodes are attached to the elements and are included
    implicitly.

    :param str name:    Name of model (optional)
    '''
    def __init__(self, name=None):
        self.name = name if name else ''
        self._elements = set()
        self._nodes = set()
        self.materials = set()
        self._loads = []
        self._forces = []
        self._disp = []
        self.extents = { 'x_max': 0, 'x_min':   0,
                         'y_max': 0, 'y_min':   0,
                         'width': 0, 'height:': 0 }
        self.solver = None
        self.solution = None
    
    def solve(self):
        if not self.solver:
            raise Exception('No solver assigned')
        self.assign_nodal_DOF_indices()
        self.solution = self.solver(self)
        self.solution.solve()
    
    @property
    def loads(self):
        '''A list of the loads defined in the model'''
        return list(itertools.chain.from_iterable([l.loads for l in self._nodes]))
    
    @property
    def displacements(self):
        return list(filter(lambda x: isinstance(x, Displacement), self.loads))

    @property
    def forces(self):
        return list(filter(lambda x: isinstance(x, Force), self.loads))

    @property
    def nodes(self):
        '''A list of the nodes in the model'''
        return sorted(self._nodes, key=lambda x:x.num)
    
    @property
    def elements(self):
        '''A list of the elements in the model'''
        return sorted(self._elements, key=lambda x:x.num)
    
    @property
    def num_nodes(self):
        '''Total number of defined nodes'''
        return len(self._nodes)
    
    @property
    def num_elems(self):
        '''Total number of defined elements'''
        return len(self._elements)
    
    @property
    def global_matrix_size(self):
        '''Calculate the size of the global (stiffness) matrix.'''
        return sum([n.nDOF for n in self.nodes ])
        
    @property
    def summary(self):
        '''
        Return a string summary of the model:

            - number of nodes and elements
            - loads defined
            - materials defined
        '''
        output = '\n' + '*'*80 + '\n' + 'MODEL SUMMARY'.center(80) + '\n' + '*'*80 + '\n\n'

        output += ' Mesh '.center(80,'-') + '\n'
        output += tabulate([
                ['Nodes', self.num_nodes],
                ['Elements', self.num_elems]
            ],
            tablefmt='plain'
        ) + '\n\n'
        
        output += ' Loads '.center(80,'-') + '\n'
        output += tabulate(
            [[l.node,l] for l in self.loads],
            tablefmt='plain'
        ) + '\n\n'
        
        output += ' Materials '.center(80,'-') + '\n'
        for m in self.materials:
            output += f'-- Material {m.num} --'.center(80) + '\n'
            output += m.summary + '\n\n'
        
        output += ' END '.center(80,'*') + '\n'
        
        return output
    
    def assign_nodal_DOF_indices(self):
        '''Loop through each node and assign their DOFs a global index number'''
        i = 0
        for n in self.nodes:
            for DOF in n.DOF:
                n.indices.update({DOF:i})
                i += 1
    
    def update_extents(self, n):
        self.extents['x_max'] = max(self.extents['x_max'], n.x)
        self.extents['x_min'] = min(self.extents['x_min'], n.x)
        self.extents['y_max'] = max(self.extents['y_min'], n.y)
        self.extents['y_min'] = min(self.extents['y_min'], n.y)
        self.extents['width'] = self.extents['x_max'] - self.extents['x_min']
        self.extents['height'] = self.extents['y_max'] - self.extents['y_min']
    
    def add_elems(self, *elems):
        '''Add elements to the model'''
        for e in elems:
            self._elements.add(e)
            for n in e.nodes:
                self._nodes.add(n)
                self.update_extents(n)
    
    def remove_elems(self, *elems):
        '''Remove elements from the model'''
        for e in elems:
            self._elements.remove(e)
    
    def add_material(self,mat):
        '''Add a material definition to the model'''
        self.materials.add(mat)
    
    def F(self,node,x=0,y=0,z=0):
        '''Define a force and apply it to the model'''
        f = Force(node,x,y,z)
        self._loads.append(f)
        self._forces.append(f)

    def D(self, node,x=None,y=None,z=None):
        '''Define a displacement constraint and apply it to the model'''
        d = Displacement( node,x,y,z)
        self._loads.append(d)
        self._disp.append(d)

    def plot(self):
        '''Plot the full model with all applied BCs/loads'''
        fig,ax = init_plot(self.extents)
        ax = plot_elements(ax,self.elements)
        ax = plot_nodes(ax,self.elements)
        add_force_arrows(ax,self.extents,self._forces)
        add_displacement_arrows(ax,self.extents,self._disp)
        show_plot()
        return fig,ax

    def nplot(self):
        '''Plot just nodes'''
        fig,ax = init_plot(self.extents)
        ax.set_title('Nodes')
        ax = plot_nodes(ax,self.elements)
        show_plot()
        return fig,ax

    def eplot(self):
        '''Plot just elements'''
        fig,ax = init_plot(self.extents)
        ax.set_title('Elements')
        ax = plot_elements(ax,self.elements)
        show_plot()
        return fig,ax

    def __repr__(self):
        return f'Model {self.name}'