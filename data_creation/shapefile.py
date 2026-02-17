import geopandas as gpd
from shapely.geometry import Polygon, LineString, Point
import pandas as pd
import numpy as np
import os

np.random.seed(42)

# =====================================================
# 1. CREATION DES 5 BATIMENTS (REALISTES)
# =====================================================

batiments = [
    {
        "nom": "Vaccination",
        "departement": "Vaccination",
        "compteur": "Compteur_A",
        "geometry": Polygon([(0,6), (4,6), (4,10), (0,10)])
    },
    {
        "nom": "Admin-Fin",
        "departement": "Admin-Fin",
        "compteur": "Compteur_A",
        "geometry": Polygon([(6,6), (11,6), (11,10), (6,10)])
    },
    {
        "nom": "Informatique",
        "departement": "Informatique",
        "compteur": "Compteur_B",
        "geometry": Polygon([(0,0), (5,0), (5,4), (0,4)])
    },
    {
        "nom": "Projets",
        "departement": "Projets",
        "compteur": "Compteur_B",
        "geometry": Polygon([(6,0), (10,0), (10,4), (6,4)])
    },
    {
        "nom": "Direction_Generale",
        "departement": "Direction_Generale",
        "compteur": "Compteur_A",
        "geometry": Polygon([(4,4), (7,4), (7,6), (4,6)])
    }
]

gdf_batiment = gpd.GeoDataFrame(batiments, crs="EPSG:3857")
gdf_batiment["type"] = "batiment"

# =====================================================
# 2. COULOIRS (VOIES)
# =====================================================

couloirs = [
    LineString([(2,4), (2,10)]),  # vers vaccination
    LineString([(8,4), (8,10)]),  # vers admin
    LineString([(5.5,0), (5.5,6)]),  # axe vertical central
    LineString([(0,5), (11,5)])  # axe horizontal
]

gdf_couloirs = gpd.GeoDataFrame(
    [{"type": "couloir", "geometry": c} for c in couloirs],
    crs="EPSG:3857"
)

# =====================================================
# 3. SORTIES
# =====================================================

sorties = [
    Point(5.5, 11),
    Point(0,5),
    Point(11,5),
    Point(5.5, -1)
]

gdf_sorties = gpd.GeoDataFrame(
    [{"type": "sortie", "geometry": s} for s in sorties],
    crs="EPSG:3857"
)

# =====================================================
# 4. LIMITE DU SITE
# =====================================================

limite = Polygon([(-2,-2), (13,-2), (13,12), (-2,12)])

gdf_limite = gpd.GeoDataFrame(
    [{"type": "limite", "geometry": limite}],
    crs="EPSG:3857"
)

# =====================================================
# 5. COMPTEURS (POSITION STRATEGIQUE)
# =====================================================

compteurs = [
    {"compteur": "Compteur_A", "geometry": Point(3, -1)},
    {"compteur": "Compteur_B", "geometry": Point(9, -1)}
]

gdf_compteurs = gpd.GeoDataFrame(compteurs, crs="EPSG:3857")
gdf_compteurs["type"] = "compteur"

# =====================================================
# 6. EQUIPEMENTS (POINTS INTERNES)
# =====================================================

equipements = []

for idx, bat in gdf_batiment.iterrows():

    minx, miny, maxx, maxy = bat.geometry.bounds

    # créer 4 points par bâtiment
    for i in range(4):
        x = np.random.uniform(minx+0.5, maxx-0.5)
        y = np.random.uniform(miny+0.5, maxy-0.5)

        equipements.append({
            "type": "equipement",
            "batiment": bat["nom"],
            "departement": bat["departement"],
            "compteur": bat["compteur"],
            "geometry": Point(x, y)
        })

gdf_conso = gpd.GeoDataFrame(equipements, crs="EPSG:3857")

# =====================================================
# 7. RESEAU ELECTRIQUE
# =====================================================

lignes = []

for idx, row in gdf_conso.iterrows():

    compteur_geom = gdf_compteurs[
        gdf_compteurs["compteur"] == row["compteur"]
    ].geometry.iloc[0]

    ligne = LineString([compteur_geom, row.geometry])

    lignes.append({
        "type": "ligne_elec",
        "compteur": row["compteur"],
        "geometry": ligne
    })

gdf_reseau = gpd.GeoDataFrame(lignes, crs="EPSG:3857")

# =====================================================
# 8. LAYERS
# =====================================================

gdf_batiment_layer = pd.concat([
    gdf_batiment,
    gdf_couloirs,
    gdf_sorties,
    gdf_limite
], ignore_index=True)

gdf_batiment_layer = gpd.GeoDataFrame(gdf_batiment_layer, geometry="geometry", crs="EPSG:3857")

gdf_electricite_layer = pd.concat([
    gdf_compteurs,
    gdf_reseau,
    gdf_conso
], ignore_index=True)

gdf_electricite_layer = gpd.GeoDataFrame(gdf_electricite_layer, geometry="geometry", crs="EPSG:3857")

# =====================================================
# 9. EXPORT
# =====================================================

os.makedirs("data", exist_ok=True)

gdf_batiment_layer.to_file("data/institut.gpkg", layer="batiment", driver="GPKG")
gdf_electricite_layer.to_file("data/institut.gpkg", layer="electricite", driver="GPKG")

print("Shapefile amélioré créé")

# =====================================================
# 10. VISUALISATION
# =====================================================

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12,10))

# fond
gdf_limite.plot(ax=ax, edgecolor="black", facecolor="none", linewidth=2)

# batiments
gdf_batiment.plot(ax=ax, color="lightgrey", edgecolor="black")

# couloirs
gdf_couloirs.plot(ax=ax, color="blue", linewidth=2)

# réseau
gdf_reseau.plot(ax=ax, color="red", linewidth=1)

# compteurs
gdf_compteurs.plot(ax=ax, color="orange", markersize=100)

# équipements
gdf_conso.plot(ax=ax, color="purple", markersize=30)

# sorties
gdf_sorties.plot(ax=ax, color="green", markersize=80)

# labels bâtiments
for idx, row in gdf_batiment.iterrows():
    x, y = row.geometry.centroid.coords[0]
    ax.text(x, y, row["nom"], fontsize=10, ha="center")

# légende
legend_elements = [
    mpatches.Patch(color='lightgrey', label='Bâtiment'),
    Line2D([0], [0], color='blue', lw=2, label='Couloir'),
    Line2D([0], [0], color='red', lw=2, label='Réseau électrique'),
    Line2D([0], [0], marker='o', color='w', label='Compteur',
           markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Equipement',
           markerfacecolor='purple', markersize=6),
    Line2D([0], [0], marker='o', color='w', label='Sortie',
           markerfacecolor='green', markersize=8),
]

ax.legend(handles=legend_elements, loc='upper right')

ax.set_title("Plan énergétique amélioré de l'institut", fontsize=14)
ax.set_axis_off()

plt.show()
