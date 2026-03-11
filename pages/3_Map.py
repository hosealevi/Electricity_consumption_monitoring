import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

from modules.data_loader import load_data
from modules.cleaning import clean_data
from modules.kpi import compute_kpi
from modules.mapping import prepare_map_data
from modules.logo import render_header

render_header()
# =========================
# LOAD DATA
# =========================

df, gdf_bat, gdf_elec = load_data()
df = clean_data(df)
df = compute_kpi(df)

# =========================
# TITLE
# =========================

st.title("Cartographie énergétique")

# =========================
# FILTRES
# =========================

annee = st.selectbox("Année", sorted(df["annee"].unique()))
mois = st.slider("Mois", 1, 12, 1)

kpi = st.selectbox("Indicateur", [
    "consommation_kwh",
    "facture_fcfa",
    "depassement_kw",
    "taux_utilisation",
    "facteur_puissance"
])

# =========================
# LABELS KPI
# =========================

kpi_labels = {
    "consommation_kwh": "Consommation énergétique (kWh)",
    "facture_fcfa": "Dépense énergétique (FCFA)",
    "depassement_kw": "Dépassement de puissance (kW)",
    "taux_utilisation": "Taux d'utilisation (%)",
    "facteur_puissance": "Facteur de puissance"
}

mois_nom = [
    "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

# =========================
# PREP DATA
# =========================

gdf_bat_map, gdf_elec_map = prepare_map_data(
    df, gdf_bat, gdf_elec, annee, mois, kpi
)

# =========================
# SEPARATION DES LAYERS
# =========================

batiments = gdf_bat_map[gdf_bat_map["type"] == "batiment"]
couloirs = gdf_bat_map[gdf_bat_map["type"] == "couloir"]
sorties = gdf_bat_map[gdf_bat_map["type"] == "sortie"]
limite = gdf_bat_map[gdf_bat_map["type"] == "limite"]

lignes = gdf_elec_map[gdf_elec_map["type"] == "ligne_elec"]
equipements = gdf_elec_map[gdf_elec_map["type"] == "equipement"]
compteurs = gdf_elec_map[gdf_elec_map["type"] == "compteur"]

# =========================
# FIGURE
# =========================

fig, ax = plt.subplots(figsize=(10,10))
fig.patch.set_facecolor("white")
ax.set_facecolor("#f7f7f7")

# =========================
# FOND
# =========================

limite.plot(ax=ax, facecolor="none", edgecolor="black", linewidth=2)

# =========================
# INFRASTRUCTURE
# =========================

couloirs.plot(ax=ax, color="blue", linewidth=2, alpha=0.7)
sorties.plot(ax=ax, color="green", markersize=80)

# =========================
# BATIMENTS (KPI)
# =========================

batiments.plot(
    column=kpi,
    cmap="coolwarm",
    legend=True,
    ax=ax,
    edgecolor="black",
    alpha=0.85
)

# =========================
# RESEAU ELECTRIQUE
# =========================

lignes.plot(ax=ax, color="black", linewidth=1, alpha=0.3)

equipements.plot(
    ax=ax,
    column=kpi,
    cmap="coolwarm",
    markersize=40
)

compteurs.plot(ax=ax, color="blue", markersize=120)

# =========================
# LABELS
# =========================

for idx, row in batiments.iterrows():

    if row.geometry:
        x, y = row.geometry.centroid.coords[0]

        # valeur au centre
        ax.text(
            x, y,
            f"{row[kpi]:.0f}",
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=0.7, boxstyle="round")
        )

        # nom du bâtiment à l'extérieur
        ax.annotate(
            row["nom"],
            xy=(x, y),
            xytext=(x, y + 1.2),
            arrowprops=dict(arrowstyle="-", color="black"),
            ha="center",
            fontsize=9,
            fontweight="bold"
        )
# =========================
# LEGENDE PERSONNALISEE
# =========================

legend_elements = [

    mpatches.Patch(color='lightgrey', label='Bâtiment (couleur = KPI)'),

    Line2D([0], [0], color='blue', lw=2, label='Couloir'),

    Line2D([0], [0], color='black', lw=2, label='Réseau électrique'),

    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='blue', markersize=10,
           label='Compteur'),

    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='red', markersize=6,
           label='Equipement'),

    Line2D([0], [0], marker='o', color='w',
           markerfacecolor='green', markersize=8,
           label='Sortie'),

    Line2D([0], [0], color='black', lw=2, label='Limite site')
]

legend = ax.legend(
    handles=legend_elements,
    loc='upper left',
    bbox_to_anchor=(0, -0.15),   # 👈 POSITION BAS GAUCHE
    ncol=2,                      # 👈 sur 2 colonnes
    fontsize=9,
    frameon=True
)

# =========================
# TITRE
# =========================

titre = f"""
Carte énergétique de l'institut
{kpi_labels[kpi]}
Date : {mois_nom[mois]} {annee}
"""

ax.set_title(titre, fontsize=14, fontweight="bold")

# =========================
# FINAL
# =========================

ax.axis("off")

st.pyplot(fig)
