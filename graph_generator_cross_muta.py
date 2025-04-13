import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Charger uniquement le fichier proba
df = pd.read_csv('result/pi-12-1000-1000-001.kna-proba.csv')

# Définir les types d'initialisation
init_types = ['LOW', 'MEDIUM', 'HIGH']

# Créer des graphiques pour chaque type d'initialisation
for init_type in init_types:
    # Filtrer les données pour ce type d'initialisation
    data = df[df['TYPE_INIT_POP'] == init_type]

    if not data.empty:
        # 1. Graphique principal: PROBA_CROSSOVER vs PROFIT
        plt.figure(figsize=(12, 8))

        # Scatter plot avec taille variable basée sur NB_POPULATION et couleur basée sur NB_GENERATION
        scatter = plt.scatter(
            data['PROBA_CROSSOVER'],
            data['PROFIT'],
            s=data['NB_POPULATION'] / 10,  # Taille proportionnelle à NB_POPULATION
            c=data['NB_GENERATION'],  # Couleur basée sur NB_GENERATION
            alpha=0.7,
            cmap='viridis',
            edgecolors='black'
        )

        # Ajouter des étiquettes pour NB_BEST à chaque point
        for i, row in data.iterrows():
            plt.annotate(
                f"NB_BEST: {row['NB_BEST']}",
                (row['PROBA_CROSSOVER'], row['PROFIT']),
                textcoords="offset points",
                xytext=(0, 10),
                ha='center',
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
            )

        # Ajouter une ligne de tendance
        if len(data) > 1:
            z = np.polyfit(data['PROBA_CROSSOVER'], data['PROFIT'], 1)
            p = np.poly1d(z)
            plt.plot(data['PROBA_CROSSOVER'], p(data['PROBA_CROSSOVER']),
                     linestyle='--', color='red', linewidth=2)
            slope = z[0]
            plt.title(
                f"PROBA_CROSSOVER vs PROFIT - Type: {init_type}\nTendance: {'Positive' if slope > 0 else 'Négative'} (pente = {slope:.2f})",
                fontsize=14)
        else:
            plt.title(f"PROBA_CROSSOVER vs PROFIT - Type: {init_type}", fontsize=14)

        # Légendes et labels
        plt.colorbar(scatter, label='NB_GENERATION')
        plt.xlabel('PROBA_CROSSOVER', fontsize=12)
        plt.ylabel('PROFIT', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Ajouter une légende pour la taille des points
        sizes = [min(data['NB_POPULATION']), max(data['NB_POPULATION'])]
        labels = [f"Min: {min(data['NB_POPULATION'])}", f"Max: {max(data['NB_POPULATION'])}"]

        # Créer des points de légende factices
        for size, label in zip(sizes, labels):
            plt.scatter([], [], s=size / 10, c='gray', alpha=0.7, label=label)

        plt.legend(title="NB_POPULATION", loc='best')

        # Sauvegarder le graphique principal
        plt.tight_layout()
        plt.savefig(f'crossover_profit_main_{init_type}.png', dpi=300)
        plt.close()

        # 2. Graphique de facettes par NB_BEST
        if data['NB_BEST'].nunique() > 1:
            unique_nb_best = sorted(data['NB_BEST'].unique())
            n_cols = min(3, len(unique_nb_best))
            n_rows = (len(unique_nb_best) + n_cols - 1) // n_cols  # Calcul du nombre de lignes nécessaires

            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows), sharex=True, sharey=True)

            # Adapter pour le cas d'une seule ligne
            if n_rows == 1 and n_cols == 1:
                axes = np.array([axes])
            elif n_rows == 1:
                axes = np.array([axes])
            elif n_cols == 1:
                axes = axes.reshape(-1, 1)

            for i, nb_best in enumerate(unique_nb_best):
                row_idx = i // n_cols
                col_idx = i % n_cols

                ax = axes[row_idx, col_idx] if n_rows > 1 else axes[col_idx]

                # Filtrer les données pour ce NB_BEST
                subset = data[data['NB_BEST'] == nb_best]

                # Scatter plot
                scatter = ax.scatter(
                    subset['PROBA_CROSSOVER'],
                    subset['PROFIT'],
                    s=subset['NB_POPULATION'] / 10,
                    c=subset['NB_GENERATION'],
                    alpha=0.7,
                    cmap='viridis',
                    edgecolors='black'
                )

                # Ajouter une ligne de tendance
                if len(subset) > 1:
                    z = np.polyfit(subset['PROBA_CROSSOVER'], subset['PROFIT'], 1)
                    p = np.poly1d(z)
                    ax.plot(subset['PROBA_CROSSOVER'], p(subset['PROBA_CROSSOVER']),
                            linestyle='--', color='red', linewidth=2)

                ax.set_title(f"NB_BEST = {nb_best}", fontsize=12)
                ax.grid(True, linestyle='--', alpha=0.7)

                # Ajouter les étiquettes d'axe uniquement sur les graphiques du bas et de gauche
                if row_idx == n_rows - 1:
                    ax.set_xlabel('PROBA_CROSSOVER', fontsize=10)
                if col_idx == 0:
                    ax.set_ylabel('PROFIT', fontsize=10)

            # Masquer les axes vides
            for i in range(len(unique_nb_best), n_rows * n_cols):
                row_idx = i // n_cols
                col_idx = i % n_cols
                if n_rows > 1:
                    fig.delaxes(axes[row_idx, col_idx])
                else:
                    fig.delaxes(axes[col_idx])

            # Ajouter une barre de couleur commune
            plt.tight_layout()
            fig.subplots_adjust(right=0.9)
            cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
            fig.colorbar(scatter, cax=cbar_ax, label='NB_GENERATION')

            # Ajouter un titre global
            fig.suptitle(f"PROBA_CROSSOVER vs PROFIT par NB_BEST - Type: {init_type}", fontsize=16, y=1.02)

            # Sauvegarder le graphique de facettes
            plt.savefig(f'crossover_profit_by_nb_best_{init_type}.png', dpi=300, bbox_inches='tight')
            plt.close()

        # 3. Graphique de groupe par NB_GENERATION
        if data['NB_GENERATION'].nunique() > 1:
            plt.figure(figsize=(14, 8))

            # Créer un boxplot pour visualiser la distribution des profits par PROBA_CROSSOVER
            ax = sns.boxplot(x='PROBA_CROSSOVER', y='PROFIT', data=data, color='lightgray')

            # Ajouter des points individuels, colorés par NB_GENERATION
            sns.stripplot(x='PROBA_CROSSOVER', y='PROFIT', hue='NB_GENERATION',
                          data=data, jitter=True, size=10, palette='viridis')

            # Ajouter des étiquettes pour NB_POPULATION et NB_BEST
            for i, row in data.iterrows():
                plt.annotate(
                    f"P:{row['NB_POPULATION']}, B:{row['NB_BEST']}",
                    (row['PROBA_CROSSOVER'], row['PROFIT']),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center',
                    fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.7)
                )

            plt.title(f"Distribution du PROFIT par PROBA_CROSSOVER - Type: {init_type}", fontsize=14)
            plt.xlabel('PROBA_CROSSOVER', fontsize=12)
            plt.ylabel('PROFIT', fontsize=12)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.legend(title='NB_GENERATION', bbox_to_anchor=(1.05, 1), loc='upper left')

            plt.tight_layout()
            plt.savefig(f'crossover_profit_distribution_{init_type}.png', dpi=300)
            plt.close()

        # 4. Graphique 3D pour visualiser PROBA_CROSSOVER, PROFIT et un troisième paramètre
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        scatter = ax.scatter(
            data['PROBA_CROSSOVER'],
            data['NB_POPULATION'],
            data['PROFIT'],
            c=data['NB_GENERATION'],
            s=data['NB_BEST'] * 5,
            alpha=0.7,
            cmap='viridis',
            edgecolors='black'
        )

        ax.set_xlabel('PROBA_CROSSOVER', fontsize=12)
        ax.set_ylabel('NB_POPULATION', fontsize=12)
        ax.set_zlabel('PROFIT', fontsize=12)

        plt.colorbar(scatter, label='NB_GENERATION')
        plt.title(
            f"Analyse 3D: PROBA_CROSSOVER, NB_POPULATION et PROFIT - Type: {init_type}\n(Taille = NB_BEST, Couleur = NB_GENERATION)",
            fontsize=14)

        plt.tight_layout()
        plt.savefig(f'crossover_profit_3d_{init_type}.png', dpi=300, bbox_inches='tight')
        plt.close()

print("Graphiques d'analyse PROBA_CROSSOVER vs PROFIT générés avec succès!")