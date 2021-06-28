'''
Preprocessing classes and functions.
'''

from simpleFEA.loads import Force, Displacement


def N_dist(n1,n2):
    '''Calculate the scalar distance between two nodes'''
    return ((n2.x - n1.x)**2 + (n2.y - n1.y)**2 + (n2.z - n1.z)**2)**0.5


class Node:
    '''
    Node class.
    
    :param num x,y,z:        scalar location components
    :param num num:          node number, defaults to *max defined node number + 1*
    '''
    nodes = []

    def __init__(self, x=0, y=0, z=0, num=None):
        self.x = x
        self.y = y
        self.z = z
        self.num = num if num else self.max_n + 1
        Node.nodes.append(self)

        # Initialize property containers
        self.solution = {}
        """Store solution quantities here"""
        self.loads = []
        """All loads applied to this node"""
        self.forces = []
        self.disp = []
        self.DOF = set()
        '''The DOFs for this node (none defined until attached to an element)'''
        self.indices = dict()
        '''The indices of this node's DOF in the global matrix'''
        self.elements = set()
        '''The parent elements this node is attached to'''
    
    @property
    def nDOF(self):
        return len(self.DOF)
    
    @property
    def max_n(self):
        return max([n.num for n in Node.nodes] + [0])
    
    def F(self, x=None, y=None, z=None):
        '''Apply a force to the node'''
        f = Force(self,x,y,z)
        return f

    def D(self, x=None, y=None, z=None):
        '''Apply a displacement to the node'''
        d = Displacement(self,x,y,z)
        return d
    
    def __repr__(self):
        return f'Node {self.num} ({round(self.x,3)},{round(self.y,3)},{round(self.z,3)})'

    @property
    def ux(self):
        '''The ux displacement solution quantity in the global coordinate system'''
        return self.solution[1]

    @property
    def uy(self):
        '''The uy displacement solution quantity in the global coordinate system'''
        return self.solution[2]

    @property
    def uz(self):
        '''The uz displacement solution quantity in the global coordinate system'''
        try:
            return self.solution[3]
        except KeyError:
            return 0