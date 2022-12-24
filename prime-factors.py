def is_prime(num):
    if num <= 1:
        return False

    if (num > 2) and (not num % 2):
        return False

    for n in range(2, num):
        if not num % n:
            return False

    return True


def get_factors(num):
    for i in range(2, num):
        j = num // i
        if i * j == num:
            return i, j


def get_prime_factors(num):
     result = []

     for n in get_factors(num):
          if is_prime(n):
               result.append(n)
          else:
               result.extend(get_prime_factors(n))

     return result


n = int(input('Enter a number to get its prime factors: '))

if n <= 1:
     print('Number you entered must be greater than 1!')

elif is_prime(n):
     print('Number you entered itself is prime!')

else:
     factors = get_prime_factors(n)
     result = []

     for factor in set(factors):
          frequent = factors.count(factor)
          result.append(f'{factor}^{frequent}')

     print(' × '.join(result))
