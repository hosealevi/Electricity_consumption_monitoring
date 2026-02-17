from config import HOURS_PER_MONTH, COSPHI_THRESHOLD

def compute_kpi(df):

    df = df.copy()

    # facture
    df["facture_fcfa"] = df["consommation_kwh"] * df["cout_kwh_fcfa"]

    # évolution facture
    df["facture_prev"] = df.groupby("batiment")["facture_fcfa"].shift(1)
    df["taux_evolution_facture"] = (
        (df["facture_fcfa"] - df["facture_prev"]) / df["facture_prev"]
    ) * 100

    # variation coût
    df["cout_prev"] = df.groupby("batiment")["cout_kwh_fcfa"].shift(1)
    df["variation_cout_kwh"] = (
        (df["cout_kwh_fcfa"] - df["cout_prev"]) / df["cout_prev"]
    ) * 100

    # dépassement
    df["depassement_kw"] = (
        df["puissance_max_kw"] - df["puissance_souscrite_kw"]
    ).clip(lower=0)

    # utilisation
    df["taux_utilisation"] = (
        df["puissance_max_kw"] / df["puissance_souscrite_kw"]
    ) * 100

    # cosphi (approximation)
    df["puissance_moyenne_kw"] = df["consommation_kwh"] / HOURS_PER_MONTH
    df["facteur_puissance"] = (
        df["puissance_moyenne_kw"] / df["puissance_max_kw"]
    ).clip(0,1)

    # pénalité
    df["penalite_cosphi"] = (df["facteur_puissance"] < COSPHI_THRESHOLD).astype(int)

    return df
