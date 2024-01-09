def diagonal(matrix):
    return [l[i] for i, l in enumerate(matrix)]

def constant_matrix(m, n, fill=0):
    return [[fill for j in range(n)] for i in range(m)]

def transpose(matrix):
    return [[l[i] for l in matrix] for i in range(len(matrix))]

def magic_matrix(n):
    matrix = constant_matrix(n, n, fill=0)
    num = 1
    i = 0
    j = len(matrix) // 2

    while True:
        i %= n  # keep in matrix size
        j %= n

        if matrix[i][j]:  # not equal to zero
            j += 1
            i += 2
        else:
            matrix[i][j] = num
            num += 1
            i -= 1
            j -= 1

        if num == (n**2 + 1):
            break

    return matrix


n = int(input('Enter dimention length for matrix: '))
matrix = magic_matrix(n)
matrix_t = transpose(matrix)
s_diameter = diagonal(matrix[::-1])[::-1]
b_diameter = diagonal(matrix)

from pprint import pprint
pprint(matrix)

print(f'\nSlash diameter: {s_diameter}')
print(f'Backslash diameter :{b_diameter}')
print(f'\nSum rows: {[sum(l) for l in matrix]}')
print(f'Sum cols: {[sum(l) for l in matrix_t]}')
print(f'Sum Slash diameter: {sum(s_diameter)}')
print(f'Sum Backslash diameter: {sum(b_diameter)}')

input('\n\nPress enter to exit...')
