import math
import numbers
import random

class Vector:
    def __init__(self, *nums):
        self.nums = list(nums)
        self.len = len(nums)

    def __len__(self):
        return len(self.nums)

    def __str__(self):
        s = '( '
        for n in self.nums:
            s += str(n).center(5) + ' '
        s += ')'
        return s

    def __add__(self, other):

        if isinstance(other, str):
            return str(self) + other

        if self.len != other.len:
            return 'Error'

        return Vector(*[self.nums[i] + other.nums[i] for i in range(self.len)])

    def __sub__(self, other):
        if self.len != other.len:
            return 'Error'

        return Vector(*[self.nums[i] - other.nums[i] for i in range(self.len)])

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(*[self.nums[i] * other for i in range(self.len)])

        if isinstance(other, Vector):
            return sum([self.nums[i] * other.nums[i] for i in range(self.len)])

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return self * other

    def __truediv__(self, other):
        return self * (1 / other)

    def __neg__(self):
        return self * -1

    def __getitem__(self, *item):
        if isinstance(item[0], int) and 0 <= item[0] < self.len:
            return self.nums[item[0]]

        if isinstance(item[0], list):
            return Vector(*[self.nums[i] for i in item[0]])

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return all([self.nums[i] == other for i in range(self.len)])

        if isinstance(other, Vector):
            if other.len != self.len:
                return False
            return all([self.nums[i] == other.nums[i] for i in range(self.len)])

    def __le__(self, other):
        if isinstance(other, numbers.Number):
            return all([self.nums[i] <= other for i in range(self.len)])

    def __ge__(self, other):
        if isinstance(other, numbers.Number):
            return all([self.nums[i] >= other for i in range(self.len)])

    def to_matrix(self):
        return Matrix([Vector(n) for n in self.nums])


    @staticmethod
    def empty(n):
        return Vector(*[0 for _ in range(n)])

    @staticmethod
    def random(n):
        return Vector(*[random.random() for _ in range(n)])

    def set(self, index, value):
        if isinstance(index, list):
            k = 0
            for i in index:
                self.nums[i] = value.nums[k]
                k += 1

        if isinstance(index, int):
            self.nums[index] = value

    def T(self):
        return Matrix([Vector(n) for n in self.nums]).T()

    def norm(self):
        return math.sqrt(sum(n ** 2 for n in self.nums))

class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self.cols = []
        for i in range(self.rows[0].len):
            arr = []
            for j in range(len(self.rows)):
                arr.append(self.rows[j][i])

            self.cols.append(Vector(*arr))

        self.matrix = []
        for row in rows:
            self.matrix.append(row.nums)

        self.m = len(self.rows)
        self.n = len(self.cols)

        self._det = None
        self.inverse = None

    def det(self):
        if self._det is not None:
            return self._det

        self._det = 0

        if self.m != self.n:
            return 'Error'
        elif 1 == self.m:
            self._det = self.matrix[0][0]
        elif 2 == self.m:
            self._det = self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        else:
            for i in range(self.n):
                num = self.matrix[0][i] * ((-1) ** i)
                rows = list(range(1, self.m))
                cols = [n for n in range(self.n) if n != i]

                self._det += num * self[rows, cols].det()

        return self._det

    def __str__(self):
        s = ''
        for row in self.rows:
            s += str(row) + '\n'

        return s

    def __add__(self, other):
        if isinstance(other, Matrix) and self.m == other.m and self.n == other.n:
            return Matrix([self.rows[i] + other.rows[i] for i in range(self.m)])

    def __sub__(self, other):
        if isinstance(other, Matrix) and self.m == other.m and self.n == other.n:
            return Matrix([self.rows[i] - other.rows[i] for i in range(self.m)])

    def __mul__(self, other):
        if isinstance(other, Matrix) and self.n == other.m:
            rows = []
            for row in self.rows:
                rows.append(Vector(*[row * col for col in other.cols]))
            return Matrix(rows)

        if isinstance(other, Vector) and self.n == other.len:
            M = self * other.to_matrix()
            return Vector(*[row.nums[0] for row in M.rows])

        if isinstance(other, numbers.Number):
            return Matrix([row * other for row in self.rows])

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return self * other

        if isinstance(other, Vector):
            return other.to_matrix() * self

    def T(self):
        return Matrix(self.cols)

    def __getitem__(self, *item):
        M = item[0][0]
        N = item[0][1]

        if not (isinstance(M, list) and
                isinstance(N, list) and
                0 <= min(M) <= max(M) < self.m and
                0 <= min(N) <= max(N) < self.n):
            return self.matrix[M][N]

        return Matrix([self.rows[i][N] for i in M])

    def __xor__(self, other):
        if other != -1:
            return None

        if self.inverse:
            return self.inverse

        if self.det() == 0:
            return None

        rows = []
        for row in range(self.m):
            r = []
            for col in range(self.n):
                M = [k for k in range(self.m) if k != row]
                N = [n for n in range(self.n) if n != col]
                val = (-1) ** (row + col) * self[M, N].det()

                r.append(val)
            rows.append(Vector(*r))
        self.inverse = Matrix(rows).T() * (1 / self.det())
        return self.inverse

    @staticmethod
    def E(n):
        rows = []

        for i in range(n):
            rows.append(Vector(*[0 if j != i else 1 for j in range(n)]))

        return Matrix(rows)

    def push(self, M):

        rows = [Vector(*(self.rows[i].nums[:] + M.rows[i].nums[:])) for i in range(self.m)]
        return Matrix(rows)

    def to_vector(self):

        if self.m == 1:
            return Vector(*self.rows[0].nums)

        if self.n == 1:
            return Vector(*self.cols[0].nums)

        print('Impossible to convert this matrix to a vector')
        return AssertionError

    def norm(self):
        ans = 0
        for i in range(self.m):
            for j in range(self.n):
                ans += self.matrix[i][j] ** 2

        return math.sqrt(ans)



def combinations(elements, r):
    if r == 0:
        yield []
    elif r > len(elements):
        return
    else:
        for i in range(len(elements)):
            current_element = elements[i]
            remaining_elements = elements[i+1:]
            for combination in combinations(remaining_elements, r-1):
                yield [current_element] + combination