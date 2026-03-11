import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from modules.data_loader import load_data
from modules.cleaning import clean_data
from modules.kpi import compute_kpi
from modules.logo import render_header

render_header()
df, _, _ = load_data()
df = clean_data(df)
df = compute_kpi(df)

# KPI selector
kpi = st.selectbox("Select KPI", [
    "consommation_kwh",
    "facture_fcfa",
    "taux_evolution_facture"
])

# -------------------------
# BOXPLOT
# -------------------------

st.subheader("Distribution mensuelle")

fig, ax = plt.subplots()
sns.boxplot(data=df, x="mois", y=kpi, ax=ax)

st.pyplot(fig)

# -------------------------
# SEASONAL LINE (mean)
# -------------------------

st.subheader("Tendance mensuelle (moyenne)")

season = df.groupby("mois")[kpi].mean().reset_index()

fig2 = px.line(season, x="mois", y=kpi, markers=True)
st.plotly_chart(fig2)

# -------------------------
# HEATMAP (VERY IMPORTANT)
# -------------------------

st.subheader("Seasonality Heatmap")

pivot = df.pivot_table(
    index="annee",
    columns="mois",
    values=kpi,
    aggfunc="mean"
)

fig3 = px.imshow(pivot, text_auto=True)
st.plotly_chart(fig3)
