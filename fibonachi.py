from functools import wraps
import time


def timer(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Running {func.__name__} took {end_time-start_time} seconds")
        return result

    return wrapper


def static(n):
    if n <= 1:
        return n

    result = 1
    a, b = 0, 1
    for _ in range(n-1):
        result += a
        a, b = b, b+a

    return result


def dynamic(n, memory={}):
    if n in [0, 1]:
        return n

    if n in memory:
        return memory[n]

    result = dynamic(n-1, memory) + dynamic(n-2, memory)
    memory[n] = result
    return result


def recursive(n):
    if n < 2:
        return n
    return recursive(n-1) + recursive(n-2)


print('Static(500):', timer(static)(500))
print('Dynamic(500):', timer(dynamic)(500))
print('Recusive(30):', timer(recursive)(30))

print('Static:', list(map(static, range(10))))
print('Dynamic:', list(map(dynamic, range(10))))
print('Recursive:', list(map(recursive, range(10))))
