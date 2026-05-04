BULK INSERT AQI_Data
FROM 'C:\Users\asif6\Downloads\AQI_Air_Quality_Dataset.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK
);

SELECT*
FROM AQI_Data


-- QUERY 1
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT city) AS unique_cities,
    COUNT(DISTINCT country) AS unique_countries,
    MIN(date) AS earliest_date,
    MAX(date) AS latest_date,
    ROUND(AVG(PM2_5), 2) AS avg_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10
FROM AQI_Data;

-- QUERY 2
SELECT
    city,
    COUNT(*) AS readings,
    ROUND(AVG(PM2_5), 2) AS avg_pm25,
    ROUND(MAX(PM2_5), 2) AS max_pm25,
    ROUND(MIN(PM2_5), 2) AS min_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10,
    ROUND(AVG(no2), 2) AS avg_no2,
    ROUND(AVG(so2), 2) AS avg_so2,
    ROUND(AVG(co), 2) AS avg_co,
    ROUND(AVG(o3), 2) AS avg_o3
FROM AQI_Data
GROUP BY city
ORDER BY avg_pm25 DESC;

-- QUERY 3
SELECT
    city,
    date,
    PM2_5,
    CASE
        WHEN PM2_5 < 12.0 THEN 'Good'
        WHEN PM2_5 < 35.4 THEN 'Moderate'
        WHEN PM2_5 < 55.4 THEN 'Unhealthy for Sensitive Groups'
        WHEN PM2_5 < 150.4 THEN 'Unhealthy'
        WHEN PM2_5 < 250.4 THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS aqi_category
FROM AQI_Data
ORDER BY PM2_5 DESC;

-- QUERY 4
SELECT
    aqi_category,
    COUNT(*) AS total_days,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM AQI_Data), 1) AS pct
FROM (
    SELECT
        CASE
            WHEN PM2_5 < 12.0 THEN 'Good'
            WHEN PM2_5 < 35.4 THEN 'Moderate'
            WHEN PM2_5 < 55.4 THEN 'Unhealthy for Sensitive Groups'
            WHEN PM2_5 < 150.4 THEN 'Unhealthy'
            WHEN PM2_5 < 250.4 THEN 'Very Unhealthy'
            ELSE 'Hazardous'
        END AS aqi_category
    FROM AQI_Data
) sub
GROUP BY aqi_category
ORDER BY total_days DESC;

-- QUERY 5 
SELECT
    CONVERT(VARCHAR(7), date, 120) AS year_month,
    ROUND(AVG(PM2_5), 2) AS avg_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10,
    ROUND(AVG(no2), 2) AS avg_no2
FROM AQI_Data
GROUP BY CONVERT(VARCHAR(7), date, 120)
ORDER BY year_month;

-- QUERY 6
SELECT
    city,
    CONVERT(VARCHAR(7), date, 120) AS year_month,
    ROUND(AVG(PM2_5), 2) AS avg_pm25
FROM AQI_Data
GROUP BY city, CONVERT(VARCHAR(7), date, 120)
ORDER BY city, year_month;

-- QUERY 7
SELECT TOP 10
    sr_no,
    city,
    date,
    PM2_5,
    pm10,
    no2,
    so2,
    CASE
        WHEN PM2_5 < 55.4 THEN 'Unhealthy for Sensitive Groups'
        WHEN PM2_5 < 150.4 THEN 'Unhealthy'
        WHEN PM2_5 < 250.4 THEN 'Very Unhealthy'
        ELSE 'Hazardous'
    END AS aqi_category
FROM AQI_Data
ORDER BY PM2_5 DESC;

-- QUERY 8
SELECT TOP 10
    city,
    date,
    PM2_5,
    CASE
        WHEN PM2_5 < 12.0 THEN 'Good'
        WHEN PM2_5 < 35.4 THEN 'Moderate'
        ELSE 'Unhealthy for Sensitive Groups'
    END AS aqi_category
FROM AQI_Data
ORDER BY PM2_5 ASC;

