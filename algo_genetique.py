import random
import numpy
from typing import List

from item import Item
from solution import Solution


# TODO Vérifier temps éxécution

def generate_random_index(end, list_item_already_generated):
    while True:
        random_number = random.randint(0, end - 1)
        if random_number not in list_item_already_generated:
            return random_number


# Le nombre d'item dans le sac peut faire partie des tests
# (tester avec une pop init qui a bcp d'item de base ou une avec peu) et voir les différences
def create_initial_population(n: int, items: List[Item]) -> List[Solution]:
    """
    Créer la population initiale de solutions.
    Une solution a la taille du nombre d'item et un index de la solution correspond à un item de la liste d'items.
    Si on a 1 alors l'item est dans le sac.
    Si on a 0 alors l'item n'est pas dans le sac.

    :param n: le nombre de solutions à créer
    :param items: la liste des items
    :return: la liste des solutions.
    """
    populations = []
    index_already_generated = []

    for i in range(n):
        random_index = generate_random_index(len(items), index_already_generated)

        solution = Solution()
        solution.add_item(random_index, items[random_index])

        populations.append(solution)

    return populations


def update_best_solution(population: List[Solution], items: List[Item]) -> Solution:
    """
    Récupère la meilleure solution de la population

    :param population: une liste de solution avec 1 pour un item et 0 pour pas d'item.
    :param items: la liste d'items
    :return: la meilleure solution de la population
    """
    best_solution_with_index = population[0].profit, 0

    for i in range(1, len(population)):
        if population[i].profit > best_solution_with_index[0]:
            best_solution_with_index = population[i].profit, i

    return population[best_solution_with_index[1]]


def roulette_wheel_reproduction(population: List[Solution]) -> List[Solution]:
    """
    Reproduit les solutions sélectionnée en fonction de leur profit

    :param population: une liste de solution avec 1 pour un item et 0 pour pas d'item.
    :return: une liste de solution avec doublons de solution en fonction de la reproduction.
    """
    selected_solutions_for_reproduction = []

    total_profit = sum(solution.profit for solution in population)

    reproduction_proportion_for_each_solution = []

    last_proportion = 0
    for i in range(len(population)):
        reproduction_proportion = population[i].profit / total_profit
        reproduction_proportion_for_each_solution.append(last_proportion + reproduction_proportion)
        last_proportion += reproduction_proportion

    solution_number_to_add = numpy.zeros(len(population), dtype=int).tolist()

    for index_solution in range(len(population)):
        random_probability = numpy.random.random()

        for index, reproduction_proportion in enumerate(reproduction_proportion_for_each_solution):
            if random_probability <= reproduction_proportion:
                solution_number_to_add[index] += 1
                break

    for index, number_to_add in enumerate(solution_number_to_add):
        for _ in range(number_to_add):
            selected_solutions_for_reproduction.append(population[index])

    return selected_solutions_for_reproduction


def best_solutions_reproduction(nb_best: int, population: List[Solution]) -> List[Solution]:
    """
    Retourne les nb_best meilleures solutions

    :param nb_best: le nombre de meilleures solutions qu'on veut garder.
    :param population: une liste de solution avec 1 pour un item et 0 pour pas d'item.
    :param items: liste d'item.
    :return: les nb_best solutions gardées.
    """
    population_sort_by_profit = sorted(population, key=lambda solution: solution.profit, reverse=True)

    return population_sort_by_profit[:nb_best]


def crossover(population: List[List[int]], items: List[Item], max_capacity: int) -> List[int]:
    """
    On va croiser deux solutions sélectionné au hasard dans la population passé en paramètre

    :param items: tous les items.
    :param population: une liste de solution avec 1 pour un item et 0 pour pas d'item.
    :param max_capacity: capacité maximale du sac.
    :return: la solution après le croisement
    """

    items_number = len(items)

    random_index_first_crossover = numpy.random.randint(0, len(population))
    random_index_second_crossover = random_index_first_crossover

    # On veut croiser deux solutions différentes
    while random_index_first_crossover == random_index_second_crossover:
        random_index_second_crossover = numpy.random.randint(0, len(population))

    is_crossover_not_correct = True

    first_crossover = []
    second_crossover = []

    while is_crossover_not_correct:
        first_crossover, second_crossover = get_crossover(population[random_index_first_crossover],
                                                          population[random_index_second_crossover], items_number)

        is_first_crossover_correct = check_knapsack(first_crossover, items, max_capacity)
        is_second_crossover_correct = check_knapsack(second_crossover, items, max_capacity)

        if is_first_crossover_correct and not is_second_crossover_correct:
            return first_crossover

        if not is_first_crossover_correct and is_second_crossover_correct:
            return second_crossover

        is_crossover_not_correct = not is_first_crossover_correct and not is_second_crossover_correct

    if numpy.random.random() <= 0.5:
        return first_crossover

    return second_crossover


