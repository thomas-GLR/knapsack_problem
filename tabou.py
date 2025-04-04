import random 
from tqdm import tqdm

def knapsack_neighborhood(solution, items, max_capacity):
    neighborhood = []
    solution_set = set(solution)
    solution_weight = sum(item.weight for item in solution)

    # Parcourir chaque élément de la solution actuelle
    for i in range(len(solution)):
        # Créer un voisin en supprimant un élément
        neighbor = solution[:i] + solution[i+1:]
        neighbor_weight = solution_weight - solution[i].weight
        # Ajouter le voisin si son poids est inférieur ou égal à la capacité maximale
        if neighbor_weight <= max_capacity:
            neighborhood.append(neighbor)

    # Parcourir chaque élément disponible
    for item in items:
        # Ajouter un élément qui n'est pas déjà dans la solution
        if item not in solution_set:
            neighbor = solution + [item]
            neighbor_weight = solution_weight + item.weight
            # Ajouter le voisin si son poids est inférieur ou égal à la capacité maximale
            if neighbor_weight <= max_capacity:
                neighborhood.append(neighbor)

    return neighborhood

def knapsack_profit(solution):
    return sum(item.profit for item in solution)

def tabu_search(x0, f, max_iter, neighborhood_func, tabu_tenure, items, max_capacity):
    x_max = x0
    f_max = f(x0)
    tabu_list = []

    x = x0
    for i in tqdm(range(max_iter), desc='Tabu Search Progress'):
        # Définir le voisinage en excluant les solutions taboues
        neighborhood = [m for m in neighborhood_func(x, items, max_capacity) if m not in tabu_list]

        if not neighborhood:
            break  # Arrêt si aucun voisin n'est disponible

        # Sélectionner le meilleur voisin
        x_next = max(neighborhood, key=f)

        # Calculer la variation de f
        delta_f = f(x_next) - f(x)

        # Ajouter à la liste taboue si nécessaire
        if delta_f >= 0:
            tabu_list.append(x)
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)  # Maintenir la taille de la liste taboue

        # Mise à jour de la meilleure solution trouvée
        if f(x_next) > f_max:
            x_max = x_next
            f_max = f(x_next)

        x = x_next  # Avancer à la prochaine itération

    return x_max
