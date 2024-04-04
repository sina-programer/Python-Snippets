import time


def max_crossing_subarray(arr, low, mid, high):
    sum_left = float('-inf')
    max_left = 0
    summation = 0
    for i in range(mid, low-1, -1):
        summation += arr[i]
        if summation > sum_left:
            sum_left = summation
            max_left = i

    sum_right = float('-inf')
    max_right = 0
    summation = 0
    for j in range(mid+1, high+1):
        summation += arr[j]
        if summation > sum_right:
            sum_right = summation
            max_right = j

    return max_left, max_right, sum_left+sum_right


def max_subarray(arr, low, high):
    if low == high:
        return low, high, arr[low]

    mid = (low + high) // 2
    left_low, left_high, left_sum = max_subarray(arr, low, mid)
    right_low, right_high, right_sum = max_subarray(arr, mid+1, high)
    cross_low, cross_high, cross_sum = max_crossing_subarray(arr, low, mid, high)

    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_low, left_high, left_sum
    elif right_sum >= left_sum and right_sum >= cross_sum:
        return right_low, right_high, right_sum
    return cross_low, cross_high, cross_sum


def division(arr):
    low, high, maximum_sum = max_subarray(arr, 0, len(arr)-1)
    return arr[low:high+1]


def brute_force(array):
    maximum = array[0]
    right = 1
    left = 1

    for i in range(len(array)):
        current_sum = 0
        for j in range(i, len(array)):
            current_sum += array[j]
            if current_sum > maximum:
                maximum = current_sum
                left = i
                right = j

    return array[left:right+1]


if __name__ == "__main__":
    numbers = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]
    print('Numbers:', numbers, '\n')

    start_time = time.perf_counter()
    brute_array = brute_force(numbers)
    print(f"Brute-Force Method \nsum: {sum(brute_array)}")
    print(brute_array)
    stop_time = time.perf_counter()
    print('running brute-force took', stop_time-start_time, 'seconds')
    print()

    start_time = time.perf_counter()
    division_array = division(numbers)
    print(f"Division Method \nsum: {sum(division_array)}")
    print(division_array)
    stop_time = time.perf_counter()
    print('running division took', stop_time-start_time, 'seconds')
