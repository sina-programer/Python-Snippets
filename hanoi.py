counter = 1

def tower(n, a, b, c):
    global counter

    if n == 1:
        print(f"{counter}_ Move {a} to {c}.")
        counter += 1

    else:
        tower(n-1, a, c, b)  # move all blocks to extra bar except greatest
        print(f"{counter}_ Move {a} to {c}.")  # move greatest block to dest bar
        counter += 1
        tower(n-1, b, a, c)  # move all blocks on greatest bloc


tower(2, 'A', 'B', 'C')
