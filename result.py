from typing import List

from item import Item
from quality_population_enum import QualityPopulationEnum
from solution import Solution


class Result:
    def __init__(self, solution: Solution, items: List[Item], number_generation: int, number_population: int, nb_best: int, proba_crossover: float, proba_mutation: float, type_init_population: QualityPopulationEnum, execution_time: float):
        self.profit = solution.profit
        self.weight = solution.weight

        self.selected_items = []
        for item_index in solution.items_indexes:
            self.selected_items.append(items[item_index].id)

        self.number_generation = number_generation
        self.number_population = number_population
        self.nb_best = nb_best
        self.proba_crossover = proba_crossover
        self.proba_mutation = proba_mutation
        self.type_init_population = type_init_population
        self.execution_time = execution_time

    def get_type_init_population(self) -> str:
        return self.type_init_population.name

    def items_list_string(self) -> str:
        return ','.join(map(str, self.selected_items))

    def result_to_csv(self):
        return [self.profit, self.weight, self.items_list_string(), self.number_generation, self.number_population, self.nb_best, self.proba_crossover, self.proba_mutation, self.get_type_init_population(), self.execution_time]
