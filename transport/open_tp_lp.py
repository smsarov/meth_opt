from transport.transport import TransportProblem
from simplex.simplex import Problem

costs = [
    [8, 15, 23, 19, 9],
    [2, 1, 9, 10, 1],
    [1, 4, 8, 9, 3],
]

sellers = [7, 14, 11]
buyers = [8, 15, 2, 5, 16]


P = TransportProblem(costs, sellers, buyers)
P.solve()

LP = TransportProblem.to_linear_problem(P)
LP.print()

LP = Problem.to_canonical(LP)
LP.print()
LP.solve()
LP.write_solution()