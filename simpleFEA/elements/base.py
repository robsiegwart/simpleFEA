'''
Base classes for elements.
'''

import math
from numpy import arctan, pi, dot, array
from simpleFEA.preprocessing import N_dist


class Element:
    '''
    Base class for all elements.
    
    :param int num:             element number, defaults to *max defined element number + 1*
    :param Material material:   material definition
    '''
    elements = []

    def __init__(self, num=None, material=None):
        self.num = num if num else self.max_e + 1
        Element.elements.append(self)
        self.material = material
        self.solution = {}
        """Store solution quantities here"""

        # Bookeeping for nodes on new element creation
        for n in self.nodes:
            # Assign the DOF to the nodes
            n.DOF = n.DOF|self.DOF
            # Add the element as a parent
            n.elements.add(self)
    
    @property
    def max_e(self):
        '''Max element number defined'''
        return max([e.num for e in Element.elements] + [0])
    
    def get_global_index(self, local_index: int) -> int:
        '''
        Return the global index based on the row/col indices of an entry in the
        local element stiffness matrix.

        :param int local_index:     The row or column index of the entry in the
                                    local element stiffness matrix
        '''
        node = math.floor(local_index/self.nDOF)
        DOF = local_index - (node)*self.nDOF + 1
        return self.nodes[node].indices[DOF]
    
    @property
    def nDOF(self):
        '''Number of DOF per node'''
        return len(self.DOF)
    
    def __repr__(self):
        return f'Element {self.num} ({self.ENAME})'

    __str__ = __repr__
    

class TwoNodeElement(Element):
    '''Base class for link and beam elements having two nodes'''
    
    n_num = 2
    '''Number of nodes forming the element'''

    def __init__(self, num, mat):
        super().__init__(num, mat)
        
        # Check that nodes are not coincident
        if self.n1.x == self.n2.x and self.n1.y == self.n2.y:
            raise Exception(f'Nodes for {self} are coindicent.')

    # Properties
    @property
    def L(self):
        '''The scalar length of the element.'''
        return N_dist(self.n1, self.n2)
    
    @property
    def nodes(self):
        '''The nodes defining the element as a tuple.'''
        return (self.n1, self.n2)
    
    @property
    def theta(self):
        '''The angle in radians formed by the element w.r.t the horizontal axis.'''
        return math.atan2((self.n2.y - self.n1.y), (self.n2.x - self.n1.x))

    # Post processing
    @property
    def d(self):
        '''Element elongation, equal to n_j,x - n_i,x'''
        # Transform first into local element coordinates
        u1x, u1y, u2x, u2y = dot(self.T, array([
            self.n1.solution[1], self.n1.solution[2], self.n2.solution[1], self.n2.solution[2]
        ]))
        return u2x - u1x

    @property
    def F(self):
        '''Axial force in member'''
        return self.material.E*self.A/self.L*self.d

    @property
    def Sa(self):
        '''Axial stress in element'''
        return self.F/self.A