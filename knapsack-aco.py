from antsys import AntWorld, AntSystem

max_weight = 15

items = [
    (1, 4, 12),
    (2, 3, 4),
    (3, 6, 5),
    (4, 6, 3),
    (5, 1, 8),
    (6, 4, 8),
    (7, 5, 12),
    (8, 4, 1)
]

def knapsack_rules(start, end):
    return [0, 1]

def knapsack_cost(path):
    k_value = 0
    k_weight = 0
    for edge in path:
        if edge.info == 1:
            k_value += edge.end[2]
            k_weight += edge.end[1]
    cost = 1 / k_value
    if k_weight > max_weight:
        cost += 1
    else:
        for edge in path:
            if edge.info == 0 and edge.end[1] <= (max_weight - k_weight):
                cost += 1
    return cost

def knapsack_heuristic(path, candidate):
    k_weight = 0
    for edge in path:
        if edge.info == 1:
            k_weight += edge.end[1]
    if candidate.info == 1 and candidate.end[1] < (max_weight - k_weight):
        return 0
    elif candidate.info == 0:
        return 1
    else:
        return 2

def compute_cost(path):
    weight = 0
    value = 0
    for edge in path:
        if edge.info == 1:
            weight += edge.end[1]
            value += edge.end[2]
    return weight, value


if __name__ == "__main__":
    new_world = AntWorld(items, knapsack_rules, knapsack_cost, knapsack_heuristic, True, 1)
    optimizer = AntSystem(world=new_world, n_ants=50, rand_start=True, alpha=1, betha=1, evap_rate=0.8)
    optimizer.optimize(100, 10, verbose=False)
    _, _, path = optimizer.g_best
    total_weight, total_value = compute_cost(path)
    print('\nknapsack max weight =', max_weight)
    print('Total Weight:', total_weight, '  Total Value:', total_value)
    print('Items:', ''.join(list(map(lambda x: str(x.info), path))))
