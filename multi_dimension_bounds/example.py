from multi_dimension_bounds.method import *

phi = '-3*x1-4*x2'

psi1 = 'x1**2 + x2**2 - 25'
psi2 = '-x1*x2 + 4'
psi3 = '-x1'
psi4 = '-x2'


A = MultiDimensionWithBounds(2, phi, [psi1, psi2, psi3, psi4], [], 0.0005)
A.solve()

