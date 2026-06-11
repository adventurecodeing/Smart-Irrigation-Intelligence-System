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





