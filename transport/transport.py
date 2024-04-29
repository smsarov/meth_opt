from simplex.simplex import *


def empty_table(m, n, filler=None):
    t = []
    for i in range(m):
        t.append([])
        for j in range(n):
            t[-1].append(filler)
    return t


def print_table(table, info_rows=None, info_cols=None, name=''):
    if not info_rows: info_rows = [''] * len(table)
    if not info_cols: info_cols = [''] * len(table[0])
    print()
    length = 8
    print(name.upper().center(length * len(table[0])))
    for i, row in enumerate(table):
        print(''.join([str(val).center(length) for val in row]) + ' | ' + str(info_rows[i]))
    print('__'.center(length) * len(table[0]) + '_|')
    print(''.join([str(val).center(length) for val in info_cols]))

    print()


class TransportProblem:
    def __init__(self, costs, sellers, buyers):
        self.costs = costs
        self.sellers = sellers
        self.buyers = buyers
        self.is_closed = sum(sellers) == sum(buyers)

        self.m = len(costs)
        self.n = len(costs[0])

        self.table = empty_table(self.m, self.n)
        self.potential_table = empty_table(self.m, self.n)
        self.start_cell = None

        self.solution = None

        print_table(self.costs, self.sellers, self.buyers, 'given')

    def print(self):
        print_table(self.costs, self.sellers, self.buyers)
        
    @staticmethod
    def to_linear_problem(problem):
        F = TransportProblem.close(problem)
        
        b = Vector(*F.sellers + F.buyers)

        c = []
        for i in range(F.m):
            for j in range(F.n):
                c.append(F.costs[i][j])
        c = Vector(*c)

        rows = []
        signs = []

        # upper part
        for i in range(F.m):
            row = [0] * (F.m * F.n)
            signs.append('<=')
            for j in range(i * F.n, i * F.n + F.n):
                row[j] = 1
            rows.append(Vector(*row))

        # lower part
        for i in range(F.n):
            row = [0] * (F.m * F.n)
            signs.append('>=')
            for j in range(F.m):
                row[j * F.n + i] = 1
            rows.append(Vector(*row))

        A = Matrix(rows)
        return Problem(A, b, c, signs=signs)
        
    @staticmethod
    def close(problem):
        diff = sum(problem.sellers) - sum(problem.buyers)
        if diff > 0:
            _buyers = problem.buyers[:] + [diff]
            _costs = []
            for row in problem.costs:
                _costs.append(row[:] + [0])
            return TransportProblem(_costs, problem.sellers[:], _buyers)
        elif diff < 0:
            _sellers = problem.sellers[:] + [-diff]
            _costs = []
            for row in problem.costs:
                _costs.append(row[:])
            _costs.append([0] * problem.n)
            return TransportProblem(_costs, _sellers, problem.buyers[:])
        else:
            return problem

    def calc_cost(self):
        cost = 0
        for i in range(self.m):
            for j in range(self.n):
                if self.table[i][j]:
                    cost += self.table[i][j] * self.costs[i][j]
        return cost

    def nw_method(self):
        i, j = 0, 0
        _sellers = self.sellers[:]
        _buyers = self.buyers[:]
        while i < self.m and j < self.n:
            val = min(_sellers[i], _buyers[j])
            _sellers[i] -= val
            _buyers[j] -= val

            self.table[i][j] = val

            if _sellers[i] == 0:
                i += 1
            if _buyers[j] == 0:
                j += 1

        print_table(self.table, _sellers, _buyers, 'North-West method')
        print(f'start cost is {self.calc_cost()}', '\n')

    def calculate_uv(self):
        u = [None] * self.m
        v = [None] * self.n
        u[0] = 0
        axis = 1
        unfilled_u = set(range(1, self.m))
        unfilled_v = set(range(self.n))
        elements = {0}  # reference row or col elements

        # copy self.table
        # table = []
        # for i in range(self.m):
        #     table.append([])
        #     for j in range(self.n):
        #         table[-1].append(self.table[i][j])

        # degeneracy check
        # equations = 0
        # for row in self.table:
        #     for n in row:
        #         if n is not None:
        #             equations += 1
        #
        # diff = (self.m + self.n - 1) - equations
        # for i in range(self.m):
        #     for j in range(self.n):
        #         if self.table[i][j] is None:
        #             if diff > 0:
        #                 table[i][j] = 0.000001
        #                 diff -= 1
        #             else: break

        # solve system of linear equations
        while len(unfilled_v) + len(unfilled_u):
            next_elements = set()
            if axis == 1:
                for i in elements:
                    for j in unfilled_v:
                        if self.table[i][j] is not None:
                            v[j] = self.costs[i][j] - u[i]
                            next_elements.add(j)

                unfilled_v.difference_update(next_elements)
            if axis == -1:
                for j in elements:
                    for i in unfilled_u:
                        if self.table[i][j] is not None:
                            u[i] = self.costs[i][j] - v[j]
                            next_elements.add(i)

                unfilled_u.difference_update(next_elements)

            if not next_elements:
                if axis == 1:
                    j = min(unfilled_v)
                    v[j] = 0
                    next_elements.add(j)
                    unfilled_v.remove(j)
                if axis == -1:
                    i = min(unfilled_u)
                    u[i] = 0
                    next_elements.add(i)
                    unfilled_u.remove(i)

            elements = next_elements
            axis *= -1
        return u, v

    def minimal_potential_cell(self):
        print_table(self.table, self.sellers, self.buyers, 'current plan')

        u, v = self.calculate_uv()
        self.potential_table = empty_table(self.m, self.n)
        min_potential_value, self.start_cell = float('inf'), (0,0)

        for i in range(self.m):
            for j in range(self.n):
                if self.table[i][j] is None:
                    val = self.costs[i][j] - u[i] - v[j]
                    self.potential_table[i][j] = val
                    if val < min_potential_value:
                        min_potential_value = val
                        self.start_cell = (i, j)

        print_table(self.potential_table, u, v, 'potential table')

    def is_optimal(self):
        min_potential_value = self.potential_table[self.start_cell[0]][self.start_cell[1]]
        if min_potential_value >= 0:
            print('the plan is optimal')
            print(f'final cost is {self.calc_cost()}')
            return True

        return False

    def find_path(self, path=(), draw=False):
        if not path:
            path = (self.start_cell,)

        if path[-1] == self.start_cell and len(path) >= 5:
            return path

        def is_possible(cell):
            if cell != self.start_cell and self.potential_table[cell[0]][cell[1]] is not None:
                return False

            if len(path) >= 2:
                prev_dx, prev_dy = path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]
                cur_dx, cur_dy = cell[0] - path[-1][0], cell[1] - path[-1][1]
                if prev_dx * cur_dx + prev_dy * cur_dy != 0:
                    return False

            if cell == self.start_cell and len(path) % 2 == 0:
                return len(path) >= 4

            return cell not in path

        cur_i, cur_j = path[-1]
        variants = []
        for i in range(self.m):
            cell = (i, cur_j)
            if i != cur_i and is_possible(cell):
                variants.append(cell)

        for j in range(self.n):
            cell = (cur_i, j)
            if j != cur_j and is_possible(cell):
                variants.append(cell)

        for v in variants:
            result = self.find_path((*path, v))
            if result:
                if draw:
                    s = empty_table(self.m, self.n, ' ')
                    # for i in range(len(result) - 1):
                    #     cell = result[i]
                    #     s[cell[0]][cell[1]] = '+' if i % 2 == 0 else '-'
                    # s[self.start_cell[0]][self.start_cell[1]] = "'+'"

                    for i in range(1, len(result)):
                        prev_cell = result[i - 1]
                        cur_cell = result[i]

                        dx = cur_cell[1] - prev_cell[1]
                        dy = cur_cell[0] - prev_cell[0]
                        if dx != 0: dx = int(dx / abs(dx))
                        if dy != 0: dy = int(dy / abs(dy))

                        pointer = prev_cell
                        while pointer != cur_cell:
                            if pointer == prev_cell:
                                s[pointer[0]][pointer[1]] = '□'
                            elif dx:
                                symbol = '-⟶' if dx > 0 else '⟵-'
                                s[pointer[0]][pointer[1]] = symbol
                            else:
                                symbol = '↑' if dy < 0 else '↓'
                                s[pointer[0]][pointer[1]] = symbol

                            pointer = (pointer[0] + dy, pointer[1] + dx)

                    s[self.start_cell[0]][self.start_cell[1]] = "⧆"

                    print_table(s, name='curve')
                return result

    def recalculate_plan(self):
        path = self.find_path(draw=True)[:-1]
        val = min(self.table[path[1][0]][path[1][1]], self.table[path[-1][0]][path[-1][1]])
        self.table[path[0][0]][path[0][1]] = val
        for k in range(1, len(path)):
            i, j = path[k]
            self.table[i][j] += ((-1) ** k) * val
            if not self.table[i][j]: self.table[i][j] = None

    def solve(self):
        T = TransportProblem.close(self)
        T.nw_method()
        while not T.solution:
            print('-' * 50 + '\n')
            T.calculate_uv()
            T.minimal_potential_cell()

            if T.is_optimal():
                T.solution = {
                    'plan': T.table,
                    'cost': T.calc_cost()
                }
                return T.solution

            T.recalculate_plan()



