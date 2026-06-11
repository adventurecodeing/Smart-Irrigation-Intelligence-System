import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
import pyodbc
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("SIIS — ML Model Training")
print("=" * 50)

# 1. Load cleaned data
df = pd.read_csv(r'C:\Users\dipas\SIIS_Project\data\cleaned\irrigation_cleaned.csv',
                 parse_dates=['date'])
print(f"\n Data loaded: {df.shape}")

#  2. Feature Engineering 
df['month']   = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['season']  = df['month'].map({
    12:'Winter', 1:'Winter',  2:'Winter',
    3:'Summer',  4:'Summer',  5:'Summer',
    6:'Monsoon', 7:'Monsoon', 8:'Monsoon',
    9:'Post-Monsoon', 10:'Post-Monsoon', 11:'Post-Monsoon'
})

# Encode categoricals
le_zone   = LabelEncoder()
le_crop   = LabelEncoder()
le_stage  = LabelEncoder()
le_season = LabelEncoder()

df['zone_enc']   = le_zone.fit_transform(df['zone'])
df['crop_enc']   = le_crop.fit_transform(df['crop_type'])
df['stage_enc']  = le_stage.fit_transform(df['growth_stage'])
df['season_enc'] = le_season.fit_transform(df['season'])

print("Features engineered")

#  3. Define Features & Target 
# Target: WSI (Water Stress Index) — predicting next period stress
features = [
    'temperature_C', 'humidity_%', 'rainfall_mm',
    'irrigation_applied_mm', 'soil_moisture_%',
    'month', 'quarter',
    'zone_enc', 'crop_enc', 'stage_enc', 'season_enc'
]

X = df[features]
y = df['WSI']

print(f"Features: {len(features)}")
print(f"   Target: WSI (Water Stress Index)")

#  4. Train/Test Split 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n Train size: {X_train.shape[0]} | Test size: {X_test.shape[0]}")

#  5. Model 1: Linear Regression 
print("\n--- Linear Regression ---")
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

lr_r2   = r2_score(y_test, y_pred_lr)
lr_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lr))
lr_mae  = mean_absolute_error(y_test, y_pred_lr)
lr_cv   = cross_val_score(lr, X, y, cv=5, scoring='r2').mean()

print(f"  R²:        {lr_r2:.4f}")
print(f"  RMSE:      {lr_rmse:.4f}")
print(f"  MAE:       {lr_mae:.4f}")
print(f"  CV R² (5): {lr_cv:.4f}")

#  6. Model 2: Random Forest 
print("\n--- Random Forest Regressor ---")
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

rf_r2   = r2_score(y_test, y_pred_rf)
rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
rf_mae  = mean_absolute_error(y_test, y_pred_rf)
rf_cv   = cross_val_score(rf, X, y, cv=5, scoring='r2').mean()

print(f"  R²:        {rf_r2:.4f}")
print(f"  RMSE:      {rf_rmse:.4f}")
print(f"  MAE:       {rf_mae:.4f}")
print(f"  CV R² (5): {rf_cv:.4f}")

# 7. Feature Importance (Random Forest) 
print("\n--- Feature Importance ---")
importance_df = pd.DataFrame({
    'feature'   : features,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)
print(importance_df.to_string(index=False))

# 8. Pick Best Model & Generate Predictions 
print("\n--- Model Selection ---")
best_model = rf if rf_r2 > lr_r2 else lr
best_name  = "Random Forest" if rf_r2 > lr_r2 else "Linear Regression"
best_r2    = max(rf_r2, lr_r2)
print(f"  Best model: {best_name} (R² = {best_r2:.4f})")

# Generate predictions on full dataset
df['predicted_WSI'] = best_model.predict(X)
df['prediction_error'] = (df['predicted_WSI'] - df['WSI']).round(4)
df['alert_level'] = pd.cut(
    df['predicted_WSI'],
    bins     = [-np.inf, 4, 7, 9, np.inf],
    labels   = ['NORMAL', 'WARNING', 'CRITICAL', 'SEVERE']
)

print(f"\n Predictions generated for all {len(df)} records")
print("\nAlert level distribution:")
print(df['alert_level'].value_counts())

#  9. Export predictions to CSV 
export_cols = [
    'date', 'zone', 'crop_type', 'growth_stage', 'season',
    'soil_moisture_%', 'temperature_C', 'WSI',
    'predicted_WSI', 'prediction_error', 'alert_level'
]
predictions_df = df[export_cols].copy()
predictions_df['predicted_WSI']    = predictions_df['predicted_WSI'].round(4)
predictions_df['date']             = predictions_df['date'].dt.strftime('%Y-%m-%d')

predictions_df.to_csv(
    r'C:\Users\dipas\SIIS_Project\exports\predictions.csv',
    index=False
)
print("\n Predictions exported to exports/predictions.csv")

# ── 10. Save metrics to CSV ───────────────────────
metrics_df = pd.DataFrame([
    {
        'model'    : 'Linear Regression',
        'R2'       : round(lr_r2,  4),
        'RMSE'     : round(lr_rmse,4),
        'MAE'      : round(lr_mae, 4),
        'CV_R2'    : round(lr_cv,  4)
    },
    {
        'model'    : 'Random Forest',
        'R2'       : round(rf_r2,  4),
        'RMSE'     : round(rf_rmse,4),
        'MAE'      : round(rf_mae, 4),
        'CV_R2'    : round(rf_cv,  4)
    }
])
metrics_df.to_csv(
    r'C:\Users\dipas\SIIS_Project\exports\model_metrics.csv',
    index=False
)
print(" Model metrics saved to exports/model_metrics.csv")

# ── 11. Push predictions back to SQL Server ───────
print("\n--- Pushing predictions to SQL Server ---")

# First create the table in SSMS if not exists
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP1\\SQLEXPRESS;"
    "DATABASE=SIIS_DB;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

# Create predictions table
cursor.execute("""
    IF NOT EXISTS (
        SELECT * FROM sysobjects 
        WHERE name='ml_predictions' AND xtype='U'
    )
    CREATE TABLE ml_predictions (
        pred_id         INT IDENTITY(1,1) PRIMARY KEY,
        pred_date       DATE,
        zone_name       VARCHAR(50),
        crop_name       VARCHAR(50),
        growth_stage    VARCHAR(50),
        season          VARCHAR(50),
        soil_moisture   DECIMAL(5,2),
        temperature     DECIMAL(5,2),
        actual_WSI      DECIMAL(5,2),
        predicted_WSI   DECIMAL(5,2),
        prediction_error DECIMAL(5,2),
        alert_level     VARCHAR(20)
    )
""")
conn.commit()
print(" ml_predictions table ready")

# Insert predictions
insert_sql = """
    INSERT INTO ml_predictions (
        pred_date, zone_name, crop_name, growth_stage, season,
        soil_moisture, temperature, actual_WSI,
        predicted_WSI, prediction_error, alert_level
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
"""

rows = 0
for _, row in predictions_df.iterrows():
    cursor.execute(insert_sql, (
        row['date'],
        row['zone'],
        row['crop_type'],
        row['growth_stage'],
        row['season'],
        float(row['soil_moisture_%']),
        float(row['temperature_C']),
        float(row['WSI']),
        float(row['predicted_WSI']),
        float(row['prediction_error']),
        str(row['alert_level'])
    ))
    rows += 1
    if rows % 100 == 0:
        print(f"  Pushed {rows} predictions...")

conn.commit()
cursor.close()
conn.close()

print(f"\n {rows} predictions pushed to SQL Server")
print("\n" + "=" * 50)
print("=" * 50)