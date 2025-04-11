import os
import csv
import time

from typing import List

import matplotlib.pyplot as plt
import numpy as np

from tqdm import tqdm

from algo_genetique import algo_genetique
from item import Item
from quality_population_enum import QualityPopulationEnum
from result import Result


def get_profit_of_solution(solution: List[int], items: List[Item]) -> int:
    profit = 0
    for solution_index, in_knapsack in enumerate(solution):
        if in_knapsack == 1:
            profit += items[solution_index].profit

    return profit


def get_data_from_file(file_name: str) -> (int, List[Item]):
    items = []
    max_capacity = 0

    with open("data/{}".format(file_name), "r") as file:
        for index, line in enumerate(file):
            # MAX_CAPACITY
            if index == 4:
                max_capacity = int(line.split("MAX_CAPACITY: ")[1])

            # ITEMS
            if index >= 7:
                line_info = line.split(" ")
                items.append(Item(id=int(line_info[0]), profit=int(line_info[1]), weight=int(line_info[2])))

    return max_capacity, items


def use_algo_genetique_with_asking_user(files: List[str], file_index: int):
    for index, file in enumerate(files):
        print("{} - {}".format(index, file))

    if file_index == -1:
        file_index = int(input("Choisir un fichier en sélectionnant le numéro : "))

    max_capaxity = 0
    items = []

    file_name = files[file_index]

    max_capacity, items = get_data_from_file(file_name)

    best_solution = algo_genetique(60, 60, max_capaxity, items, 20, -1.0, 0.3, False).profit

    print("La meilleure solution de jeux de donnée {} est : {}".format(file_name, best_solution))


def write_data_in_file(file_name: str, results: List[Result]):
    header = ["profit", "poids", "Nombre génération", "Nombre population", "Nombre meilleur solution sélectionnée",
                   "Probabilité crossover", "Probabilité mutation", "Items sélectionnés", "Type population initiale"]

    with open('result/{}.csv'.format(file_name), 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(header)

        for result in results:
            writer.writerow(result.result_to_csv())


def benchmark():

    folder_path = "data"
    files = os.listdir(folder_path)

    proba_crossovers = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    proba_mutations = [0.005, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    quality_init_population = [QualityPopulationEnum.LOW, QualityPopulationEnum.MEDIUM, QualityPopulationEnum.HIGH]

    for file_name in files:

        print("Début itération fichier {} !".format(file_name))

        max_capacity, items = get_data_from_file(file_name)

        results = []

        for number_generation in tqdm(range(60, 660), desc="Nombre de génération", colour="red"):
            for number_population in tqdm(range(10, 310), desc="Nombre de la population", colour="green"):
                for nb_best in tqdm(range(1, number_population + 1), desc="Nombre de best", colour="blue"):
                    for proba_crossover in proba_crossovers:
                        for proba_mutation in proba_mutations:
                            for type_init_population in quality_init_population:

                                start_time = time.time()
                                try:
                                    current_solution = algo_genetique(number_generation, number_population, max_capacity, items, nb_best, proba_crossover, proba_mutation, False, type_init_population)
                                except Exception as e:
                                    print("Une exception est survenue : {} avec les paramètres suivants :\n"
                                          " - Nombre de génération : {}\n"
                                          " - Nombre de population : {}\n"
                                          " - Nombre de best : {}\n"
                                          " - Probabilité crossover : {}\n"
                                          " - Probabilité mutation : {}\n"
                                          " - Type init population : {}\n".format(
                                        e,
                                        number_generation,
                                        number_population,
                                        nb_best,
                                        proba_crossover,
                                        proba_mutation,
                                        type_init_population.name
                                    )
                                    )

                                    write_data_in_file(file_name + "_erreur", results)

                                    raise e

                                end_time = time.time()

                                results.append(Result(current_solution, items, number_generation, number_population, nb_best, proba_crossover, proba_mutation, type_init_population, end_time - start_time))

        write_data_in_file(file_name, results)

        print("Fichier {} terminé !".format(file_name))


# TODO récupérer dans CSV :
# - id items
# - profit solution
# - poids solution
# - paramètres solution

# TODO tester avec même paramètre (peut etre les meilleurs) mais plein de fois pour voir si solutions très différentes ou pas

# TODO Tester avec une autre méthode de mutation
if __name__ == '__main__':

    benchmark()

    # folder_path = "data"
    # files = os.listdir(folder_path)
    #
    # max_capacity, items = get_data_from_file(files[0])
    #
    # for i in tqdm(range(5000), desc="Test", colour="red"):
    #     algo_genetique(60, 10, max_capacity, items, 8, 0.2, 1.0, False, QualityPopulationEnum.MEDIUM)

    # folder_path = "data"
    # files = os.listdir(folder_path)
    #
    # max_capacity_knapsack, items_list = get_data_from_file(files[1])
    #
    # x = []
    # y = []
    #
    # for number_generation in tqdm(range(0, 200), desc="Outer"):
    #
    #     x.append(number_generation)
    #     profits = []
    #     weights = []
    #
    #     for iteration_number in range(1):
    #         solution = algo_genetique(
    #             60,
    #             60,
    #             max_capacity_knapsack,
    #             items_list,
    #             20,
    #             1,
    #             0.3,
    #             False
    #         )
    #         profits.append(solution.profit)
    #         weights.append(solution.weight)
    #
    #     y.append(np.mean(profits, dtype=int))
    #
    # plt.plot(x, y, label="line 1")
    # plt.title("Evolution de la solution en fonction du nombre de population")
    # plt.xlabel("x - Nombre de population")
    # plt.ylabel("y - Profits")
    # plt.show()
