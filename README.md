simpleFEA
=========

A simple structural FEA program as a project for learning FEA programming.

## Contents
Currently features the following:

*Preprocessing*

- Node
- Element

*Loads*

- Nodal displacement
- Nodal force

*Elements*

- Two-dimensional link/truss (`Link2D`)

*Solution*

- Linear


## Usage

All model building is via direct generation of nodes and elements. Create nodes
and elements with the `Node` and `Link2D` classes.

Imports:

```Python
from simpleFEA import *
from simpleFEA.elements import Link2D
```

Create a material:

```Python
mat = LinearMaterial(E=5e5)
```

Build the model mesh:

```Python
n1 = Node(0, 0)
n2 = Node(10, 0)
n3 = Node(10, 10)
e1 = Link2D(n1, n2, mat, A=0.25)
e2 = Link2D(n1, n3, mat, A=0.25)
e3 = Link2D(n2, n3, mat, A=0.25)
```

Create a `Model` instance:

```Python
model = Model('my model', [e1,e2,e3])
```

Add displacements, forces:

```Python
model.D(n1, x=0, y=0)
model.D(n2, y=0)
model.F(n3, x=100)
```

Then add a solver and call `solve`:

```Python
model.solver = LinearSolution
model.solve()
```

Results are available on the nodes or elements:

```Python
print(n3.ux)                    # UX displacement
print(n3.uy)                    # UY displacement
print(e2.F)                     # Element axial force
print(e2.Sa)                    # Element axial stress
```

Output:

```
0.03062741699796952
-0.008
141.42135623730948
565.6854249492379
```

Or with summary properties:

```Python
print(model.solution.prnsol)    # ANSYS print nodal solution
```

```
Nodal Displacement Solution

   Node |           ux |     uy |   uz
--------+--------------+--------+------
      1 |  0           |  0     |    0
      2 | -4.89859e-19 |  0     |    0
      3 |  0.0306274   | -0.008 |    0
```

```Python
print(model.solution.prrsol)    # ANSYS print nodal reaction solution
```

```
Nodal Force Reaction Solution

   Node |   Fx |   Fy | Fz
--------+------+------+------
      1 | -100 | -100 |
      2 |      |  100 |
```
