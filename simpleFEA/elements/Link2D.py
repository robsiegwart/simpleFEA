'''
A 2D link element having 2 nodes each with 2 translational DOF.
'''

from functools import cached_property
from numpy import array, cos, sin, dot
from .base import TwoNodeElement


class Link2D(TwoNodeElement):
    '''
    A two-dimensional link element. Must reside in XY plane.
    
    :param Node n1:         Node 1
    :param Node n2:         Node 2
    :param Material mat:    Material
    :param num A:           Cross sectional area
    '''
    
    DOF = set([1,2])
    '''Nodal degree-of-freedoms (DOF) - ux (1) and uy (2)'''

    nDOF = len(DOF)
    '''Number of DOF per node'''
    
    n_num = 2
    '''Number of nodes forming the element'''

    def __init__(self, n1, n2, mat=None, A=None, num=None):
        self.n1 = n1
        self.n2 = n2
        self.A = A
        self._nodes = (n1, n2)
        super().__init__(num, mat)
    
    @cached_property
    def T(self):
        """The displacment transformation matrix"""
        c = cos(self.theta)
        s = sin(self.theta)
        return array([
                [ c, s, 0, 0],
                [-s, c, 0, 0],
                [ 0, 0, c, s],
                [ 0, 0,-s, c]
            ])
    
    @property
    def Ke(self):
        '''The stiffness matrix in the element coordinate system'''
        return self.material.E*self.A/self.L*array([
                [ 1, 0,-1, 0],
                [ 0, 0, 0, 0],
                [-1, 0, 1, 0],
                [ 0, 0, 0, 0]
            ])

    @cached_property
    def K(self):
        '''The global element stiffness matrix'''
        return dot(dot(self.T.T, self.Ke), self.T)

    def __repr__(self):
        return f'Element {self.num} (Link2D)'