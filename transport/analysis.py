from simplex.lib import Vector

x_sim = [4, 0, 0, 0, 3, 0, 1, 0, 0, 13, 4, 0, 2, 5, 0, 0, 14, 0, 0, 0]
x_trans = [4, 0, 0, 0, 3, 0, 14, 0, 0, 0, 4, 0, 2, 5, 0, 0, 1, 0, 0, 13]
x_book = [2, 0, 0, 0, 5, 0, 11, 0, 0, 3, 6, 0, 2, 3, 0, 0, 4, 0, 2, 8]

costs = [
    [8, 15, 23, 19, 9],
    [2, 1, 9, 10, 1],
    [1, 4, 8, 9, 3],
    [7, 3, 13, 10, 3]
]
m = len(costs)
n = len(costs[0])

sellers = [7, 14, 11, 14]
buyers = [8, 15, 2, 5, 16]

c = []
for row in costs:
    c.extend(row)

x_sim, x_trans, c, x_book = Vector(*x_sim), Vector(*x_trans), Vector(*c), Vector(*x_book)
C = (x_sim + x_trans) / 2

print(c * x_sim, c * x_trans, c * x_book)


hyperplanes = []  # array of (normal, point)

# m + n equations from table
for i in range(m):
    normal = Vector.empty(m * n)
    point = Vector.empty(m * n)
    for j in range(n):
        normal.set(i * n + j, costs[i][j])
    point.set(i * n, sellers[i] / costs[i][0])

    hyperplanes.append({'n': normal, 'p': point})

for j in range(n):
    normal = Vector.empty(m * n)
    point = Vector.empty(m * n)
    for i in range(m):
        normal.set(i * n + j, costs[i][j])
    point.set(j, buyers[j] / costs[0][j])
    hyperplanes.append({'n': normal, 'p': point})


# m * n from constraints
for i in range(m * n):
    normal = Vector.empty(m * n)
    point = Vector.empty(m * n)
    normal.set(i, 1)
    hyperplanes.append({'n': normal, 'p': point})


# find minimal distance to hyperplanes in each direction
dx = x_sim - x_trans
dx = dx / dx.norm()
dists = []
for hp in hyperplanes:
    normal = hp['n']
    point = hp['p']
    if dx * normal == 0: continue
    dist = (point - C) * normal / (dx * normal)
    dists.append(dist)

d1 = min(d for d in dists if d > 0)
d2 = max(d for d in dists if d < 0)
A = C + dx * d1
B = C + dx * d2

print(A)
print(B)

# any convex combination of A and B is a solution



def check_alignment(a, b, c):
    v1 = b - c
    v2 = a - c
    return v1 * v2 / v1.norm() / v2.norm()

print(check_alignment(x_sim, x_trans, x_book))
