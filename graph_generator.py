import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def inspect_dataframe(df):
    """Affiche des informations détaillées sur le DataFrame pour le débogage"""
    print("\n===== INSPECTION DU DATAFRAME =====")
    print("Shape:", df.shape)
    print("\nColonnes:", df.columns.tolist())
    print("\nPremières lignes:")
    print(df.head())
    print("\nInformations sur les types de données:")
    print(df.info())
    print("\nStatistiques descriptives:")
    print(df.describe())

    # Vérifier si les noms de colonnes ont des espaces ou des problèmes de casse
    for col in df.columns:
        stripped_col = col.strip()
        if col != stripped_col:
            print(f"Attention: La colonne '{col}' contient des espaces en début/fin.")

        # Vérifiez si une version en majuscules ou minuscules existe
        if col.upper() in [c.upper() for c in df.columns] and col != col.upper():
            print(f"Attention: La colonne '{col}' pourrait avoir un problème de casse.")


def analyse_par_type_pop(df, type_col='TYPE_INIT_POP', profit_col='PROFIT', time_col='TIME_EXECUTION',
                         weight_col='WEIGHT'):
    """Fonction adaptée pour accepter les noms de colonnes réels"""
    print(f"Analyse par {type_col}")

    # Vérifier si les colonnes existent
    if type_col not in df.columns:
        print(f"ERREUR: La colonne '{type_col}' n'existe pas dans le DataFrame!")
        print("Colonnes disponibles:", df.columns.tolist())
        return

    if profit_col not in df.columns:
        print(f"ERREUR: La colonne '{profit_col}' n'existe pas dans le DataFrame!")
        return

    if time_col not in df.columns:
        print(f"ERREUR: La colonne '{time_col}' n'existe pas dans le DataFrame!")
        return

    # Analyse par type de population
    plt.figure(figsize=(12, 6))

    # Boîte à moustaches pour la comparaison de PROFIT par TYPE_INIT_POP
    plt.subplot(1, 2, 1)
    sns.boxplot(x=type_col, y=profit_col, data=df)
    plt.title(f'Distribution du {profit_col} par {type_col}')
    plt.xticks(rotation=45)

    # Boîte à moustaches pour la comparaison de TIME_EXECUTION par TYPE_INIT_POP
    plt.subplot(1, 2, 2)
    sns.boxplot(x=type_col, y=time_col, data=df)
    plt.title(f'Distribution du TEMPS d\'exécution par {type_col}')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # Calcul des moyennes par TYPE_INIT_POP
    if weight_col in df.columns:
        print(df.groupby(type_col)[[profit_col, weight_col, time_col]].mean())
    else:
        print(df.groupby(type_col)[[profit_col, time_col]].mean())


# Charger les données avec plus d'options pour s'adapter à différents formats
def load_data():
    """Tente de charger les données avec différentes options"""
    file_paths = [
        'result/pi-15-1000-1000-001.kna.csv',
        'pi-15-1000-1000-001.kna - Copie.csv',
        'pi-15-1000-1000-001.kna.csv'
    ]

    # Essayez différentes options de chargement
    for path in file_paths:
        try:
            # Essai standard
            print(f"Tentative de chargement de {path}...")
            df = pd.read_csv(path)
            print(f"Chargement réussi avec {len(df)} lignes et {len(df.columns)} colonnes!")
            return df
        except FileNotFoundError:
            print(f"Fichier non trouvé: {path}")
            continue
        except Exception as e:
            print(f"Erreur lors du chargement de {path}: {e}")
            try:
                # Essai avec différents séparateurs
                print("Tentative avec séparateur ;...")
                df = pd.read_csv(path, sep=';')
                print(f"Chargement réussi avec {len(df)} lignes et {len(df.columns)} colonnes!")
                return df
            except Exception:
                print("Échec avec séparateur ;")
                try:
                    # Essai avec détection automatique du séparateur
                    print("Tentative avec détection automatique du séparateur...")
                    df = pd.read_csv(path, sep=None, engine='python')
                    print(f"Chargement réussi avec {len(df)} lignes et {len(df.columns)} colonnes!")
                    return df
                except Exception:
                    print("Échec avec détection automatique")
                    continue

    # Si toutes les tentatives ont échoué, demander le chemin à l'utilisateur
    print("\nToutes les tentatives automatiques ont échoué.")
    path = input("Veuillez entrer le chemin complet du fichier CSV: ")

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Erreur: {e}")
        sep = input("Entrez le séparateur à utiliser (virgule par défaut): ") or ','
        try:
            df = pd.read_csv(path, sep=sep)
            return df
        except Exception as e:
            print(f"Impossible de charger le fichier: {e}")
            return None


# Programme principal
df = load_data()

if df is None:
    print("Impossible de charger les données. Le programme va s'arrêter.")
    exit(1)

# Inspecter le DataFrame pour comprendre sa structure
inspect_dataframe(df)

# Si les colonnes ont des noms différents, créez un dictionnaire de correspondance
# Par exemple, si 'type_init_pop' existe au lieu de 'TYPE_INIT_POP'
column_mapping = {}
for col in df.columns:
    if col.upper() == 'TYPE_INIT_POP':
        column_mapping['TYPE_INIT_POP'] = col
    elif col.upper() == 'PROFIT':
        column_mapping['PROFIT'] = col
    elif col.upper() == 'WEIGHT':
        column_mapping['WEIGHT'] = col
    elif col.upper() == 'TIME_EXECUTION':
        column_mapping['TIME_EXECUTION'] = col
    elif 'TYPE' in col.upper() and 'INIT' in col.upper() and 'POP' in col.upper():
        column_mapping['TYPE_INIT_POP'] = col
    elif 'PROFIT' in col.upper():
        column_mapping['PROFIT'] = col
    elif 'WEIGHT' in col.upper():
        column_mapping['WEIGHT'] = col
    elif 'TIME' in col.upper() and 'EXEC' in col.upper():
        column_mapping['TIME_EXECUTION'] = col

print("\nCorrespondance des colonnes trouvée:", column_mapping)

# Utiliser les noms de colonnes réels pour l'analyse
type_col = column_mapping.get('TYPE_INIT_POP', 'TYPE_INIT_POP')
profit_col = column_mapping.get('PROFIT', 'PROFIT')
weight_col = column_mapping.get('WEIGHT', 'WEIGHT')
time_col = column_mapping.get('TIME_EXECUTION', 'TIME_EXECUTION')

# Exécuter l'analyse avec les noms de colonnes trouvés
analyse_par_type_pop(df, type_col, profit_col, time_col, weight_col)