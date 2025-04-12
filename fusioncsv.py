import os
import pandas as pd

# Dossier contenant les fichiers CSV
#for i in range(0,9):
i=2
dossier =f"results/{i}"
dossier_name=f"results_{i}"

# Créer le dossier s'il n'existe pas

# Lister tous les fichiers CSV
fichiers_csv = [f for f in os.listdir(dossier) if f.endswith('.csv')]

# Fusionner tous les fichiers
df_total = pd.concat([pd.read_csv(os.path.join(dossier, f)) for f in fichiers_csv], ignore_index=True)

# Enregistrer dans un nouveau fichier
df_total.to_csv(os.path.join(dossier, f"{dossier_name}_fusionné.csv"), index=False)

print(f"Fusion terminée. Fichier enregistré sous '{dossier_name}_fusionné.csv'")
