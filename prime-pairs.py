def is_prime(x):
    if x <= 1:
        return False

    if (not x%2) and (x > 2):
        return False

    for n in range(2, x):
        if not x%n:
            return False

    return True


def primes(stop):
    yield 2
    for n in range(3, stop+1, 2):
        if is_prime(n):
            yield n


def prime_pairs(num):
    for n in primes(num):
        n2 = num - n
        if is_prime(n2):
            yield (n, n2)


if __name__ == "__main__":
    number = 55

    if is_prime(number):
        print(f"{number} itself is a prime!")
    elif number <= 3:
        print("You must enter numbers bigger than 3!")
    else:
        print("The prime-pairs: ", list(prime_pairs(number)))
