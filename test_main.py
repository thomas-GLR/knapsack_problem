import os
import csv
import time
from functools import partial
from multiprocessing import Pool
import multiprocessing

from typing import List

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


def process_single_task(task_index, params, max_capacity, items, file_name):
    number_generation, number_population, nb_best, proba_crossover, proba_mutation, type_init_population = params

    start_time = time.time()
    try:
        current_solution = algo_genetique(
            number_generation, number_population, max_capacity, items,
            nb_best, proba_crossover, proba_mutation, False, type_init_population
        )
    except Exception as e:
        print(f"Une exception est survenue : {e} avec les paramètres suivants :\n"
              f" - Nombre de génération : {number_generation}\n"
              f" - Nombre de population : {number_population}\n"
              f" - Nombre de best : {nb_best}\n"
              f" - Probabilité crossover : {proba_crossover}\n"
              f" - Probabilité mutation : {proba_mutation}\n"
              f" - Type init population : {type_init_population.name}\n")

        return "ERROR", file_name, None, task_index

    end_time = time.time()

    result = Result(
        current_solution, items, number_generation, number_population,
        nb_best, proba_crossover, proba_mutation, type_init_population,
        end_time - start_time
    )

    return "SUCCESS", file_name, result, task_index



def benchmark():

    folder_path = "data"
    files = os.listdir(folder_path)

    proba_crossovers = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    proba_mutations = [0.005, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    quality_init_population = [QualityPopulationEnum.LOW, QualityPopulationEnum.MEDIUM, QualityPopulationEnum.HIGH]

    num_processes = multiprocessing.cpu_count() - 1  # Leave one CPU free for system tasks
    print(f"Using {num_processes} processes")


    for file_name in files:

        print("Début itération fichier {} !".format(file_name))

        max_capacity, items = get_data_from_file(file_name)

        results = []
        error_results = []
        all_params = []

        number_generations = []
        number_populations = []
        nb_bests = []
        proba_crossoverss = []
        proba_mutationss = []
        types = []

        for number_generation in tqdm(range(60, 260, 10), desc="Nombre de génération", colour="red"):
            for number_population in range(10, 160, 5):
                for nb_best in range(1, number_population + 1):
                    for proba_crossover in proba_crossovers:
                        for proba_mutation in proba_mutations:
                            for type_init_population in quality_init_population:
                                number_generations.append(number_generation)
                                number_populations.append(number_population)
                                nb_bests.append(nb_best)
                                proba_crossoverss.append(proba_crossover)
                                proba_mutationss.append(proba_mutation)
                                types.append(type_init_population)
                                # all_params.append([
                                #     number_generation, number_population, nb_best,
                                #     proba_crossover, proba_mutation, type_init_population
                                # ])

        arguments = [(ng, npop, max_capacity, items, nb, pc, pb, False, t) for ng, npop, nb, pc, pb, t in zip(number_generations, number_populations, nb_bests, proba_crossoverss, proba_mutationss, types)]

        with Pool(num_processes) as pool:
            results = pool.starmap(algo_genetique, arguments)

        print(results)

        # for i in tqdm(range(len(results)), desc="Outer"):
        #     current_solution = results[i]
        #     results.append(
        #                 Result(current_solution, items, params[0], params[1], params[2], params[3],
        #                        params[4],  params[5], end_time - start_time))

        # for i in tqdm(range(len(all_params)), desc="Outer"):
        #     params = all_params[i]
        #     try:
        #         start_time = time.time()
        #         current_solution = algo_genetique(params[0], params[1], max_capacity, items, params[2],
        #                                           params[3], params[4], False, params[5])
        #         end_time = time.time()
        #         results.append(
        #             Result(current_solution, items, params[0], params[1], params[2], params[3],
        #                    params[4],  params[5], end_time - start_time))
        #     except Exception as e:
        #         print("Une exception est survenue : {} avec les paramètres suivants :\n"
        #               " - Nombre de génération : {}\n"
        #               " - Nombre de population : {}\n"
        #               " - Nombre de best : {}\n"
        #               " - Probabilité crossover : {}\n"
        #               " - Probabilité mutation : {}\n"
        #               " - Type init population : {}\n".format(
        #             e,
        #             params[0],
        #             params[1],
        #             params[2],
        #             params[3],
        #             params[4],
        #             params[5].name
        #         )
        #         )
        #         raise e
        #
        #     write_data_in_file(file_name + "_erreur", results)



        # # Add the index to each parameter set
        # indexed_params = [(i, params) for i, params in enumerate(all_params)]
        #
        # # Create a partial function with fixed parameters
        # process_func = partial(
        #     process_single_task,
        #     max_capacity=max_capacity,
        #     items=items,
        #     file_name=file_name
        # )
        #
        # with multiprocessing.Pool(processes=num_processes) as pool:
        #
        #     # Process tasks
        #     for status, file, result, task_index in pool.imap_unordered(
        #             lambda x: process_func(x[0], x[1]), indexed_params
        #     ):
        #
        #         if status == "SUCCESS":
        #             results.append(result)
        #         else:
        #             error_results.append(result)
        #
        # write_data_in_file(file_name, results)
        #
        # if error_results:
        #     write_data_in_file(file_name + "_erreur", error_results)
        #
        # print("Fichier {} terminé !".format(file_name))


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
