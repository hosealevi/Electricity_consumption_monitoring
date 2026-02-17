from modules.data_loader import load_data
from modules.cleaning import clean_data
from modules.kpi import compute_kpi
from modules.dashboard import compute_dashboard

print("=== LOADING DATA ===")
df, gdf_bat, gdf_elec = load_data()

print("Data loaded:", df.shape)

print("\n=== CLEANING ===")
df = clean_data(df)
print("After cleaning:", df.shape)

print("\n=== KPI CALCULATION ===")
df = compute_kpi(df)

print(df.head())

print("\n=== DASHBOARD ===")
dash = compute_dashboard(df)
print(dash.head())

print("\n=== TEST SUCCESSFUL ===")
