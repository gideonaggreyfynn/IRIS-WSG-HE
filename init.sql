CREATE SCHEMA IF NOT EXISTS iris_staging;

CREATE TABLE IF NOT EXISTS iris_staging.water_protection_zones (
    source_zone_id VARCHAR(255) NOT NULL,
    state_code VARCHAR(2) NOT NULL,
    zone_code VARCHAR(50),
    restriction_category VARCHAR(50),
    extraction_rate FLOAT,
    geometry geometry(Geometry, 25832),
    source_url TEXT,
    source_updated_at TIMESTAMP,
    ingested_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (source_zone_id, state_code)
);