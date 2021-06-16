'''
Material object classes.
'''

from tabulate import tabulate


class Material:
    '''Base material class.'''
    _materials = []

    def __init__(self, num=None):
        self.num = num if num else max([m.num for m in Material._materials] + [0])
        Material._materials.append(self)
    
    def __getattr__(self, prop):
        '''Retrieve a property definition'''
        return self.property_dict.get(prop)


class LinearMaterial(Material):
    '''
    Linear structural material.

    Valid property labels:
    
    ======= =======================
    ``E``   Young's Modulus
    ``nu``  Poisson's ratio
    ``rho`` Density
    ======= =======================

    :param kwargs kwargs:  Property-value pairs

    >>> mat = Material(E=29e6, nu=0.3)
    '''
    def __init__(self, num=None, **kwargs):
        super().__init__(num)
        self.property_dict = kwargs
    
    @property
    def summary(self):
        '''Return a string summary of the properties'''
        return tabulate(
            [ [k,v] for k,v in self.property_dict.items() ],
            tablefmt='plain'
        )
    
    def __repr__(self):
        return f'Linear material {self.num} with {len(self.property_dict)} defined properties.'