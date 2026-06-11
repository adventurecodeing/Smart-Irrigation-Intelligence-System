USE SIIS_DB;
GO

-- Top 5 highest stress days per zone using ROW_NUMBER()
WITH ranked_stress AS (
    SELECT
        z.zone_name,
        d.full_date,
        d.season,
        c.crop_name,
        ROUND(f.WSI, 2)                AS WSI,
        ROUND(f.drought_risk_score,2)  AS drought_risk_score,
        ROUND(f.soil_moisture_pct, 2)  AS soil_moisture_pct,
        ROW_NUMBER() OVER (
            PARTITION BY z.zone_name
            ORDER BY f.WSI DESC
        ) AS stress_rank
    FROM fact_irrigation f
    JOIN dim_zone z ON f.zone_id = z.zone_id
    JOIN dim_date d ON f.date_id = d.date_id
    JOIN dim_crop c ON f.crop_id = c.crop_id
)
SELECT
    zone_name,
    stress_rank,
    full_date,
    season,
    crop_name,
    WSI,
    drought_risk_score,
    soil_moisture_pct
FROM ranked_stress
WHERE stress_rank <= 5
ORDER BY zone_name, stress_rank;