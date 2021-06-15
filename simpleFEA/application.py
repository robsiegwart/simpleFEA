'''
Project-level classes.
'''

import itertools
from tabulate import tabulate
from simpleFEA.loads import Force, Displacement


class Model:
    '''
    A finite element model consisting of a mesh (nodes, elements) plus loads
    and materials.

    Represents the subset (if any) of nodes, elements used for solution.

    Only elements are added. Nodes are attached to the elements and are included
    implicitly.

    :param str name:    Name of model (optional)
    '''
    def __init__(self, name=None, elems=[]):
        self.name = name if name else ''
        self._elements = set()
        self._nodes = set()
        self._loads = []
        self._forces = []
        self._disp = []
        self.solver = None
        self.solution = None
        if elems:
            self.add_elems(*elems)
    
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
        '''A list of displacement loads defined in the model'''
        return list(filter(lambda x: isinstance(x, Displacement), self.loads))

    @property
    def forces(self):
        '''A list of force loads defined in the model'''
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
    def materials(self):
        return set([e.material for e in self.elements])
        
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
        
        output += ' END MODEL SUMMARY '.center(80,'*') + '\n'
        
        return output
    
    def assign_nodal_DOF_indices(self):
        '''Loop through each node and assign their DOFs a global index number'''
        i = 0
        for n in self.nodes:
            for DOF in n.DOF:
                n.indices.update({DOF:i})
                i += 1
    
    @property
    def extents(self):
        '''
        Calculate the model bounds in each axis.
        
        Returns a tuple:  (x_min, x_max, y_min, y_max, z_min, z_max)
        '''
        x_min, x_max, y_min, y_max, z_min, z_max = 0,0,0,0,0,0
        for n in self.nodes:
            x_min = min(x_min, n.x)
            x_max = max(x_max, n.x)
            y_min = min(y_min, n.y)
            y_max = max(y_max, n.y)
            z_min = min(z_min, n.z)
            z_max = max(z_max, n.z)
        return (x_min, x_max, y_min, y_max, z_min, z_max)
    
    def add_elems(self, *elems):
        '''Add elements to the model'''
        for e in elems:
            self._elements.add(e)
            for n in e.nodes:
                self._nodes.add(n)
    
    def remove_elems(self, *elems):
        '''Remove elements from the model'''
        for e in elems:
            self._elements.remove(e)
    
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

    def __repr__(self):
        return f'Model {self.name}'