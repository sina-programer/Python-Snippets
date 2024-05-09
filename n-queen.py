from itertools import combinations
import numpy as np
import time

def is_ponit_valid(point):
    for i in point:
        if not (0 <= i < n):
            return False
    return True

def max_distance(point):
    mx = 0
    for i in point:
        mx = max(i, n-i-1, mx)
    return mx

def get_neighbors(point, distance=0):
    n = len(point)
    for coefs in set(combinations([1, -1]*n, r=n)):
        yield tuple(i + distance*c for i, c in zip(point, coefs))

def generate_diagonals(point):
    points = []
    for idx in range(n):
        for p in list(filter(is_ponit_valid, set(get_neighbors(point, distance=idx)))):
            if p not in points:
                points.append(p)
    return points

def is_safe(b, i, j):
    for idx, row in enumerate(b):
        if row[j] == q:  # vertical
            return False
        if idx == i and q in row:  # horizontal
            return False
    for irow, icol in generate_diagonals((i, j)):  # diagonal
        if b[irow, icol] == q:
            return False
    return True

def get_valid_cols(b, r):  # get valid col positions for row=r in board
    cols = []
    for col in range(n):
        if is_safe(b, i=r, j=col):
            cols.append(col)
    return cols

def create_board(points=None, b=None):
    if b is None:
        b = np.zeros((n, n))
    if points is not None:
        for row, col in points:
            b[row, col] = q
    return b

def bfs(verbose=False):
    max_memory = 0
    nodes = 0
    queue = list(zip([0]*n, list(range(n)), [[]]*n))  # pairwise positions as (row, col, other queens' positions)
    while queue:
        row, col, points = queue.pop(0)
        nodes += 1
        point = (row, col)
        new_points = points + [point]
        board = create_board(points=new_points)
        next_row = row+1
        for new_col in get_valid_cols(board, r=next_row):
            queue.append((next_row, new_col, new_points))
        max_memory = max(max_memory, len(queue))
        if row==n-1 and verbose:
            print('-'*30)
            print(board)
    return nodes, max_memory

def dfs(points=None, row=0, nodes=0, max_memory=0, verbose=False):
    if points is None:
        points = []
    board = create_board(points=points)
    for col in get_valid_cols(board, r=row):
        point = (row, col)
        new_points = points + [point]
        _nodes, _max_memory = dfs(new_points, row=row+1, max_memory=len(points), verbose=verbose)
        max_memory = max(max_memory, _max_memory)
        nodes += _nodes + 1
        if row==n-1 and verbose:
            print(create_board(points=new_points))
    return nodes, max_memory


q = 1  # queen character (int)
n = 8  # board size

if __name__ == '__main__':
    # print(create_board(points=generate_diagonals((4, 2))))

    t1 = time.perf_counter()
    nodes1, memory1 = bfs(verbose=False)
    t2 = time.perf_counter()
    print(format('BFS', '-<35'))
    print('Nodes:', nodes1, '  Max-Memory:', memory1, '  ETA:', t2-t1)

    t3 = time.perf_counter()
    nodes2, memory2 = dfs(verbose=False)
    t4 = time.perf_counter()
    print(format('DFS', '-<35'))
    print('Nodes:', nodes2, '  Max-Memory:', memory2, '  ETA:', t4-t3)
