def compute_dashboard(df):

    dashboard = df.groupby("annee").agg({
        "facture_fcfa": "sum",
        "consommation_kwh": "sum",
        "taux_evolution_facture": "mean",
        "variation_cout_kwh": "mean",
        "depassement_kw": "sum",
        "taux_utilisation": "mean",
        "facteur_puissance": "mean",
        "penalite_cosphi": "mean"
    }).reset_index()

    return dashboard
