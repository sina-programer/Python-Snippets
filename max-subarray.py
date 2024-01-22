def max_crossing_subarray(arr, low, mid, high):
    left_sum = float('-inf')
    max_left = 0
    max_right = 0
    sum = 0
    for i in range(mid, low - 1, -1):
        sum += arr[i]
        if sum > left_sum:
            left_sum = sum
            max_left = i

    right_sum = float('-inf')
    sum = 0
    for j in range(mid + 1, high + 1):
        sum += arr[j]
        if sum > right_sum:
            right_sum = sum
            max_right = j

    return max_left, max_right, left_sum+right_sum


def max_subarray(arr, low, high):
    if low == high:
        return low, high, arr[low]

    mid = (low + high) // 2
    left_low, left_high, left_sum = max_subarray(arr, low, mid)
    right_low, right_high, right_sum = max_subarray(arr, mid + 1, high)
    cross_low, cross_high, cross_sum = max_crossing_subarray(arr, low, mid, high)

    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_low, left_high, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_low, right_high, right_sum
    return cross_low, cross_high, cross_sum


def division(arr):
    low, high, maximum_sum = max_subarray(arr, 0, len(arr)-1)
    return arr[low:high+1]


def brute_force(numbers):
    maximum = numbers[0]
    right = 1
    left = 1

    for i in range(len(numbers)):
        current_sum = 0
        for j in range(i, len(numbers)):
            current_sum += numbers[j]
            if current_sum > maximum:
                maximum = current_sum
                left = i
                right = j

    return numbers[left:right+1]


if __name__ == '__main__':
    numbers = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    print('Numbers:', numbers)

    brute_array = brute_force(numbers)
    print(f"Brute-Force Method \nsum: {sum(brute_array)}")
    print(brute_array)
    print()

    division_array = division(numbers)
    print(f"Division Method \nsum: {sum(division_array)}")
    print(division_array)