def get_crossover(first_element: List[int], second_element: List[int], items_number: int) -> (List[int], List[int]):
    """
    Croise deux solutions entre elles en les coupant en deux.

    :param first_element: première solution à croiser.
    :param second_element: deuxième solution à croiser.
    :param items_number: le nombre d'items
    :return: les deux nouvelles solutions croisées entre elles.
    """
    random_crossover = numpy.random.randint(1, items_number)

    first_part_first_element = first_element[:random_crossover]
    second_part_first_element = first_element[random_crossover:]

    first_part_second_element = second_element[:random_crossover]
    second_part_second_element = second_element[random_crossover:]

    return first_part_first_element + second_part_second_element, first_part_second_element + second_part_first_element


# Possible de choisir un nombre d'index à faire muter et on fait muter tous les index choisi
def mutation(population: List[Solution], items: List[Item], max_capacity: int, proba_mutation: float) -> Solution:
    """
    On fait muter suivant la probabilité de mutation, une solution pioché au hasard dans la population.
    Reviens à ajouter un item s'il n'est pas dans le sac ou inversement à l'enlever.

    :param max_capacity: la capacité max du sac.
    :param items: tous les items possible à mettre dans le sac.
    :param population: la population à faire muter
    :param proba_mutation: la probabilité de mutation.
    :return: la solution mutée.
    """
    # 
    number_item_to_mutate = len(items) * proba_mutation

    random_index_mutation = numpy.random.randint(0, len(population))

    selected_solutions_for_mutation = population[random_index_mutation].copy()

    for index_item in range(len(selected_solutions_for_mutation)):
        random_mutation = numpy.random.random()
        if random_mutation <= proba_mutation:
            result_number_mutation = 1 if selected_solutions_for_mutation[index_item] == 0 else 0

            selected_solutions_for_mutation[index_item] = result_number_mutation

            if result_number_mutation == 1:
                if not check_knapsack(selected_solutions_for_mutation, items, max_capacity):
                    selected_solutions_for_mutation[index_item] = 0

    return selected_solutions_for_mutation


def check_knapsack(solution: List[int], items: List[Item], max_capacity: int) -> bool:
    """
    Vérifie si la liste d'item passée en paramètre n'a pas un poids supérieur à la capcité maximale.

    :param solution: la solution que l'on souhaite vérifiée.
    :param items: la liste d'item.
    :param max_capacity: la capacité maximale du sac.
    :return: True si la liste d'items rentre dans le sac, False sinon.
    """

    selected_items = []
    for index, in_knapsack in enumerate(solution):
        if in_knapsack == 1:
            selected_items.append(items[index])

    weights = sum(item.weight for item in selected_items)
    if weights > max_capacity:
        return False
    return True


def algo_genetique(
        nombre_generation: int,
        max_capacity: int,
        items: List[Item],
        nb_best: int,
        proba_cross: float,
        proba_mutation: float,
        debug: bool
) -> List[int]:
    # TODO le prof a fait avec nombre_generation = 60 && nb_best = 20 pour un autre problème

    # On créé la première itération et donc la première population. Le tableau est de type -> List[List[List[int]]]
    population_iteration = [create_initial_population(nombre_generation, items)]

    best_known = update_best_solution(population_iteration[0], items)

    for k in range(1, nombre_generation):
        if debug:
            print("Nombre de génération : {} / {}".format(k, nombre_generation))

        population_etoile_k_moins_un = roulette_wheel_reproduction(population_iteration[k - 1])
        population_iteration.append(best_solutions_reproduction(nb_best, population_iteration[k - 1], items))

        for i in range(nb_best + 1, nombre_generation):
            if numpy.random.random() < proba_cross:
                population_iteration[k].append(crossover(population_etoile_k_moins_un, items, max_capacity))
            else:
                population_iteration[k].append(
                    mutation(population_etoile_k_moins_un, items, max_capacity, proba_mutation))

        best_known = update_best_solution(population_iteration[k], items)

    return best_known
