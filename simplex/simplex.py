from .lib import *


class Problem:
    def __init__(self, A, b, c, signs="=", constraints=">=", target='min', actual_x=None):
        self.actual_x = actual_x or A.n
        self.target = target

        self.A = A
        self.b = b
        self.c = c

        self.signs = []
        if isinstance(signs, str):
            match signs:
                case "=":
                    self.signs = ['='] * len(b.nums)
                case "<=":
                    self.signs = ['<='] * len(b.nums)
                case ">=":
                    self.signs = ['>='] * len(b.nums)
                case _:
                    raise ValueError('innappropriate sign')
        elif isinstance(signs, list):
            if len(signs) != len(b.nums):
                raise ValueError('check signs length')
            for s in signs:
                if s not in ['=', '<=', '>=']:
                    raise ValueError('innappropriate signs')
            self.signs = signs

        self.constraints = []
        if isinstance(constraints, str):
            match constraints:
                case "":
                    self.constraints = ['>='] * self.actual_x
                case ">=":
                    self.constraints = ['>='] * self.actual_x
                case "<=":
                    self.constraints = ['<='] * self.actual_x
                case "<>":
                    self.constraints = ['<>'] * self.actual_x
        elif isinstance(constraints, list):
            if len(constraints) != A.n:
                raise ValueError('check constraints length')
            for s in constraints:
                if s not in ['>=', '<=', '<>']:
                    raise ValueError('innappropriate constraints')
            self.constraints = constraints

        self.solution = None

    def print(self):
        m = self.A.m // 2
        print()
        for i in range(self.A.m):
            s = ''
            s += str(self.A.rows[i])

            if i == m:
                s += ' * x  '
            else:
                s += '      '

            s += '' + self.signs[i] + ' '
            s += ' ' + str(self.b[i]) + ' '

            print(s)
        print()

        for i in range(self.A.n):
            s = ''
            s += 'x_' + str(i + 1)
            s += ' ' + self.constraints[i] + ' 0 '
            print(s)
        print()

        s = 'f(x) = '
        for i in range(self.A.n):
            s += str(self.c.nums[i]) + '*x_' + str(i + 1) + ' + '
        print(s[:-3] + ' -> ' + self.target)

    @staticmethod
    def to_canonical(P):
        rows = [P.A.rows[i].nums[:] for i in range(P.A.m)]
        signs = P.signs[:]
        constraints = P.constraints[:]
        b = P.b.nums[:]
        c = P.c.nums[:]
        target = P.target

        def swap_signs(sign):
            if sign == '>=':
                return '<='
            if sign == '<=':
                return '>='
            if sign == '=':
                return '='

        recount = []

        # vector b must be >= 0
        for i in range(P.A.m):
            if b[i] < 0:
                rows[i] = [-n for n in rows[i]]
                signs[i] = swap_signs(signs[i])
                b[i] = b[i] * (-1)

        # all signs must be '='
        # if '<=' substact y>0, if '>=' add y>0
        if '>=' in signs or '<=' in signs:
            for i in range(P.A.m):
                row = [0] * P.A.m
                if signs[i] == '>=':
                    signs[i] = '='
                    row[i] = -1
                elif signs[i] == '<=':
                    signs[i] = '='
                    row[i] = 1
                rows[i] += row
                constraints.append('>=')
                c.append(0)

        # all constraints must be '>='
        for i in range(len(constraints)):
            if constraints[i] == '<=':
                for row in rows:
                    row[i] *= -1
                    c[i] *= -1

            if constraints[i] == '<>':
                for row in rows:
                    row += [row[i], -row[i]]
                    row[i] = 0

                c += [c[i], -c[i]]
                c[i] = 0

                constraints += ['>=', '>=']

        # target must be 'min'
        if target == 'max':
            for i in range(len(c)):
                c[i] *= -1

        return Problem(Matrix([Vector(*row) for row in rows]),
                Vector(*b),
                Vector(*c),
                signs,
                constraints,
                target,
                actual_x=P.actual_x)

    def f(self, x):
        return abs(self.c * x)

    def write_solution(self):
        ans = [0] * self.actual_x
        for i in range(self.actual_x):
            if self.constraints[i] == '<=':
                ans[i] = self.solution[i] * (-1)
            elif self.constraints[i] == '>=':
                ans[i] = self.solution[i]

        n = -2
        for i in range(self.actual_x - 1, -1, -1):
            if self.constraints[i] == '<>':
                v = self.solution.nums[n] - self.solution.nums[n + 1]
                ans[i] = v
                n -= 2

        print('optimal solution is:')
        print([round(n, 2) for n in ans])

        print('the respective cost is: ')
        print(self.f(self.solution))

    def solve(self, x=None):
        N = list(range(self.A.n))
        M = list(range(self.A.m))

        if x is None:
            _A = self.A.push(Matrix.E(self.A.m))
            _b = self.b
            _c = Vector(*[0] * self.A.n + [1] * self.A.m)
            x0 = Vector(*[0] * self.A.n + self.b.nums)

            _x = Problem(_A, _b, _c).solve(x0)
            print(' \n  SUBPROBLEM IS SOLVED')
            x1 = _x[N]
            print(f'  start vector is: {x1}\n')
            y1 = _x[list(range(self.A.n, _x.len))]
            for i in M:
                if y1[i] > 0:
                    print('S is empty')
                    return None

            return self.solve(x1)

        N_plus = [n for n in N if x[n] > 0]
        N_null = [n for n in N if x[n] == 0]
        columns_to_push = self.A.m - len(N_plus)

        combs = combinations(N_null, columns_to_push)
        N_cur = []
        for indexes in combs:
            N_cur = N_plus + indexes
            if self.A[M, N_cur].det() != 0:
                break

        while combs:
            nulls = list(set(N_cur) - set(N_plus))

            L = list(set(N) - set(N_cur))
            B = self.A[M, N_cur] ^ -1

            d = Vector.empty(self.A.n)

            d.set(L, (self.c[L].T() - self.c[N_cur].T() * B * self.A[M, L]).to_vector())

            if d[L] >= 0:
                print('optimal solution found')
                self.solution = x
                print(N_cur)
                return x

            j = [[j for j in L if d[j] < 0][0]]

            u = Vector.empty(self.A.n)
            u.set(N_cur, B * self.A[M, j].to_vector())
            u.set(j, Vector(-1))

            if u[N_cur] <= 0:
                print('is not bounded from the bottom')
                return 'Infinity'

            is_degenerate = len(N_plus) != self.A.m

            if not is_degenerate:
                theta = float('inf')
                for i in N_cur:
                    if u[i] > 0:
                        theta = min(theta, x[i] / u[i])
                x_next = x - theta * u
                print('not degenerate')
                return self.solve(x_next)

            if u[nulls] <= 0:
                theta = float('inf')
                for i in N_cur:
                    if u[i] > 0:
                        theta = min(theta, x[i] / u[i])
                x_next = x - theta * u
                print('u_nulls')
                return self.solve(x_next)

            print('change basis')
            for indexes in combs:
                N_cur = N_plus + indexes
                if self.A[M, N_cur].det() != 0:
                    break
