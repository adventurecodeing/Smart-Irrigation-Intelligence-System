USE SIIS_DB;
GO

-- Rolling 7-day average soil moisture per zone
-- Shows trend smoothing to identify drying patterns
SELECT
    f.record_id,
    d.full_date,
    z.zone_name,
    f.soil_moisture_pct,
    ROUND(AVG(f.soil_moisture_pct) OVER (
        PARTITION BY f.zone_id
        ORDER BY d.full_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_7day_avg_moisture,
    ROUND(f.soil_moisture_pct - AVG(f.soil_moisture_pct) OVER (
        PARTITION BY f.zone_id
        ORDER BY d.full_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS deviation_from_rolling_avg
FROM fact_irrigation f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_zone z ON f.zone_id = z.zone_id
ORDER BY z.zone_name, d.full_date;