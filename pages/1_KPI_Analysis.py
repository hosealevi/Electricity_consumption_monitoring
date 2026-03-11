import streamlit as st
import plotly.graph_objects as go

from modules.data_loader import load_data
from modules.cleaning import clean_data
from modules.kpi import compute_kpi
from modules.logo import display_logo

display_logo()
# =========================
# LOAD DATA
# =========================

df, gdf_bat, gdf_elec = load_data()
df = clean_data(df)
df = compute_kpi(df)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filtres")

compteur = st.sidebar.selectbox(
    "Compteur", ["All"] + sorted(df["compteur"].dropna().unique())
)

# =========================
# DEPARTEMENTS DYNAMIQUES
# =========================

if compteur != "All":
    departements_disponibles = sorted(
        df[df["compteur"] == compteur]["departement"].dropna().unique()
    )
else:
    departements_disponibles = sorted(df["departement"].dropna().unique())

departement = st.sidebar.selectbox(
    "Département",
    ["All"] + departements_disponibles
)

df_f = df.copy()

if compteur != "All":
    df_f = df_f[df_f["compteur"] == compteur]

if departement != "All":
    df_f = df_f[df_f["departement"] == departement]

# =========================
# KPI SELECTOR
# =========================

kpi_options = {
    "Consommation énergétique (kWh)": "consommation_kwh",
    "Dépense énergétique (FCFA)": "facture_fcfa",
    "Dépassement de puissance (kW)": "depassement_kw",
    "Taux d'utilisation (%)": "taux_utilisation",
    "Facteur de puissance (cosφ)": "facteur_puissance"
}

kpi_label = st.selectbox("Choisir un KPI", list(kpi_options.keys()))
kpi = kpi_options[kpi_label]

# =========================
# VARIATION KPI
# =========================

variation_map = {
    "consommation_kwh": None,
    "facture_fcfa": "taux_evolution_facture",
    "depassement_kw": None,
    "taux_utilisation": None,
    "facteur_puissance": None
}

variation = variation_map.get(kpi)

# =========================
# TITRE
# =========================

st.subheader(f"Evolution du KPI : {kpi_label}")

# =========================
# AGGREGATION KPI
# =========================

agg_type = {
    "consommation_kwh": "sum",
    "facture_fcfa": "sum",
    "depassement_kw": "sum",
    "taux_utilisation": "mean",
    "facteur_puissance": "mean"
}

# dictionnaire dynamique
agg_dict = {kpi: agg_type.get(kpi, "sum")}

if variation is not None:
    agg_dict[variation] = "mean"

df_year = df_f.groupby("annee").agg(agg_dict).reset_index()

# =========================
# DEBUG (optionnel)
# =========================
# st.write("KPI:", kpi)
# st.write("Variation:", variation)
# st.write(df_year)

# =========================
# GRAPH
# =========================

fig = go.Figure()

# KPI principal
fig.add_trace(go.Scatter(
    x=df_year["annee"],
    y=df_year[kpi],
    mode='lines+markers',
    name=kpi_label,
    line=dict(width=3),
    yaxis='y1'
))

# Variation (si existe)
if variation is not None and variation in df_year.columns:
    fig.add_trace(go.Scatter(
        x=df_year["annee"],
        y=df_year[variation],
        mode='lines+markers',
        name="Variation (%)",
        line=dict(dash='dot'),
        yaxis='y2'
    ))

# =========================
# LAYOUT PRO
# =========================

fig.update_layout(
    template="plotly_white",

    xaxis=dict(
        title="Année",
        tickmode='linear'
    ),

    yaxis=dict(
        title=kpi_label,
        showgrid=True
    ),

    yaxis2=dict(
        title="Variation (%)",
        overlaying='y',
        side='right',
        showgrid=False
    ),

    legend=dict(
        x=0.01,
        y=0.99,
        bgcolor="rgba(255,255,255,0.6)"
    ),

    margin=dict(l=40, r=40, t=40, b=40)
)

# =========================
# DISPLAY
# =========================

st.plotly_chart(fig, use_container_width=True)
