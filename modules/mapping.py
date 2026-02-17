def prepare_map_data(df, gdf_bat, gdf_elec, annee, mois, kpi, compteur=None):

    # =========================
    # FILTRE TEMPOREL
    # =========================
    df_map = df[(df["annee"] == annee) & (df["mois"] == mois)]

    # =========================
    # FILTRE COMPTEUR
    # =========================
    if compteur is not None and compteur != "All":
        df_map = df_map[df_map["compteur"] == compteur]

    # =========================
    # AGREGER BATIMENT
    # =========================
    agg_bat = df_map.groupby("batiment")[kpi].sum().reset_index()

    # harmonisation
    gdf_bat["nom"] = gdf_bat["nom"].str.lower().str.strip()
    agg_bat["batiment"] = agg_bat["batiment"].str.lower().str.strip()

    gdf_bat_map = gdf_bat.merge(
        agg_bat,
        left_on="nom",
        right_on="batiment",
        how="left"
    )

    gdf_bat_map[kpi] = gdf_bat_map[kpi].fillna(0)

    # =========================
    # FILTRER BATIMENTS NON LIES
    # =========================
    if compteur is not None and compteur != "All":
        batiments_valides = df_map["batiment"].unique()
        gdf_bat_map = gdf_bat_map[
            gdf_bat_map["nom"].isin(batiments_valides)
            | (gdf_bat_map["type"] != "batiment")
        ]

    # =========================
    # ELECTRICITE
    # =========================
    agg_compteur = df_map.groupby("compteur")[kpi].sum().reset_index()

    gdf_elec_map = gdf_elec.merge(
        agg_compteur,
        on="compteur",
        how="left"
    )

    gdf_elec_map[kpi] = gdf_elec_map[kpi].fillna(0)

    # filtrer réseau aussi
    if compteur is not None and compteur != "All":
        gdf_elec_map = gdf_elec_map[
            gdf_elec_map["compteur"] == compteur
        ]

    return gdf_bat_map, gdf_elec_map
