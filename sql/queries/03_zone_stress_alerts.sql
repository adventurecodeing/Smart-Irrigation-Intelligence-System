USE SIIS_DB;
GO

-- Identify zones with consecutive high-stress days
-- A zone is flagged if WSI > 7 for 3 or more consecutive days
WITH daily_stress AS (
    SELECT
        z.zone_name,
        d.full_date,
        d.season,
        f.WSI,
        f.drought_risk_score,
        CASE WHEN f.WSI >= 7 THEN 1 ELSE 0 END AS is_critical
    FROM fact_irrigation f
    JOIN dim_date d  ON f.date_id = d.date_id
    JOIN dim_zone z  ON f.zone_id = z.zone_id
),
stress_groups AS (
    SELECT
        zone_name,
        full_date,
        season,
        WSI,
        drought_risk_score,
        is_critical,
        SUM(is_critical) OVER (
            PARTITION BY zone_name
            ORDER BY full_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS stress_3day_sum
    FROM daily_stress
)
SELECT
    zone_name,
    full_date,
    season,
    ROUND(WSI, 2)               AS WSI,
    ROUND(drought_risk_score,2) AS drought_risk_score,
    CASE
        WHEN stress_3day_sum = 3 THEN 'CRITICAL ALERT'
        WHEN WSI >= 4            THEN ' WARNING'
        ELSE                          ' NORMAL'
    END AS alert_status
FROM stress_groups
WHERE WSI >= 4
ORDER BY zone_name, full_date;