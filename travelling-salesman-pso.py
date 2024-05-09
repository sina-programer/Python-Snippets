from collections import namedtuple
import numpy as np

Particle = namedtuple('Particle', ['position', 'velocity', 'best_pos', 'best_fitness'])

def euclidean(p1, p2):
   return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def distance_matrix(cities):
    n = len(cities)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i, j] = euclidean(cities[i], cities[j])
    return matrix

def calculate_fitness(position, distances):
    total_distance = 0
    num_nodes = len(position)
    for i in range(num_nodes):
        total_distance += distances[position[i], position[(i + 1) % num_nodes]]
    return total_distance

def pso(cities, n_particles=30, iters=1000, w=0.8, c1=2, c2=2):
    n = len(cities)
    particles = [
        Particle(
            (p := np.random.permutation(n)),
            np.zeros(n),
            np.copy(p),
            float('inf')
        )
        for _ in range(n_particles)
    ]
    global_best_position = np.zeros(n)
    global_best_fitness = float('inf')
    distances = distance_matrix(cities)
    for _ in range(iters):
        for idx, particle in enumerate(particles):
            fitness = calculate_fitness(particle.position, distances)
            if fitness < particle.best_fitness:
                particle = particle._replace(best_fitness=fitness, best_pos=np.copy(particle.position))
                particles[idx] = particle
            if fitness < global_best_fitness:
                global_best_fitness = fitness
                global_best_position = np.copy(particle.position)

        for idx, particle in enumerate(particles):
            r1 = np.random.rand(n)
            r2 = np.random.rand(n)
            particle = particle._replace(
                velocity=(
                    w * particle.velocity +
                    c1 * r1 * (particle.best_pos - particle.position) +
                    c2 * r2 * (global_best_position - particle.position)
                ),
                position=np.argsort(particle.position + particle.velocity)
            )
            particles[idx] = particle
    
    return global_best_position, global_best_fitness


if __name__ == "__main__":
    cities = np.array([
        (20, 52),
        (43, 50),
        (20, 84),
        (70, 65),
        (29, 90),
        (87, 83),
        (83, 23)
    ])

    best_route, best_distance = pso(cities)
    print("Best Route:", best_route)
    print("Best Distance:", best_distance)
