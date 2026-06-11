USE SIIS_DB;
GO

-- Compare irrigation efficiency season over season
-- Uses LAG() to calculate change from previous season
WITH seasonal_stats AS (
    SELECT
        d.season,
        d.year,
        ROUND(AVG(f.IES), 2)                AS avg_efficiency,
        ROUND(AVG(f.WSI), 2)                AS avg_WSI,
        ROUND(AVG(f.drought_risk_score), 2) AS avg_drought_risk,
        ROUND(SUM(f.irrigation_applied_mm), 2) AS total_irrigation_mm,
        COUNT(*)                            AS days_count
    FROM fact_irrigation f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.season, d.year
)
SELECT
    season,
    year,
    avg_efficiency,
    avg_WSI,
    avg_drought_risk,
    total_irrigation_mm,
    LAG(avg_efficiency) OVER (
        PARTITION BY season
        ORDER BY year
    ) AS prev_year_efficiency,
    ROUND(avg_efficiency - LAG(avg_efficiency) OVER (
        PARTITION BY season
        ORDER BY year
    ), 2) AS efficiency_change,
    ROUND(avg_WSI - LAG(avg_WSI) OVER (
        PARTITION BY season
        ORDER BY year
    ), 2) AS WSI_change_YoY
FROM seasonal_stats
ORDER BY season, year;