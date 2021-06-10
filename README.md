simpleFEA
=========

A completely simple and trivial structural FEA program as a project for learning
FEA programming.

## Contents
Currently features the following:

*Preprocessing*

- Node
- Element

*Loads*

- Nodal displacement
- Nodal force

*Elements*

- Two-dimensional link/spar (`Link2D`)

*Solution*

- Linear


## Usage

All model building is via direct generation of nodes and elements. Create nodes
and elements with the `Node` and `Link2D` classes.

```Python
n1 = Node(0, 0, 0)
n2 = Node(10, 0, 0)
n2 = Node(10, 10, 0)
e1 = Link2D(n1, n2, A=2)
e1 = Link2D(n1, n3, A=2)
```

Add material properties:

```Python
mat1 = LinearMaterial(1, E=29e6)
```

Create a `Model` instance to organize a model and add elements.

```Python
model = Model('my model')
model.add_elems(e1, e2)
model.add_mat(mat1)
```

Add displacements and optionally forces.

```Python
model.D(n1, x=0, y=0)
model.D(n2, x=0, y=0)
model.F(n3, x=10, y=20)
```

Then add a solver and call `solve`:

```Python
model.solver = LinearSolution
model.solve()
```

Results are available on the nodes or elements:

```Python
print(n3.ux)    # UX displacement
print(n3.uy)    # UY displacement
print(e1.Fe)    # Element axial force
print(e1.Sa)    # Element axial stress
```

