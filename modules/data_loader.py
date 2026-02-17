import pandas as pd
import geopandas as gpd
from config import DATA_PATH, GPKG_PATH, LAYER_BATIMENT, LAYER_ELECTRICITE

def load_data():

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])

    gdf_bat = gpd.read_file(GPKG_PATH, layer=LAYER_BATIMENT)
    gdf_elec = gpd.read_file(GPKG_PATH, layer=LAYER_ELECTRICITE)

    return df, gdf_bat, gdf_elec
