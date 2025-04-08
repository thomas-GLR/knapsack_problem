import os
import matplotlib.pyplot as plt
import numpy as np
import time

from tqdm import tqdm
from alive_progress import alive_bar
from item import Item
from magasin import Magasin
from algo_genetique import algo_genetique
from typing import List


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

    best_solution = algo_genetique(60, max_capaxity, items, 20, -1.0, 0.3, False)

    print("La meilleure solution de jeux de donnée {} est : {}".format(file_name,
                                                                       get_profit_of_solution(best_solution, items)))


# TODO Tester avec une autre méthode de mutation
if __name__ == '__main__':
    folder_path = "data"
    files = os.listdir(folder_path)

    max_capacity_knapsack, items_list = get_data_from_file(files[1])

    x = []
    y = []

    for number_generation in tqdm(range(60, 70), desc="Outer"):

        x.append(number_generation)
        best_solutions = []

        for iteration_number in range(10):
            best_solutions.append(get_profit_of_solution(algo_genetique(
                number_generation,
                max_capacity_knapsack,
                items_list,
                20,
                0.5,
                0.3,
                False
            ), items_list))

        y.append(np.mean(best_solutions, dtype=int))

    print(x)
    print(y)

    plt.plot(x, y, label="line 1")
    plt.title("Evolution de la solution en fonction du nombre de génération")
    plt.xlabel("x - Nombre de génération")
    plt.ylabel("y - Solutions")
    plt.show()
