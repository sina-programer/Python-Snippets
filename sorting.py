# https://www.geeksforgeeks.org/sorting-algorithms/

def bubble_sort(array):
    n = len(array)
    for i in range(n-1):
        swapped = False
        print(array)

        for j in range(n-i-1):
            if array[j] > array[j+1]:
                array[j+1], array[j] = array[j], array[j+1]
                swapped = True

        if not swapped:
            break

    return array


def quick_sort(array):
    if not array:
        return []

    pivot = array.pop(-1)
    left = list(filter(lambda x: x<pivot, array))
    right = list(filter(lambda x: x>pivot, array))
    return [*quick_sort(left), pivot, *quick_sort(right)]


def merge_sort(array):
    if len(array) <= 1:
        return array

    middle = len(array)//2
    left = array[:middle]
    right = array[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    
    a = l = r = 0
    while l < len(left) and r < len(right):
        if left[l] < right[r]:
            array[a] = left[l]
            l = l+1
        else:
            array[a] = right[r]
            r = r+1
        a += 1

    while l < len(left):
        array[a] = left[l]
        l = l+1
        a = a+1

    while r < len(right):
        array[a] = right[r]
        r = r+1
        a = a+1

    return array


def selection_sort(array):
    if not array:
        return array

    minimum = min(array)
    array.remove(minimum)
    return [minimum] + selection_sort(array)


def insertion_sort(array):
    for i in range(len(array)-1):
        if array[i] > array[i+1]:
            for j in range(i, -1, -1):
                if array[j] > array[j+1]:
                    array[j+1], array[j] = array[j], array[j+1]
                else:
                    break
    return array


def counting_sort(array):
    output = [0] * len(array)
    counting = [array.count(n) for n in range(max(array)+1)]
    cum_count = 0
    for i in range(len(counting)):
        cum_count += counting[i]
        counting[i] = cum_count

    for n in array[::-1]:
        count = counting[n]
        output[count-1] = n
        counting[n] = count-1

    return output


def pigeon_hole_sort(array):
    minimum = min(array)
    maximum = max(array)
    size = maximum - minimum + 1
    holes = [0] * size

    for x in array:
        holes[x - minimum] += 1

    i = 0
    for idx in range(size):
        while holes[idx] > 0:
            holes[idx] -= 1
            array[i] = minimum+idx
            i += 1

    return array


def radix_sort(array):
    digits = len(str(max(array)))
    for d in range(digits):
        c = 10 ** d
        array.sort(key=lambda x: x//c%10)
    return array



if __name__ == "__main__":
    numbers = [3, 1, 8, 22, 0, 4]
    print('Numbers:', numbers)
    print('Bobble-Sort:', bubble_sort(numbers.copy()))
    print('Quick-Sort:', quick_sort(numbers.copy()))
    print('Merge-Sort:', merge_sort(numbers.copy()))
    print('Selection-Sort:', selection_sort(numbers.copy()))
    print('Insertion-Sort:', insertion_sort(numbers.copy()))
    print('Counting-Sort:', counting_sort(numbers.copy()))
    print('Pigeon-Hole-Sort:', pigeon_hole_sort(numbers.copy()))
    print('Radix-Sort:', radix_sort(numbers.copy()))
