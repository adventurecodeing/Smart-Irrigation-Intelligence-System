USE SIIS_DB;
GO

-- Rank crops by total water consumed per season
-- Uses DENSE_RANK window function
WITH crop_season_water AS (
    SELECT
        c.crop_name,
        d.season,
        ROUND(SUM(f.rainfall_mm + f.irrigation_applied_mm), 2) AS total_water_mm,
        ROUND(AVG(f.WSI), 2)                                    AS avg_WSI,
        ROUND(AVG(f.soil_moisture_pct), 2)                      AS avg_soil_moisture,
        COUNT(*)                                                 AS record_count
    FROM fact_irrigation f
    JOIN dim_crop c ON f.crop_id = c.crop_id
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY c.crop_name, d.season
)
SELECT
    crop_name,
    season,
    total_water_mm,
    avg_WSI,
    avg_soil_moisture,
    DENSE_RANK() OVER (
        PARTITION BY season
        ORDER BY total_water_mm DESC
    ) AS water_consumption_rank
FROM crop_season_water
ORDER BY season, water_consumption_rank; 