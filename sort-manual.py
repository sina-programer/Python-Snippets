import itertools


def sort(numbers):
    numbers = numbers.copy()
    indexes = list(range(len(numbers)))
    for i, j in itertools.combinations(indexes, 2):
        if numbers[i] > numbers[j]:
            temp = numbers[i]
            numbers[i] = numbers[j]
            numbers[j] = temp

    return numbers
