\# Smart Irrigation Intelligence System (SIIS)



\## Problem Statement

Agriculture accounts for \~80% of freshwater consumption in India, yet an estimated

30–40% of irrigation water is wasted due to over-watering and lack of real-time monitoring.

Farmers lack data-driven tools to decide \*when\*, \*where\*, and \*how much\* to irrigate.



This project builds an end-to-end data analytics pipeline to:

1\. Analyze historical soil moisture, weather, and crop data

2\. Detect zones at risk of water stress or over-irrigation

3\. Predict next-week soil moisture deficit using machine learning

4\. Deliver actionable insights via an interactive Power BI dashboard



\## Key Performance Indicators

| KPI | Definition | Target |

|-----|-----------|--------|

| Water Stress Index (WSI) | Demand vs supply gap, scored 0–10 | < 4 = healthy |

| Irrigation Efficiency Score (IES) | % of water applied that was actually needed | > 75% |

| Predicted Yield Loss % | ML-estimated yield drop due to water stress | Minimize |



\## Tools \& Technologies

\- \*\*Python\*\* — Data cleaning, EDA, feature engineering, ML model (scikit-learn)

\- \*\*SQL Server Express / SQLite\*\* — Star schema design, stored procedures, window functions

\- \*\*Power BI Desktop\*\* — DirectQuery dashboard, DAX measures, 3-page executive report



\## Data Sources

\- Kaggle: Crop Recommendation Dataset (soil nutrients, rainfall, crop labels)

\- Synthetic IoT Sensor Data: Simulated hourly soil moisture, temperature, humidity

\- Kaggle: Indian Agriculture Crop Production Statistics



\## Project Structure



SIIS\_Project/

├── data/raw/          → Original datasets

├── data/cleaned/      → Python-cleaned outputs

├── notebooks/         → EDA and exploration (Jupyter)

├── sql/schema/        → Star schema DDL scripts

├── sql/queries/       → Analysis queries, stored procedures

├── ml/                → Model training and evaluation

├── powerbi/           → .pbix dashboard file

├── exports/           → ML predictions fed back to SQL

└── README.md

## Key Findings
- **Summer is the highest stress season** — Drought Risk Score 14.0, nearly 2x Monsoon
- **91% of days** show WARNING or CRITICAL water stress levels
- **Temperature drives 67.5%** of water stress variance (Random Forest feature importance)
- **Zone_C** has the highest average WSI — priority zone for irrigation optimization
- **Cotton** shows highest water stress (WSI 6.40) vs Wheat lowest (WSI 6.15)
- ML model achieved **R² = 0.97, RMSE = 0.22** on Water Stress Index prediction

## Dashboard Screenshots

### Page 1 — Executive Overview
![Executive Overview](data/cleaned/dashboard_page1.png)

### Page 2 — Crop & Season Analysis
![Crop & Season Analysis](data/cleaned/dashboard_page2.png)

### Page 3 — ML Predictions
![ML Predictions](data/cleaned/dashboard_page3.png)

## How to Run
1. Clone this repository
2. Run `generate_sensor_data.py` to generate synthetic sensor data
3. Run `ml/load_to_sql.py` to load data into SQL Server
4. Open `notebooks/01_EDA.ipynb` for exploratory analysis
5. Run `ml/model_training.py` to train the ML model
6. Open `powerbi/SIIS_Dashboard.pbix` in Power BI Desktop



