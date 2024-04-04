from dataclasses import dataclass
import random

CAPACITY = 15

@dataclass
class Item:
    index: int
    weight: float
    value: float


def get_random_subset(items, capacity):
    items = items.copy()
    random.shuffle(items)
    for item in items:
        if capacity >= item.weight:
            yield item
            capacity -= item.weight

def knapsack_random(items, capacity, tries=20):
    best_subset = []
    best_value = 0
    for _ in range(tries):
        subset = list(get_random_subset(items, capacity))
        value = sum(list(map(lambda x: x.value, subset)))        
        if value > best_value:
            best_value = value
            best_subset = subset
    return best_subset


def knapsack_hill_climbing(items, capacity, children=3, changes=2):
    best_subset = list(get_random_subset(items, capacity))
    best_value = sum(list(map(lambda x: x.value, best_subset)))

    while True:
        unused_items = list(filter(lambda x: x not in best_subset, items))
        neighbors = []
        for _ in range(children):
            added_items = 0
            subset = random.sample(best_subset, k=len(best_subset)-changes)
            weight = sum(list(map(lambda x: x.weight, subset)))
            random.shuffle(unused_items)
            for item in unused_items:
                if added_items >= changes:
                    break
                if (weight + item.weight) <= capacity:
                    subset.append(item)
                    weight += item.weight
                    added_items += 1
            neighbors.append(subset)

        best_neighbor = None
        best_neighbor_value = 0
        for neighbor in neighbors:
            neighbor_value = sum(list(map(lambda x: x.value, neighbor)))
            if neighbor_value > best_neighbor_value:
                best_neighbor_value = neighbor_value
                best_neighbor = neighbor

        if best_neighbor_value > best_value:
            best_value = best_neighbor_value
            best_subset = best_neighbor
        else:
            break

    return best_subset


if __name__ == "__main__":
    total_items = [
        Item(0, 4, 12),
        Item(1, 3, 4),
        Item(2, 6, 5),
        Item(3, 6, 3),
        Item(4, 1, 8),
        Item(5, 4, 8),
        Item(6, 5, 12),
        Item(7, 4, 1)
    ]

    random_subset = knapsack_random(total_items, CAPACITY)
    random_weight = sum(list(map(lambda x: x.weight, random_subset)))
    random_value = sum(list(map(lambda x: x.value, random_subset)))
    print('Random ------------')
    print("subset: ", random_subset)
    print("subset-binary: ", list(map(lambda x: int(x in random_subset), total_items)))
    print('total-weight:', random_weight, ' total-value:', random_value)

    hill_subset = knapsack_hill_climbing(total_items, CAPACITY)
    hill_weight = sum(list(map(lambda x: x.weight, hill_subset)))
    hill_value = sum(list(map(lambda x: x.value, hill_subset)))
    print('Hill ------------')
    print("subset: ", hill_subset)
    print("subset-binary: ", list(map(lambda x: int(x in hill_subset), total_items)))
    print('total-weight:', hill_weight, ' total-value:', hill_value)
