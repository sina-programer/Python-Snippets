from itertools import cycle
from time import sleep

def normal(n):
    for _ in range(n):
        for char in _CHARS:
            print(f'\rLoading {char}', end='')
            sleep(DELAY)

def iterating(n):
    for _ in range(n):
        print(f'\rLoading {next(CHARS)}', end='')
        sleep(DELAY)


_CHARS = '/-\|'
CHARS = iter(cycle(_CHARS))
DELAY = .15
LAPS = 5

normal()