-- QUERY 9 
SELECT 'PM2.5' AS pollutant, city, avg_value
FROM (
    SELECT TOP 1 city, AVG(PM2_5) AS avg_value
    FROM AQI_Data
    GROUP BY city
    ORDER BY AVG(PM2_5) DESC
) t

UNION ALL

SELECT 'PM10', city, avg_value
FROM (
    SELECT TOP 1 city, AVG(pm10) AS avg_value
    FROM AQI_Data
    GROUP BY city
    ORDER BY AVG(pm10) DESC
) t

UNION ALL

SELECT 'NO2', city, avg_value
FROM (
    SELECT TOP 1 city, AVG(no2) AS avg_value
    FROM AQI_Data
    GROUP BY city
    ORDER BY AVG(no2) DESC
) t

UNION ALL

SELECT 'SO2', city, avg_value
FROM (
    SELECT TOP 1 city, AVG(so2) AS avg_value
    FROM AQI_Data
    GROUP BY city
    ORDER BY AVG(so2) DESC
) t

UNION ALL

SELECT 'CO', city, avg_value
FROM (
    SELECT TOP 1 city, AVG(co) AS avg_value
    FROM AQI_Data
    GROUP BY city
    ORDER BY AVG(co) DESC
) t

UNION ALL

SELECT 'O3', city, avg_value
FROM (
    SELECT TOP 1 city, AVG(o3) AS avg_value
    FROM AQI_Data
    GROUP BY city
    ORDER BY AVG(o3) DESC
) t;


-- QUERY 10
SELECT
    CASE
        WHEN temperature < 22 THEN 'Cold'
        WHEN temperature < 28 THEN 'Mild'
        WHEN temperature < 34 THEN 'Warm'
        ELSE 'Hot'
    END AS temp_range,
    COUNT(*) AS readings,
    ROUND(AVG(PM2_5), 2) AS avg_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10
FROM AQI_Data
GROUP BY CASE
        WHEN temperature < 22 THEN 'Cold'
        WHEN temperature < 28 THEN 'Mild'
        WHEN temperature < 34 THEN 'Warm'
        ELSE 'Hot'
    END
ORDER BY avg_pm25 DESC;

-- QUERY 11
SELECT
    CASE
        WHEN humidity < 40  THEN 'Dry (<40%)'
        WHEN humidity < 60  THEN 'Comfortable (40–60%)'
        WHEN humidity < 75  THEN 'Humid (60–75%)'
        ELSE 'Very Humid (>75%)'
    END AS humidity_range,
    COUNT(*) AS readings,
    ROUND(AVG(PM2_5), 2) AS avg_pm25
FROM AQI_Data
GROUP BY 
    CASE
        WHEN humidity < 40  THEN 'Dry (<40%)'
        WHEN humidity < 60  THEN 'Comfortable (40–60%)'
        WHEN humidity < 75  THEN 'Humid (60–75%)'
        ELSE 'Very Humid (>75%)'
    END
ORDER BY avg_pm25 DESC;

-- QUERY 12
SELECT
    CASE
        WHEN wind_speed < 2   THEN 'Calm (<2 m/s)'
        WHEN wind_speed < 4   THEN 'Light (2–4 m/s)'
        WHEN wind_speed < 6   THEN 'Moderate (4–6 m/s)'
        ELSE 'Strong (>6 m/s)'
    END AS wind_range,
    COUNT(*) AS readings,
    ROUND(AVG(PM2_5), 2) AS avg_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10
FROM AQI_Data
GROUP BY 
    CASE
        WHEN wind_speed < 2   THEN 'Calm (<2 m/s)'
        WHEN wind_speed < 4   THEN 'Light (2–4 m/s)'
        WHEN wind_speed < 6   THEN 'Moderate (4–6 m/s)'
        ELSE 'Strong (>6 m/s)'
    END
ORDER BY avg_pm25 DESC;

