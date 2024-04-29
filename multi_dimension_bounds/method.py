from simplex.lib import *
from multi_dimension.methods import *


class MultiDimensionWithBounds:
    def __init__(self, n: int, f_str: str, psi_str_arr, hi_str_arr, eps: float):
        self.eps = eps
        self.n = n

        self.function = FunctionOfVector(n, f_str)

        # psi arr of <= 0 bounds
        self.psi_str_arr = psi_str_arr

        # hi arr of == 0 bounds
        self.hi_str_arr = hi_str_arr

    def alpha(self, x: Vector):
        alpha_str = '0'
        for psi_str in self.psi_str_arr:
            psi_vector_function = FunctionOfVector(self.n, psi_str)
            if psi_vector_function.f(x) >= 0:
                alpha_str += f'+(({psi_str})**2)'
        for hi_str in self.hi_str_arr:
            alpha_str += f'+(({hi_str})**2)'

        return FunctionOfVector(self.n, alpha_str)

    def solve(self):
        mu = 1.1
        lbd = 1.7
        x = Vector(-5, -7)

        function_to_optimise_str = f'({self.function.f_str})+({mu})*({self.alpha(x).f_str})'
        function_to_optimise = FunctionOfVector(self.n, function_to_optimise_str)
        x_mu = FirstOrderOptimisation(function_to_optimise, self.eps).solve()
        x = x_mu

        n = 1
        print(n, mu, x_mu, self.alpha(x_mu).f(x_mu), mu * self.alpha(x_mu).f(x_mu), self.function.f(x_mu))

        while mu * self.alpha(x).f(x) > self.eps:
            x = x_mu
            mu = mu * lbd

            function_to_optimise_str = f'({self.function.f_str})+({mu})*({self.alpha(x).f_str})'
            function_to_optimise = FunctionOfVector(self.n, function_to_optimise_str)
            x_mu = FirstOrderOptimisation(function_to_optimise, self.eps * 100).solve()
            n += 1
            print(n, mu, x_mu, self.alpha(x_mu).f(x_mu), mu * self.alpha(x_mu).f(x_mu), self.function.f(x_mu))

        return x