from .simplex import *

u = 0.4
v = 0.2



A = Matrix([
            Vector(-0.4, -0.2, 0.3, 0.3, 0.3, -1, 0),
            Vector(-0.1, 0.1, 0.3, 0.1,  0,   0, -1),
            Vector(  1,    1,   1,   1,   1,  0,  0)
        ])


b = Vector(0, 0, 1)
c = Vector(4, 4.5, 5.8, 6, 7.5, 0, 0)

P = Problem(A, b, c)
P.solve()
x = P.solution
P.write_solution()

B = A[[0, 1, 2], [1, 2, 6]]
arr = []
for b1 in [-0.01, -0.005, 0, 0.005, 0.01]:
    for b2 in [-0.01, -0.005, 0, 0.005, 0.01]:
        for b3 in [0.98, 0.99, 1, 1.01, 1.02]:
            try:
                _b = Vector(b1, b2, b3)
                _P = Problem(A, _b, c)
                _P.solve()
                _x = _P.solution

                dx = (x - _x).norm()
                db = (b - _b).norm()
                arr.append(dx / db)
            except:
                pass

print(arr)
print(max(arr))
print((B ^ -1).norm())












#
# A = Matrix([
#     Vector(2, -1, 1), #<=1
#     Vector(-1, 1, -1), #<= 1
#     Vector(1, -2, 3), #<=-6
#     Vector(1, 3, 1), #<=2
#     Vector(2, 1, -3) #<=12
# ])
#
# #  нет ограничений на знак
#
# c = Vector(3, 2, 1) #->max

# A = Matrix([
#     Vector(2, -1, 1),
#     Vector(-1, 1, -1),
#     Vector(1, -2, 3),
#     Vector(1, 3, 1),
#     Vector(2, 1, -3)
# ])
# b = Vector(1, 1, -6, 2, 12)
# c = Vector(3, 2, 1)
#
# P = Problem(A, b, c, signs='<=', constraints='<>', target='max')
# P.print()
# Q = Problem.to_canonical(P)
# Q.solve()
# Q.write_solution()
#
#
# _A = A.T()
# _c = b
# _b = c
#
# _P = Problem(_A, _b, _c, signs='=', constraints='>=', target='min')
# _Q = Problem.to_canonical(_P)
# _Q.solve()
# _Q.write_solution()


