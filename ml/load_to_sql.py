import pandas as pd
import pyodbc

# Load cleaned CSV
df = pd.read_csv(r'C:\Users\dipas\SIIS_Project\data\cleaned\irrigation_cleaned.csv',
                 parse_dates=['date'])
print("CSV loaded  Shape:", df.shape)

# Connect using pyodbc directly — no SQLAlchemy
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP1\\SQLEXPRESS;"
    "DATABASE=SIIS_DB;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()
print("SQL Server connected ")

# Map dimension keys
zone_map  = {'Zone_A': 1, 'Zone_B': 2, 'Zone_C': 3, 'Zone_D': 4}
crop_map  = {'Rice': 1, 'Wheat': 2, 'Sugarcane': 3, 'Cotton': 4}
stage_map = {'Sowing': 1, 'Vegetative': 2, 'Flowering': 3, 'Harvesting': 4}

df['date_id']  = df['date'].dt.strftime('%Y%m%d').astype(int)
df['zone_id']  = df['zone'].map(zone_map)
df['crop_id']  = df['crop_type'].map(crop_map)
df['stage_id'] = df['growth_stage'].map(stage_map)

# Build fact dataframe
fact_df = df[[
    'date_id', 'zone_id', 'crop_id', 'stage_id',
    'soil_moisture_%', 'temperature_C', 'humidity_%',
    'rainfall_mm', 'irrigation_applied_mm',
    'ET0', 'water_supply', 'WSI', 'IES', 'drought_risk_score'
]].copy()

fact_df.columns = [
    'date_id', 'zone_id', 'crop_id', 'stage_id',
    'soil_moisture_pct', 'temperature_c', 'humidity_pct',
    'rainfall_mm', 'irrigation_applied_mm',
    'ET0', 'water_supply', 'WSI', 'IES', 'drought_risk_score'
]

print("Fact table prepared Shape:", fact_df.shape)

# Insert one row at a time — most reliable method
insert_sql = """
    INSERT INTO fact_irrigation (
        date_id, zone_id, crop_id, stage_id,
        soil_moisture_pct, temperature_c, humidity_pct,
        rainfall_mm, irrigation_applied_mm,
        ET0, water_supply, WSI, IES, drought_risk_score
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

rows_inserted = 0
for _, row in fact_df.iterrows():
    cursor.execute(insert_sql, (
        int(row['date_id']),
        int(row['zone_id']),
        int(row['crop_id']),
        int(row['stage_id']),
        float(row['soil_moisture_pct']),
        float(row['temperature_c']),
        float(row['humidity_pct']),
        float(row['rainfall_mm']),
        float(row['irrigation_applied_mm']),
        float(row['ET0']),
        float(row['water_supply']),
        float(row['WSI']),
        float(row['IES']),
        float(row['drought_risk_score'])
    ))
    rows_inserted += 1
    if rows_inserted % 100 == 0:
        print(f"  Inserted {rows_inserted} rows...")

conn.commit()
cursor.close()
conn.close()
print(f"Data loaded into SQL Server  Total rows: {rows_inserted}")