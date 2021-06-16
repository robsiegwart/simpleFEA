'''
Solution-level classes.
'''

import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from tabulate import tabulate


class Solution:
    '''Base class for solution objects'''
    def __init__(self, model):
        self.model = model
    
    @property
    def prnsol(self):
        '''Print the nodal displacement solution'''
        table = [ [n.num, n.ux, n.uy, n.uz] for n in self.model.nodes ]
        return '\nNodal Displacement Solution\n\n' + \
            tabulate(table, headers=['Node','ux','uy','uz'], tablefmt='presto') + '\n'
    
    def __repr__(self):
        return f'{self.name} for {self.model}'
    
    @property
    def prrsol(self):
        '''Print the nodal force reaction solution'''
        table = []
        for n in sorted(self.model.constrained_nodes, key=lambda n: n.num):
            ndr = []
            for d in n.disp:
                for i in range(1,4):
                    if i in d.DOF:
                        idx = n.indices[i]
                        ndr.append(self.F_total[idx])
                    else:
                        ndr.append(None)
            table.append([ n.num ] + ndr)
        return '\nNodal Force Reaction Solution\n\n' + \
            tabulate(table, headers=['Node','Fx','Fy','Fz'], tablefmt='presto') + '\n'


class LinearSolution(Solution):
    '''
    Linear static structural solver.

    :param Model model: The input finite element model
    '''
    name = 'Linear Structural Solver'
    
    def solve(self):
        '''Solve the matrix equations to determine the displacement solution'''
        # ------------------------------ ASSEMBLY ------------------------------
        # Assemble the global stiffness matrix
        K = lil_matrix( (self.model.global_matrix_size, self.model.global_matrix_size) )
        for e in self.model.elements:
            for row,row_data in enumerate(e.K):
                for col,entry in enumerate(row_data):
                    row_g = e.get_global_index(row)
                    col_g = e.get_global_index(col)
                    K[row_g, col_g] += entry
        self.K = K

        # Augment the displacement vector with applied displacements
        U = [None]*self.model.global_matrix_size
        for d in self.model.displacements:
            for DOF in d.DOF:
                U[d.node.indices[DOF]] = d.value(DOF)
        self.U = np.asarray(U)

        # Augment the force vector with applied forces
        F = np.zeros(self.model.global_matrix_size)
        for f in self.model.forces:
            for DOF in f.DOF:
                F[f.node.indices[DOF]] = f.value(DOF)
        self.F = F

        # ------------------------------ SOLUTION ------------------------------
        # Reduce matrices at locations of zero displacement
        keep_ind = []
        for i,each in enumerate(U):
            if each != 0:
                keep_ind.append(i)
        
        F_ = F[keep_ind]
        K_ = K[:,keep_ind][keep_ind].tocsr()

        # Solve
        self.U_ = spsolve(K_,F_)

        # ------------------------------ RECOVERY ------------------------------
        # Assemble the full displacement solution
        self.U_total = self.U.copy()
        self.U_total[keep_ind] = self.U_
        self.F_total = np.dot(self.K.toarray(),self.U_total)
        
        # Assign displacmement results to nodes
        for n in self.model.nodes:
            for DOF,ind in n.indices.items():
                n.solution.update({DOF: self.U_total[ind]})
