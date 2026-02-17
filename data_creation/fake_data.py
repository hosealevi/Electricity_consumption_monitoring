import pandas as pd
import numpy as np
import os
# -------------------------
# PARAMETRES
# -------------------------
np.random.seed(42)

annee_debut = 2020
annee_fin = 2024

dates = pd.date_range(f"{annee_debut}-01-01", f"{annee_fin}-12-01", freq="MS")

batiments = [
    {"nom": "Vaccination", "compteur": "Compteur_A", "p_souscrite": 100, "base": 14000},
    {"nom": "Admin-Fin", "compteur": "Compteur_A", "p_souscrite": 100, "base": 10000},
    {"nom": "Informatique", "compteur": "Compteur_B", "p_souscrite": 120, "base": 18000},
    {"nom": "Projets", "compteur": "Compteur_B", "p_souscrite": 80, "base": 9000},
    {"nom": "Direction_Generale", "compteur": "Compteur_B", "p_souscrite": 70, "base": 8000},
]

# inflation annuelle du prix kWh
inflation = {
    2020: 95,
    2021: 100,
    2022: 105,
    2023: 110,
    2024: 115
}

# -------------------------
# FONCTION SAISONNALITE
# -------------------------
def saisonnalite(mois):
    # pics de consommation en été (clim)
    if mois in [4,5,6,7,8,9]:
        return 1.15
    elif mois in [12,1]:
        return 0.95
    else:
        return 1.0

# -------------------------
# GENERATION DATA
# -------------------------
data = []

for b in batiments:

    for date in dates:

        annee = date.year
        mois = date.month

        base = b["base"]

        # consommation avec saisonnalité + bruit
        facteur_saison = saisonnalite(mois)
        bruit = np.random.normal(0, 0.08)

        consommation = base * facteur_saison * (1 + bruit)

        # coût kWh avec inflation + variabilité
        cout_base = inflation[annee]
        cout_kwh = np.random.normal(cout_base, 3)

        facture = consommation * cout_kwh

        # cosphi (qualité réseau)
        cosphi = np.clip(np.random.normal(0.93, 0.03), 0.85, 0.99)

        # puissance max
        puissance_max = np.random.uniform(0.6, 1.3) * b["p_souscrite"]

        data.append({
            "date": date.strftime("%Y-%m"),
            "annee": annee,
            "mois": mois,
            "batiment": b["nom"],
            "departement": b["nom"],
            "compteur": b["compteur"],
            "consommation_kwh": round(consommation, 2),
            "cout_kwh_fcfa": round(cout_kwh, 2),
            "puissance_souscrite_kw": b["p_souscrite"],
            "puissance_max_kw": round(puissance_max, 2)
        })

df = pd.DataFrame(data)

# -------------------------
# EXPORT
# -------------------------
os.makedirs("Demo/data", exist_ok=True)

df.to_csv("Demo/data/consommation_5ans.csv", index=False)

print("Fichier généré : Demo/data/consommation_5ans.csv")
print("Nombre de lignes :", len(df))
