from single_dimension.methods import Golden
from sympy import *
from simplex.lib import Vector, Matrix


class FunctionOfVector:
    def __init__(self, n, f_str: str):
        self.n = n
        self.vars = symbols([f'x{n + 1}' for n in range(self.n)])
        self.f_str = f_str
        self.f_expr = sympify(f_str)
        self.f_array = lambdify(self.vars, self.f_expr)

    def f(self, x: Vector) -> float:
        return self.f_array(*x.nums)

    def grad(self, x: Vector) -> Vector:
        if x.len != self.n:
            raise ValueError('wrong dimensions')

        res = Vector.empty(self.n)

        for i in range(self.n):
            var_i = self.vars[i]
            derivative_expr = diff(self.f_expr, var_i)
            derivative_function = lambdify(self.vars, derivative_expr)

            res.set(i, derivative_function(*x.nums))

        return res

    def H(self, x: Vector) -> Matrix:
        if x.len != self.n:
            raise ValueError('wrong dimensions')

        rows = []
        for i in range(self.n):
            rows.append(Vector.empty(self.n))
            for j in range(self.n):
                var_i = self.vars[i]
                var_j = self.vars[j]
                derivative_expr = diff(self.f_expr, var_i, var_j)
                derivative_function = lambdify(self.vars, derivative_expr)

                rows[-1].set(j, derivative_function(*x.nums))
        return Matrix(rows)


class FirstOrderOptimisation:
    def __init__(self, function: FunctionOfVector, eps: float):
        self.n = function.n
        self.f = function.f
        self.grad = function.grad

        self.eps = eps

    def solve(self) -> Vector:
        x0 = Vector.random(self.n) * 10
        x = x0
        delta = 1e-6

        while self.grad(x).norm() > self.eps:
            alpha = Golden(
                lambda v: self.f(x - v * self.grad(x)),
                delta, 1,
                self.eps
            ).solve()
            x = x - alpha * self.grad(x)

        return x

    def show_orthogonality(self):
        res = self.solve_and_collect_data()
        path = res['path']

        for i in range(1, len(path)):
            x1 = path[i - 1]
            x2 = path[i]

            print(self.grad(x1), self.grad(x2), self.grad(x1) * self.grad(x2))

    def solve_and_collect_data(self):

        x0 = Vector.random(self.n) * 10

        res = {
            'x0': x0,
            'x': [],
            'alpha': [],
        }

        x = x0
        delta = 1e-6

        while self.grad(x).norm() > self.eps:
            alpha = Golden(
                lambda v: self.f(x - v * self.grad(x)),
                delta, 1,
                self.eps
            ).solve()
            x = x - alpha * self.grad(x)

            res['x'].append(x)
            res['alpha'].append(alpha)

        res['path'] = [res['x0']] + res['x']
        res['eps'] = self.eps
        res['ans'] = res['x'][-1]
        res['steps'] = len(res['path'])

        return res


class SecondOrderOptimisation:
    def __init__(self, function: FunctionOfVector, eps: float):
        self.n = function.n

        self.f = function.f
        self.grad = function.grad
        self.H = function.H

        self.eps = eps

        self.path = []

    def solve(self) -> Vector:
        lbd = 0.5

        x = Vector.random(self.n)
        self.path.append(x)
        alpha_0 = 1

        alpha = 1
        while self.grad(x).norm() > self.eps:
            p = -1 * (self.H(x) ^ -1) * self.grad(x)
            x_next = x + alpha * p

            alpha = alpha_0
            i = 0
            while self.f(x_next) - self.f(x) >= alpha * self.eps * self.grad(x) * p and i < 10:
                alpha *= lbd
                i += 1

            x = x_next
            self.path.append(x)

        return x
