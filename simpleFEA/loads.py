'''
Nodal loads classes.
'''

from numpy import array


class Load(object):
    '''Base class for loads.'''
    def __init__(self, node, x, y, z):
        self.node = node
        self.x = x
        self.y = y
        self.z = z
        
        node.loads.append(self)

        # Record which DOF(s) the force was applied to to set ``DOF``
        self.DOF = set()
        null_value = None if self.type == 'displacement' else 0
        for i,each in enumerate([x,y,z]):
            if each != null_value:
                self.DOF.add(i+1)
            
    @property
    def magnitude(self):
        '''The scalar load magnitude'''
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    @property
    def u(self):
        '''The unit vector of the load'''
        return array([self.x, self.y, self.z])/self.mag
    
    def value(self, DOF):
        '''Return the component by DOF integer lookup'''
        assert DOF in [1,2,3]
        return {1: self.x, 2: self.y, 3: self.z}[DOF]
        
    def __repr__(self):
        return f'{self.type.title()}: ({self.x},{self.y},{self.z})'
    
    __str__ = __repr__
    
    mag = magnitude


class Force(Load):
    '''
    A nodal force.
    
    :param Node node:   the target ``Node`` object
    :param num x,y,z:   force components
    '''
    type = 'force'

    def __init__(self, node, x=0, y=0, z=0):
        super().__init__(node, x, y, z)    
        node.forces.append(self)
      

class Displacement(Load):
    '''
    A displacement load.

    :param Node node:   The target ``Node`` object
    :param num x,y,z:   The coordinate displacement values
    '''
    type = 'displacement'

    def __init__(self, node, x=None, y=None, z=None):
        super().__init__(node, x, y, z)
        node.disp.append(self)