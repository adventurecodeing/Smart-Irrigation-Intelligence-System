USE SIIS_DB;
GO

-- Stored procedure: generate alert report for any zone and WSI threshold
CREATE PROCEDURE sp_IrrigationAlert
    @zone_name  VARCHAR(50) = 'All',
    @wsi_threshold DECIMAL(5,2) = 7.0
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        z.zone_name,
        d.full_date,
        d.season,
        c.crop_name,
        gs.stage_name                       AS growth_stage,
        ROUND(f.WSI, 2)                     AS WSI,
        ROUND(f.drought_risk_score, 2)      AS drought_risk,
        ROUND(f.soil_moisture_pct, 2)       AS soil_moisture_pct,
        ROUND(f.temperature_c, 2)           AS temperature_c,
        CASE
            WHEN f.WSI >= 9 THEN 'SEVERE'
            WHEN f.WSI >= 7 THEN 'CRITICAL'
            WHEN f.WSI >= 4 THEN 'WARNING'
            ELSE 'NORMAL'
        END AS alert_level
    FROM fact_irrigation f
    JOIN dim_zone  z  ON f.zone_id  = z.zone_id
    JOIN dim_date  d  ON f.date_id  = d.date_id
    JOIN dim_crop  c  ON f.crop_id  = c.crop_id
    JOIN dim_growth_stage gs ON f.stage_id = gs.stage_id
    WHERE f.WSI >= @wsi_threshold
      AND (@zone_name = 'All' OR z.zone_name = @zone_name)
    ORDER BY f.WSI DESC, d.full_date;
END;
GO

-- Test the stored procedure
EXEC sp_IrrigationAlert @zone_name = 'All',   @wsi_threshold = 7.0;
EXEC sp_IrrigationAlert @zone_name = 'Zone_A', @wsi_threshold = 4.0;