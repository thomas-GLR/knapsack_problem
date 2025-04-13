import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Charger les données
# df1 = pd.read_csv('result/pi-12-1000-1000-001.kna-proba.csv')
df2 = pd.read_csv('result/pi-12-1000-1000-001.kna.csv')

# Fusionner les deux dataframes sans se préoccuper de leur source
# df = pd.concat([df1, df2], ignore_index=True)
df = pd.concat([df2], ignore_index=True)

# Définir les types d'initialisation
init_types = ['LOW', 'MEDIUM', 'HIGH']
colors = ['blue', 'green', 'red']  # Couleurs pour chaque variable

# Créer un graphique 3D pour chaque type d'initialisation
for i, init_type in enumerate(init_types):
    # Filtrer les données pour ce type d'initialisation
    data = df[df['TYPE_INIT_POP'] == init_type]

    if not data.empty:
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Normaliser les données pour une meilleure visualisation
        x = data['NB_GENERATION']
        y = data['NB_POPULATION']
        z = data['NB_BEST']
        color = data['PROFIT']

        # Tracer les points en 3D, avec la couleur basée sur le profit
        scatter = ax.scatter(x, y, z, c=color, cmap='viridis',
                             s=100, alpha=0.8, edgecolors='w', linewidth=0.5)

        # Ajouter une barre de couleur pour indiquer le profit
        cbar = plt.colorbar(scatter)
        cbar.set_label('PROFIT', fontsize=12)

        # Ajouter des labels
        ax.set_xlabel('NB_GENERATION', fontsize=12)
        ax.set_ylabel('NB_POPULATION', fontsize=12)
        ax.set_zlabel('NB_BEST', fontsize=12)

        # Titre
        plt.title(f'Influence des paramètres sur le PROFIT - Type: {init_type}', fontsize=14)

        # Sauvegarder le graphique 3D
        plt.savefig(f'params_3d_{init_type}.png', dpi=300, bbox_inches='tight')

        # Créer également des graphiques 2D pour montrer les relations individuelles
        plt.figure(figsize=(15, 5))

        # 1. NB_GENERATION vs PROFIT
        plt.subplot(1, 3, 1)
        plt.scatter(data['NB_GENERATION'], data['PROFIT'], color=colors[0], alpha=0.7, s=80)
        plt.title(f'NB_GENERATION vs PROFIT\nType: {init_type}', fontsize=12)
        plt.xlabel('NB_GENERATION', fontsize=10)
        plt.ylabel('PROFIT', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Ajouter une ligne de tendance
        if len(data) > 1:  # Vérifier qu'il y a assez de points pour une régression
            sns.regplot(x='NB_GENERATION', y='PROFIT', data=data,
                        scatter=False, ci=None, line_kws={'color': 'darkblue', 'linestyle': '--'})

        # 2. NB_POPULATION vs PROFIT
        plt.subplot(1, 3, 2)
        plt.scatter(data['NB_POPULATION'], data['PROFIT'], color=colors[1], alpha=0.7, s=80)
        plt.title(f'NB_POPULATION vs PROFIT\nType: {init_type}', fontsize=12)
        plt.xlabel('NB_POPULATION', fontsize=10)
        plt.ylabel('PROFIT', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Ajouter une ligne de tendance
        if len(data) > 1:
            sns.regplot(x='NB_POPULATION', y='PROFIT', data=data,
                        scatter=False, ci=None, line_kws={'color': 'darkgreen', 'linestyle': '--'})

        # 3. NB_BEST vs PROFIT
        plt.subplot(1, 3, 3)
        plt.scatter(data['NB_BEST'], data['PROFIT'], color=colors[2], alpha=0.7, s=80)
        plt.title(f'NB_BEST vs PROFIT\nType: {init_type}', fontsize=12)
        plt.xlabel('NB_BEST', fontsize=10)
        plt.ylabel('PROFIT', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Ajouter une ligne de tendance
        if len(data) > 1:
            sns.regplot(x='NB_BEST', y='PROFIT', data=data,
                        scatter=False, ci=None, line_kws={'color': 'darkred', 'linestyle': '--'})

        plt.tight_layout()
        plt.savefig(f'params_2d_{init_type}.png', dpi=300)
        plt.close()

        # Créer un graphique de contour pour visualiser l'interaction entre deux variables
        # NB_GENERATION et NB_POPULATION en fonction du PROFIT
        if len(data) >= 4:  # Besoin de suffisamment de points pour une interpolation
            plt.figure(figsize=(12, 10))

            # Créer une grille pour l'interpolation
            x_min, x_max = data['NB_GENERATION'].min(), data['NB_GENERATION'].max()
            y_min, y_max = data['NB_POPULATION'].min(), data['NB_POPULATION'].max()

            # S'assurer que les valeurs min et max sont différentes
            if x_min == x_max:
                x_min -= 1
                x_max += 1
            if y_min == y_max:
                y_min -= 1
                y_max += 1

            x_grid, y_grid = np.meshgrid(
                np.linspace(x_min, x_max, 100),
                np.linspace(y_min, y_max, 100)
            )

            # Tracer le graphique avec les points colorés par NB_BEST
            plt.scatter(data['NB_GENERATION'], data['NB_POPULATION'],
                        c=data['NB_BEST'], s=data['PROFIT'] / 10,
                        cmap='plasma', alpha=0.7, edgecolors='w')

            plt.colorbar(label='NB_BEST')
            plt.xlabel('NB_GENERATION', fontsize=12)
            plt.ylabel('NB_POPULATION', fontsize=12)
            plt.title(f'Interaction entre paramètres - Type: {init_type}\n(Taille = PROFIT, Couleur = NB_BEST)',
                      fontsize=14)
            plt.grid(True, linestyle='--', alpha=0.4)

            plt.savefig(f'params_interaction_{init_type}.png', dpi=300, bbox_inches='tight')
            plt.close()

print("Graphiques générés avec succès!")