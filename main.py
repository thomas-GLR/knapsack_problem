import os

from item import Item
from magasin import Magasin

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
