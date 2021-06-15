# ==============================================================================
#                              -- Test Problem --
#                  ANSYS(R) VM4: Deflection of a Hinged Support
# ==============================================================================

import time
import math
from simpleFEA import *
from simpleFEA.elements import Link2D


time_start = time.time()

# PROBLEM DEFINITION
# ==================
model = Model('VM4')

# Properties
l = 15*12      # 15 ft to inches
theta = 30     # degrees
A = 0.5        # in^2
F = 5000       # lbf
E = 30e6       # psi

a = 2*l*math.cos(math.radians(theta))
b = l*math.sin(math.radians(theta))

# Material properties
mat = LinearMaterial(1, E=E)

# Mesh
n1 = Node(0,0)
n2 = Node(a/2,-b)
n3 = Node(a,0)

e1 = Link2D(n1,n2,mat,A)
e2 = Link2D(n2,n3,mat,A)

model.add_elems(e1,e2)

# Loads and BC's
model.F(n2, y=-F)
model.D(n1, x=0, y=0)
model.D(n3, x=0, y=0)

# Model diagnostics
print(model.summary)


# SOLUTION AND POST-PROCESSING
# ============================
# Solve
model.solver = LinearSolution
model.solve()


# Results Comparison
# ------------------

# Node 2 deformation - target value is -0.120
print(n2.uy)

# Element stress - target value is 10,000
print(e1.Sa)


# -----------------------------------------------------------------------------
time_end = time.time()
print('\nTime elapsed: {} sec'.format(time_end-time_start))