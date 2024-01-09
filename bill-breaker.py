def static(amount, coins):
    result = []
    i = 0

    while amount > 0:
        coin = coins[i]
        if amount < coin:
            if coin == coins[-1]:
                result.append(-1)
                return result
            i += 1

        else:
            amount -= coin
            result.append(coin)

    return result


def recursive(amount, coins):
    if len(coins):
        coin = coins[0]
    elif amount > 0:
        return [-1]
    else:
        return []

    if amount < coin:
        return recursive(amount, coins[1:])

    result = []
    n = amount // coin
    amount -= (n * coin)
    result.extend([coin]*n)
    result.extend(recursive(amount, coins[1:]))
    return result


if __name__ == "__main__":
    money = int(input('How much money do you want to convert? '))
    coins = [100_000, 50_000, 10_000, 5_000, 2_000, 1_000, 500]

    print(f'Static:    {static(money, coins)}')
    print(f'Recursive: {recursive(money, coins)}')

    input('\nPress enter to exit...')
