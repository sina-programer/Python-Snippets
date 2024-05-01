from decimal import Decimal, ROUND_HALF_UP, ROUND_FLOOR, ROUND_UP
import operator


def DDA(x1, y1, x2, y2):
    steps = []
    M = (y2 - y1) / (x2 - x1)
    direction = +1 if abs(M)>1 else -1

    while True:
        steps.append((x1, y1))
        if x1==x2 and y1==y2:
            break        

        dy = y2 - y1
        dx = x2 - x1
        m = dy / dx  # compute after ensuring dx!=0

        if direction==1:
            x1 += int(Decimal(1/m).to_integral_value(rounding=ROUND_UP))
            y1 += 1

        else:
            x1 += 1
            y1 += int(Decimal(m).to_integral_value(rounding=ROUND_HALF_UP))

    return steps


def plot(X, Y, **kwargs):
    configs = default_scatter_configs | kwargs

    plt.plot([X[0], X[-1]], [Y[0], Y[-1]], ls='--', c='black')
    if len(X) > 2:
        plt.scatter(X.pop(0), Y.pop(0), label='start', **(configs | dict(c='green')))
        plt.scatter(X.pop(-1), Y.pop(-1), label='stop', **(configs | dict(c='red')))
        plt.legend()

    plt.scatter(X, Y, **configs)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

default_scatter_configs = {
    'marker':'s',
    's':400,
    'c':'teal'
}


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    plt.style.use('ggplot')

    a = (2, 2)
    b = (9, 5)

    points = DDA(*a, *b)
    X = list(map(operator.itemgetter(0), points))
    Y = list(map(operator.itemgetter(1), points))
    plot(X, Y)
