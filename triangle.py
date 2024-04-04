def simple_triangle(rows):
    for row in range(rows+1):
        for space in range(rows-row):
            print(' ', end='')

        for star in range(row):
            print('*', end=' ')

        print()


def stroke_triangle(rows):
    for row in range(rows-1):
        for space in range(rows-row):
            print(' ', end='')

        print('*', end='')
        for space in range(row*2 - 1):
            print(end=' ')
        print('*', end=' ') if row else print(end=' ')
        print()

    print(end=' ')
    for star in range(rows):
        print('*', end=' ')
