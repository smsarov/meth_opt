from single_dimension.methods import *


def f(x):
    return x ** 2 - 2 * x + math.exp(-x)


print('eps'.center(10), 'dichotomy'.center(10), 'a'.center(20), 'b'.center(20),  'golden'.center(10), 'a'.center(20), 'b'.center(20))
for eps in [0.1, 0.01, 0.001, 0.0001]:
    d = Dichotomy(f, 1, 2, eps)
    d.solve()
    g = Golden(f, 1, 2, eps)
    g.solve()

    print(str(eps).center(10), str(d.count).center(10), str(d.a).center(20), str(d.b).center(20), str(g.count).center(10), str(g.a).center(20), str(g.b).center(20) )