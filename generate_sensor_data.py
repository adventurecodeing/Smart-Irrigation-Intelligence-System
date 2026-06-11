import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'date': pd.date_range(start='2021-01-01', periods=n, freq='D'),
    'zone': np.random.choice(['Zone_A', 'Zone_B', 'Zone_C', 'Zone_D'], n),
    'crop_type': np.random.choice(['Rice', 'Wheat', 'Sugarcane', 'Cotton'], n),
    'soil_moisture_%': np.round(np.random.uniform(20, 80, n), 2),
    'temperature_C': np.round(np.random.uniform(18, 42, n), 1),
    'humidity_%': np.round(np.random.uniform(30, 90, n), 1),
    'rainfall_mm': np.round(np.random.exponential(scale=5, size=n), 2),
    'irrigation_applied_mm': np.round(np.random.uniform(0, 40, n), 2),
    'growth_stage': np.random.choice(['Sowing', 'Vegetative', 'Flowering', 'Harvesting'], n)
})

df.to_csv('C:/Users/dipas/SIIS_Project/data/raw/irrigation_sensor.csv', index=False)
print("Done! Rows:", len(df))
print(df.head())