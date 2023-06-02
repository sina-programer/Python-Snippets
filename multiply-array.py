def multiply_recursive(array: list):
    if len(array) == 1:
        return array.pop()
 
    return array.pop() * multiply_recursive(array)
