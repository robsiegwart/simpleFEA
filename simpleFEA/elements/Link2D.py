'''
A 2D link element having 2 nodes each with 3 translational DOF.
'''

from functools import cached_property
from numpy import array, arctan, cos, sin, dot, pi
from simpleFEA.preprocessing import Element, N_dist


class Link2D(Element):
    '''
    A two-dimensional link element. Must reside in XY plane.
    
    :param Node n1:         Node 1
    :param Node n2:         Node 2
    :param Material mat:    Material
    :param num A:           Cross sectional area
    '''
    SF = array([
        [ 1, 0,-1, 0],
        [ 0, 0, 0, 0],
        [-1, 0, 1, 0],
        [ 0, 0, 0, 0]
    ])
    '''Shape function'''
    
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
        if self.n2.x == self.n1.x:
            return pi/2
        return arctan((self.n2.y - self.n1.y)/(self.n2.x - self.n1.x))
    
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

    @cached_property
    def K(self):
        '''The global element stiffness matrix'''
        Ke = self.material.E*self.A/self.L*self.SF
        """Local element stiffness matrix"""
        return dot(dot(self.T.T, Ke), self.T)

    def __repr__(self):
        return f'Element {self.num} (Link2D)'
    
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