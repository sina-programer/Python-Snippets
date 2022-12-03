import numpy as np


class Matrix:
    def __init__(self, matrix):
        self.matrix = np.array(matrix)

    def det(self, ic=0):
        if not Matrix.is_square(self.matrix):
            raise TypeError(f'Matrix must be square! (your matrix is {self.matrix.shape})')

        dim = len(self.matrix)
        if dim == 0:
            return 1

        if dim == 1:
            return int(self.matrix[0])

        elif dim == 2:
            return Matrix.det2(self.matrix)


        numbers = []
        coef = self.matrix[ic]

        for i, c in enumerate(coef):
            minor_matrix = self.minor(ic, i)
            numbers.append(minor_matrix.det() * c)

        result = 0
        n = -1 if is_odd(ic) else 1
        for num in numbers:
            result += (num * n)
            n *= -1

        return result

    def minor(self, i, j=0):
        shape = list(self.shape())
        rows = list(filter(lambda x: x != i, range(shape[0])))
        cols = list(filter(lambda x: x != j, range(shape[1])))

        return Matrix(np.take(self.matrix[rows], cols, axis=1))

    def shape(self):
        return self.matrix.shape

    def show(self):
        print(self.matrix)

    @classmethod
    def is_square(cls, matrix: np.array):
        shape = list(matrix.shape)
        return all(map(lambda dim: dim == shape[0], shape))

    @classmethod
    def det2(cls, matrix: np.array):
        return (matrix.diagonal().prod()) - (
                matrix[::-1].diagonal().prod())

    @classmethod
    def from_formula(cls, formula, shape):
        matrix = []

        for i in range(1, shape[0]+1):
            row = []

            for j in range(1, shape[1]+1):
                row.append(eval(formula))

            matrix.append(row)

        return cls(matrix)

    def __repr__(self):
        return f"Matrix({'×'.join(map(str, self.matrix.shape))})"



def is_odd(number):
    return number % 2


def make_matrix_formula_base():
    formula = input('Enter desired formula: ')  # for example: 2*i - j
    shape = list(map(int, input('Enter dimensions (x,y): ').split(',')))
    return Matrix.from_formula(formula, shape)



if __name__ == '__main__':
    matrix2 = Matrix([
        [2, 5],
        [5, 4]
    ])

    matrix3 = Matrix([
        [2, 3, 5],
        [3, 4, 10],
        [4, 5, 15]
    ])

    matrix4 = Matrix([
        [2, 0, 0, 0],
        [0, 4, 0, 0],
        [0, 0, 2, 0],
        [0, 0, 0, 3]
    ])

    print(matrix2.det())
    print(matrix3.det())
    print(matrix4.det())
