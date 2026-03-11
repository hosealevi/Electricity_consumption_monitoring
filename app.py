import streamlit as st

from config import APP_TITLE, APP_LAYOUT

from modules.data_loader import load_data
from modules.cleaning import clean_data
from modules.kpi import compute_kpi
from modules.dashboard import compute_dashboard
from modules.logo import display_logo

display_logo()
# =========================
# CONFIGURATION
# =========================

st.set_page_config(layout=APP_LAYOUT)

st.title(APP_TITLE)

st.markdown("### Tableau de bord énergétique")

st.markdown("""
Bienvenue dans le système de suivi énergétique.

Utilisez le menu à gauche pour naviguer entre :

- *Analyse des KPI*  
- *Saisonnalité* 
- *Cartographie*
""")

# =========================
# CHARGEMENT DES DONNÉES
# =========================

@st.cache_data
def load_pipeline():
    df, gdf_bat, gdf_elec = load_data()
    df = clean_data(df)
    df = compute_kpi(df)
    return df, gdf_bat, gdf_elec

df, gdf_bat, gdf_elec = load_pipeline()

# =========================
# FILTRES (SIDEBAR)
# =========================

st.sidebar.header("Filtres")

# =========================
# FILTRES DYNAMIQUES
# =========================

compteur = st.sidebar.selectbox(
    "Compteur",
    ["Tous"] + sorted(df["compteur"].dropna().unique())
)

# départements dépendants du compteur
if compteur != "Tous":
    departements_disponibles = sorted(
        df[df["compteur"] == compteur]["departement"].dropna().unique()
    )
else:
    departements_disponibles = sorted(df["departement"].dropna().unique())

departement = st.sidebar.selectbox(
    "Département",
    ["Tous"] + departements_disponibles
)

annee = st.sidebar.selectbox(
    "Année",
    ["Toutes"] + sorted(df["annee"].unique())
)
if departement != "Tous" and departement not in departements_disponibles:
    departement = "Tous"


# =========================
# FILTRAGE
# =========================

df_filtre = df.copy()

if compteur != "Tous":
    df_filtre = df_filtre[df_filtre["compteur"] == compteur]

if departement != "Tous":
    df_filtre = df_filtre[df_filtre["departement"] == departement]

if annee != "Toutes":
    df_filtre = df_filtre[df_filtre["annee"] == annee]

# =========================
# KPI PRINCIPAUX
# =========================

st.subheader("Indicateurs clés")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Dépense", f"{df_filtre['facture_fcfa'].sum()/1e6:.1f} M FCFA")
col2.metric("Consommation", f"{df_filtre['consommation_kwh'].sum()/1000:.1f} MWh")
col3.metric("Dépassement", f"{df_filtre['depassement_kw'].sum():.0f} kW")
col4.metric("Utilisation", f"{df_filtre['taux_utilisation'].mean():.1f} %")
col5.metric("Cosphi", f"{df_filtre['facteur_puissance'].mean():.3f}")

# =========================
# DASHBOARD ANNUEL
# =========================

st.subheader("Synthèse annuelle")

dashboard = compute_dashboard(df_filtre)

st.dataframe(dashboard, use_container_width=True)

# =========================
# INTERPRÉTATION AUTOMATIQUE
# =========================

st.subheader("Analyse automatique")

if df_filtre["taux_utilisation"].mean() > 90:
    st.error("Utilisation élevée : risque de surcharge")

if df_filtre["facteur_puissance"].mean() < 0.93:
    st.warning("Facteur de puissance faible : risque de pénalité")

if df_filtre["depassement_kw"].sum() > 0:
    st.warning("Dépassement de puissance détecté")

# =========================
# PIED DE PAGE
# =========================

st.markdown("---")
st.markdown("Système de suivi énergétique")
