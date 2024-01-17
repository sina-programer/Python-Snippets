def tri_recursive(i, d=2):
    if i <= 1:
        return i
    return i + tri_recursive(i-1, d+1)

def tri_static(i):
    if i <= 1:
        return i
    result = 1
    d = 2
    for _ in range(i-1):
        result += d
        d += 1
    return result


if __name__ == '__main__':
    print('recursive:', list(map(tri_recursive, range(10))))  # 0, 1, 3, 6, 10, 15, 21, 28, 36, 45
    print('static:', list(map(tri_static, range(10))))  # 0, 1, 3, 6, 10, 15, 21, 28, 36, 45
