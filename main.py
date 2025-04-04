import os
import random
import time

from item import Item
from magasin import Magasin
from tabou import tabu_search, knapsack_neighborhood, knapsack_profit


import csv
import os


# Fonction d'enregistrement des résultats
def save_results(file_name, best_solution, total_profit, total_weight, max_iter, tabu_tenure,tps_exec):
    results_file = f'results/{file_name}_{max_iter}_{tabu_tenure}.csv'
    file_exists = os.path.isfile(results_file)

    # Lire les résultats existants
    existing_profit = 0
    if file_exists:
        with open(results_file, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                existing_profit = int(row[1])
                break

    #sauvegarder les résultats si le profit total est supérieur
    if total_profit > existing_profit:
        with open(results_file, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Total profit", "Total weight", "Max iter", "Tabu tenure", "Items","Temps d'execution"])
            writer.writerow([total_profit, total_weight, max_iter, tabu_tenure,tps_exec, ""])
            for item in best_solution:
                writer.writerow([item.id, item.profit, item.weight])

if __name__ == '__main__':




    folder_path = "data"
    files = os.listdir(folder_path)

    for index, file in enumerate(files):
        print("{} - {}".format(index, file))

    fileIndex = int(input("Choisir un fichier en sélectionnant le numéro : "))

    max_capaxity = 0
    items = []

    file_name = files[fileIndex]

    with open("data/{}".format(file_name), "r") as file:
        for index, line in enumerate(file):
            # MAX_CAPACITY
            if index == 4:
                max_capaxity = line.split("MAX_CAPACITY: ")[1]

            # ITEMS
            if index >= 7:
                line_info = line.split(" ")
                items.append(Item(id=int(line_info[0]), profit=int(line_info[1]), weight=int(line_info[2])))

    Knapsack = Magasin(capacity=max_capaxity, items=items)
    print(max_capaxity)
    # print(len(items))
    # for item in items:
    #     print(item.id, item.profit, item.weight)

    max_iter = 1000000
    tabu_tenure = 1
    for i in range(7):
        max_capaxity = int(max_capaxity)
        weight = 0
        x_0 = []
        while weight <= max_capaxity:
            i=random.randint(0, len(items)-1)
            if weight + items[i].weight > max_capaxity:
                break
            x_0.append(items[i])
            weight += items[i].weight
        print("Initial solution weight:", weight)
        print("Initial solution items:")
        for item in x_0:
            print(item.id, item.profit, item.weight)



        deb=time.time()
        best_solution = tabu_search(x0=x_0, f=knapsack_profit, max_iter=max_iter, neighborhood_func=knapsack_neighborhood, tabu_tenure=tabu_tenure, items=items, max_capacity=max_capaxity)
        fin=time.time()
        tps_exec=fin-deb
        save_results(file_name, best_solution, knapsack_profit(best_solution), sum(item.weight for item in best_solution),
                     max_iter, tabu_tenure,tps_exec)
        print("Best solution found:")
        for item in best_solution:
            print(item.id, item.profit, item.weight)
        print("Total profit:", knapsack_profit(best_solution))
        print("Total weight:", sum(item.weight for item in best_solution))