-- QUERY 13
WITH city_stats AS (
    SELECT
        city,
        AVG(PM2_5) AS a_pm25,	
        AVG(pm10) AS a_pm10,
        AVG(no2)  AS a_no2,
        AVG(so2)  AS a_so2,
        AVG(co)   AS a_co
    FROM AQI_Data
    GROUP BY city
)
SELECT
    city,
    ROUND(a_pm25, 2) AS avg_pm25,
    ROUND(a_pm10, 2) AS avg_pm10,
    ROUND(a_no2,  2) AS avg_no2,
    ROUND(a_so2,  2) AS avg_so2,
    ROUND(a_co,   2) AS avg_co,
    ROUND((a_pm25/179.95 + a_pm10/219.63 + a_no2/70 + a_so2/60 + a_co/2) / 5 * 100, 2)
        AS composite_pollution_index
FROM city_stats
ORDER BY composite_pollution_index DESC;

-- QUERY 14
SELECT 
    city,
    date,
    PM2_5,
    pm10,
    no2,
    so2
FROM AQI_Data
WHERE PM2_5 > (SELECT AVG(PM2_5) FROM AQI_Data)
  AND pm10 > (SELECT AVG(pm10) FROM AQI_Data)
  AND no2  > (SELECT AVG(no2) FROM AQI_Data)
  AND so2  > (SELECT AVG(so2) FROM AQI_Data)
ORDER BY PM2_5 DESC;

-- QUERY 15
SELECT
    t1.city,
    t1.date,
    t1.pm2_5,
    ROUND((
        SELECT AVG(t2.pm2_5)
        FROM AQI_Data t2
        WHERE t2.city = t1.city
          AND t2.date BETWEEN DATEADD(DAY, -6, t1.date) AND t1.date
    ), 2) AS rolling_7day_pm25
FROM AQI_Data t1
ORDER BY t1.city, t1.date;

-- QUERY 16
SELECT
    city,
    ROUND(MIN(pm2_5),  2) AS min_pm25,
    ROUND(AVG(pm2_5),  2) AS avg_pm25,
    ROUND(MAX(pm2_5),  2) AS max_pm25,
    ROUND(AVG(pm2_5) - 2*STDEV(pm2_5), 2) AS low_2sigma,
    ROUND(AVG(pm2_5) + 2*STDEV(pm2_5), 2) AS high_2sigma
FROM AQI_Data
GROUP BY city;

-- QUERY 17
SELECT
    city,
    ROUND(AVG(o3), 2) AS avg_o3,
    ROUND(MAX(o3), 2) AS max_o3,
    ROUND(MIN(o3), 2) AS min_o3
FROM AQI_Data
GROUP BY city
ORDER BY avg_o3 DESC;

-- QUERY 18
SELECT
    city,
    ROUND(AVG(co), 3) AS avg_co,
    ROUND(MAX(co), 3) AS max_co,
    SUM(CASE WHEN co > 1.5 THEN 1 ELSE 0 END) AS days_above_1_5
FROM AQI_Data
GROUP BY city
ORDER BY avg_co DESC;

-- QUERY 19
SELECT
    CASE MONTH(date)
        WHEN 1 THEN '01-January'
        WHEN 2 THEN '02-February'
        WHEN 3 THEN '03-March'
        WHEN 4 THEN '04-April'
        WHEN 5 THEN '05-May'
    END AS month_name,
    COUNT(*) AS readings,
    ROUND(AVG(pm2_5), 2) AS avg_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10,
    ROUND(AVG(no2), 2) AS avg_no2,
    ROUND(AVG(temperature), 2) AS avg_temp,
    ROUND(AVG(humidity), 2) AS avg_humidity
FROM AQI_Data
GROUP BY MONTH(date)
ORDER BY MONTH(date);

-- QUERY 20
SELECT
    city,
    ROUND(AVG(PM2_5), 2) AS avg_pm25,
    ROUND(AVG(pm10), 2) AS avg_pm10,
    ROUND(AVG(PM2_5) / NULLIF(AVG(pm10), 0), 3) AS pm25_to_pm10_ratio
FROM AQI_Data
GROUP BY city
ORDER BY pm25_to_pm10_ratio DESC;