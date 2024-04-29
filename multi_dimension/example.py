from multi_dimension.methods import *
import math

f = FunctionOfVector(2, 'ln(x1**2 + x2**2 + 5) + x1**2 + x2**2')
# f = FunctionOfVector(2, 'x1**2 + x2**2 + cos(x1 + x2)')

# print('eps'.center(9) + 'x'.center(70) + 'val'.center(20))
# for eps in [0.1, 0.01, 0.001]:
#     A = FirstOrderOptimisation(f, eps)
#     x = A.solve()
#     val = A.f(x)
#     print(str(eps).center(10) + str(x).center(70) + str(val).center(20))
#
#     A = SecondOrderOptimisation(f, eps)
#     x = A.solve()
#     val = A.f(x)
#     print(str(eps).center(10) + str(x).center(70) + str(val).center(20))




A = FirstOrderOptimisation(f, 0.0001)
res = A.solve_and_collect_data()

m, M = 1.95, 2.4

x0 = res['x0']
steps = res['steps']
true_x = Vector(0, 0)
path = res['path']

for x in path:
    print(A.grad(x).norm() / m, (true_x - x).norm())

print(steps)
#
# print(x0, steps)
#
# print(math.sqrt(2 / m * (f.f(x0) - f.f(true_x))) * (1 - m / (2 * M) * (1 + m / M))**(steps / 2))























# g = FunctionOfVector(4, '(cos(1/2 *(x1 + x2 + x3 + x4)) *sin(1/2 *(x1 - x2 + x3 - x4))* (x1 - x2 + x3 - x4 - cos(1/2 *(x1 + x2 + x3 + x4))* sin(1/2 *(x1 - x2 + x3 - x4))))/((x1 - x2)**2 + (x3 - x4)**2)')
# x = FirstOrderOptimisation(g, 0.01).solve()
#
# print(x, g.f(x))

# g = FunctionOfVector(4, '-(((x1/(x1**2+x3**2+5) - x2/(x2**2+x4**2+5))**2 + (x3/(x1**2+x3**2+5) - x4/(x2**2+x4**2+5))**2))/((x1 - x2)**2 + (x3 - x4)**2)')
# x = FirstOrderOptimisation(g, 0.001).solve()
#
# print(x, g.f(x))