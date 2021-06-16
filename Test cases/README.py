from simpleFEA import *
from simpleFEA.elements import Link2D


mat = LinearMaterial(E=5e5)

n1 = Node(0, 0)
n2 = Node(10, 0)
n3 = Node(10, 10)
e1 = Link2D(n1, n2, mat, A=0.25)
e2 = Link2D(n1, n3, mat, A=0.25)
e3 = Link2D(n2, n3, mat, A=0.25)

model = Model('my model', [e1,e2,e3])

model.D(n1, x=0, y=0)
model.D(n2, y=0)
model.F(n3, x=100)

model.solver = LinearSolution
model.solve()

print(n3.ux)                    # UX displacement
print(n3.uy)                    # UY displacement
print(e2.F)                     # Element axial force
print(e2.Sa)                    # Element axial stress
print(model.solution.prnsol)    # ANSYS-type print nodal solution
print(model.solution.prrsol)    # ANSYS-type print reaction solution