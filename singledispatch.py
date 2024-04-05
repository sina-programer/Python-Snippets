from functools import singledispatch

@singledispatch
def fmax(x: int | float, *args):
    print('default dtype; unpacked numbers')
    _max = x
    for arg in args:
        if arg > _max:
            _max = arg
    return _max

@fmax.register(dict)
def fmax_dict(x):
    print('dictionary dtype; returns the key with greatest value')
    return max(x.keys(), key=x.get)

@fmax.register(list)
@fmax.register(tuple)
def _(x, key=None):
    print('subscriptable dtype [list, tuple]; returns the maximum value normally')
    return max(x, key=key)

@fmax.register
def fmax_dtype_set(x: set, key=None):
    print('set dtype; uses the subscriptable function inside')
    return _(x, key=key)


if __name__ == "__main__":
    TEST_CASES = [
        'fmax([1, 2, 3])',
        'fmax((1, 2, 3))',
        'fmax({1, 2, 3})',
        'fmax({"one":1, "two":2})',
        'fmax(1, 2, 3)',
        'fmax(1.5, 2.2)',
    ]

    for case in TEST_CASES:
        print(case + ':', eval(case))
