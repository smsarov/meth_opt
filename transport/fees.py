from transport.transport import TransportProblem

costs = [
    [8, 15, 23, 19, 9],
    [2, 1, 9, 10, 1],
    [1, 4, 8, 9, 3],
]

sellers = [7, 14, 11]
buyers = [8, 15, 2, 5, 16]
fees = [4, 10, 1, 3, 12]

P = TransportProblem(costs, sellers, buyers)
P = TransportProblem.close(P)
P.costs[-1] = fees[:]

P.print()
P.solve()

