from dataclasses import dataclass
import operator
import pygad


@dataclass
class Item:
    idx: int
    weight: float
    value: float


class Items:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def add_item(self, item):
        if isinstance(item, Item):
            self.items.append(item)
        elif Items.is_iterable(item) and len(item)==2:
            weight, value = item
            self.items.append(
                Item(
                    self.length+1,
                    weight,
                    value
                )
            )

    def add_items(self, items):
        if not Items.is_iterable(items):
            raise TypeError
        for item in items:
            self.add_item(item)

    def represent(self):
        result = ''
        for item in ITEMS:
            if item in self:
                result += '1'
            else:
                result += '0'
        return result

    @classmethod
    def parse(cls, representation: str):
        items = cls()
        for i, item in zip(representation, ITEMS):
            if i == '1':
                items.add_item(item)
        return items

    @property
    def total_value(self): return sum(map(operator.attrgetter('value'), self.items))

    @property
    def total_weight(self): return sum(map(operator.attrgetter('weight'), self.items))

    @property
    def length(self): return len(self.items)

    @property
    def indexes(self): return list(map(operator.attrgetter('idx'), self.items))

    @staticmethod
    def is_iterable(x):
        try:
            len(list(x))
            return True
        except Exception:
            return False

    def __contains__(self, x):
        if isinstance(x, Item):
            x = x.idx
        if isinstance(x, int):
            return x in self.indexes


def fitness_function(instance, solution, solution_idx):
    items = Items.parse(''.join(map(str, solution)))
    if items.total_weight > CAPACITY:
        return 0
    # print(items.represent(), items.total_value, items.total_weight)  # 10001010 32 10
    return items.total_value


CAPACITY = 15
ITEMS = [
    Item(1, 4, 12),
    Item(2, 3, 4),
    Item(3, 6, 5),
    Item(4, 6, 3),
    Item(5, 1, 8),
    Item(6, 4, 8),
    Item(7, 5, 12),
    Item(8, 4, 1)
]


if __name__ == "__main__":
    total_items = Items(ITEMS)
    ga = pygad.GA(
        fitness_func=fitness_function,
        gene_type=int,  # binary representation
        gene_space=[0, 1] * total_items.length,
        num_generations=50,
        num_parents_mating=2,
        sol_per_pop=10,
        parent_selection_type="sss",
        crossover_type="single_point",
        mutation_type="random",
        num_genes=total_items.length
    )
    ga.run()

    solution, solution_fitness, solution_idx = ga.best_solution()
    final_items = Items.parse(''.join((map(str, solution))))
    print(f"Final-Solution:  {final_items.represent()}  Total-Value: {final_items.total_value}  Total-Weight: {final_items.total_weight}")
