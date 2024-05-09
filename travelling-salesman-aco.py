from antsys import AntWorld, AntSystem
import numpy as np
import operator

def euclidean(p1, p2):
    return [
        np.sqrt(
            np.add(
                np.power(
                    np.subtract(
                        p1[-2],
                        p2[-2]
                    )
                    , 2
                ),
                np.power(
                    np.subtract(
                        p1[-1],
                        p2[-1]
                    ),
                    2
                )
            )        
        )
    ]

def cost(path):
    return sum(map(operator.attrgetter('info'), path))

cities = [
    ('a', 20, 52),
    ('b', 43, 50),
    ('c', 20, 84),
    ('d', 70, 65),
    ('e', 29, 90),
    ('f', 87, 83),
    ('g', 83, 23)
]
n = len(cities)
distances = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        distances[i, j] = euclidean(cities[i], cities[j])[0]
    
world = AntWorld(cities, euclidean, cost, lambda p, c: c.info)
optimizer = AntSystem(world=world, n_ants=100)
optimizer.optimize(max_iter=100, n_iter_no_change=20, verbose=False)
total_distance, best_path, _ = optimizer.g_best
print('Path:', ''.join(list(map(operator.itemgetter(0), best_path))))
print('Distance:', total_distance)
print(np.round(distances, 2))
