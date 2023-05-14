def sum_digits_numerical(number):
    result = 0
    while number:
        result += (number % 10)
        number //= 10

    return result


def sum_digits_str(number):
    result = 0
    for digit in str(number):
        result += int(digit)

    return result

def sum_digits_str_advanced(number):
    return sum(map(int, str(number)))


if __name__ == "__main__":
    number = 123
    print('Number: ', number)
    print('Numerical Sum: ', sum_digits_numerical(number))
    print('String Sum: ', sum_digits_str(number))
    print('Advanced String Sum: ', sum_digits_str_advanced(number))
