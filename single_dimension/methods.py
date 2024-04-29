import math


class Dichotomy:
    def __init__(self, f, a, b, eps=0.01):
        self.a = min(a, b)
        self.b = max(a, b)
        self.__f__ = f
        self.eps = eps

        self.count = 0

    def f(self, x):
        self.count += 1
        return self.__f__(x)

    def solve(self):
        step = 0
        delta = self.eps / 4

        while self.b - self.a > self.eps:
            step += 1
            middle = (self.a + self.b) / 2
            x1, x2 = middle - delta, middle + delta
            y1, y2 = self.f(x1), self.f(x2)

            if y1 < y2:
                self.b = x2
            else:
                self.a = x1

        return (self.a + self.b) / 2


class Golden:
    def __init__(self, f, a, b, eps=0.01):
        self.a = min(a, b)
        self.b = max(a, b)
        self.__f__ = f
        self.eps = eps

        self.count = 0

    def f(self, x):
        self.count += 1
        return self.__f__(x)

    def solve(self):
        phi = (3 - math.sqrt(5)) / 2
        psi = (math.sqrt(5) - 1) / 2

        x1 = self.a + phi * (self.b - self.a)
        x2 = self.a + psi * (self.b - self.a)
        y1 = self.f(x1)
        y2 = self.f(x2)

        step = 1

        while self.b - self.a > self.eps:
            step += 1
            if y1 < y2:
                self.b = x2
                x2 = x1
                y2 = y1
                x1 = self.a + psi * (x2 - self.a)
                y1 = self.f(x1)

            else:
                self.a = x1
                x1 = x2
                y1 = y2
                x2 = self.b - psi * (self.b - x1)
                y2 = self.f(x2)

        return (self.a + self.b) / 2
