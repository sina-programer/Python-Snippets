from functools import wraps
import time


def time_of(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"running {func.__name__} took {end-start} seconds.")
        return result

    return wrapper


def time_of_args(name, show_state):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            if show_state:
                print(f"running {name} took {end-start} seconds.")
            return result

        return wrapper

    return decorator


def _process(n):
    result = 0
    for i in range(n):
        result += i
    return result


@time_of
def process(n):
    return _process(n)

@time_of_args('SumBot', show_state=True)
def process_args(n): return _process(n)

process_args2 = time_of_args('UnknownBot', False)(_process)
