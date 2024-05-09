from pyswarms.single.global_best import GlobalBestPSO
import numpy as np

def fitness(position):
    total_value = np.sum(values * position)
    total_weight = np.sum(weights * position)
    if total_weight > max_weight:
        total_value = np.sum(values)
    else:
        total_value = -total_value
    return total_value

def objective(positions):
    positions = np.round(positions).astype(int)
    fitnesses = np.zeros(positions.shape[0])
    for i in range(positions.shape[0]):
        fitnesses[i] = fitness(positions[i])
    return fitnesses


if __name__ == "__main__":
    weights = np.array([4, 3, 6, 6, 1, 4, 5, 4])
    values = np.array([12, 4, 5, 3, 8, 8, 12, 1])
    max_weight = 15
    n = len(values)
    bounds = (np.zeros(n), np.ones(n))
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = GlobalBestPSO(n_particles=10, dimensions=n, options=options, bounds=bounds)
    best_cost, best_pos = optimizer.optimize(objective, iters=100)
    best_pos = np.round(best_pos).astype(int)  # Best position as 0/1
    print('Items: ', best_pos)
    print('Total Weight:', np.sum(best_pos * weights))
    print('Best value:', np.abs(fitness(best_pos)))
