import numpy as np

rows = 5
cols = 3
cleaned_rooms = 0
total_rooms = rows * cols
matrix = np.random.randint(0, 2, (rows, cols))
print(matrix)

states = {
    0: 'clean',
    1: 'dirty'
}
actions = {
    0: 'nothing',
    1: 'cleaning'
}

for x in range(matrix.shape[0]):
    for y in range(matrix.shape[1]):
        state = matrix[x, y]
        if (x == rows-1) and (y == cols-1):
            print(f'Agent in room ({x}, {y}); state={states[state]}; action={actions[state]}')
        else:
            print(f'Agent in room ({x}, {y}); state={states[state]}; action={actions[state]} and move ', end='')
            if y == cols-1:
                print('down.')
            else:
                print('right.')

        if state == 1:
            cleaned_rooms += 1
            matrix[x, y] = 0

print(f'All the rooms checked and {cleaned_rooms} rooms were cleaned!')
print(matrix)
