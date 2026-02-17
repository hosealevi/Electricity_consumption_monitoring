def clean_data(df):

    df = df.copy()

    # tri
    df = df.sort_values(["batiment", "date"])

    # enlever valeurs invalides
    df = df[df["consommation_kwh"] > 0]

    # remplir NA
    df = df.fillna(method="ffill")

    return df
