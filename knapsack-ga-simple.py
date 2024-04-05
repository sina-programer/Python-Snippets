import pygad

def fitness_function(instance, solution, solution_idx):
    solution = unbinarize(solution)
    solution_weight = sum(map(lambda x: x[0], solution))
    solution_value = sum(map(lambda x: x[1], solution))
    if solution_weight > CAPACITY:
        return 0
    return solution_value

def binarize(solution):
    result = []
    for item in ITEMS:
        if item in solution:
            result.append(1)
        else:
            result.append(0)
    return result

def unbinarize(binary: list[int]):
    result = []
    for idx, state in enumerate(binary):
        if state == 1:
            result.append(ITEMS[idx])
    return result


CAPACITY = 15
ITEMS = [
    # weight, value
    (4, 12),
    (3, 4),
    (6, 5),
    (6, 3),
    (1, 8),
    (4, 8),
    (5, 12),
    (4, 1)
]


if __name__ == "__main__":
    ga = pygad.GA(
        fitness_func=fitness_function,
        gene_type=int,  # binary representation
        gene_space=[0, 1] * len(ITEMS),
        num_generations=50,
        num_parents_mating=2,
        sol_per_pop=10,
        parent_selection_type="sss",
        crossover_type="single_point",
        mutation_type="random",
        num_genes=len(ITEMS)
    )
    ga.run()

    solution_binary, solution_fitness, solution_idx = ga.best_solution()
    solution = unbinarize(solution_binary)
    solution_weight = sum(map(lambda x: x[0], solution))
    solution_value = sum(map(lambda x: x[1], solution))
    print(f"Final-Solution:  {''.join(map(str, solution_binary))}  Total-Value: {solution_value}  Total-Weight: {solution_weight}")
