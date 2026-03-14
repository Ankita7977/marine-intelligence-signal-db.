-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Dataset Registry Table
CREATE TABLE dataset_registry (
dataset_id SERIAL PRIMARY KEY,
dataset_name TEXT,
source TEXT,
ingestion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ingestion Log Table
CREATE TABLE ingestion_log (
log_id SERIAL PRIMARY KEY,
dataset_id INTEGER,
records_inserted INTEGER,
records_rejected INTEGER,
ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Marine Signals Table
CREATE TABLE marine_signals (
signal_id SERIAL PRIMARY KEY,
source_id TEXT,
timestamp TIMESTAMP,
latitude DOUBLE PRECISION,
longitude DOUBLE PRECISION,
geom GEOGRAPHY(Point, 4326),
feature_type TEXT,
normalized_value DOUBLE PRECISION,
source_reference TEXT,
truth_level INTEGER,
confidence_score DOUBLE PRECISION,
ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Spatial Index
CREATE INDEX idx_marine_signals_geom
ON marine_signals
USING GIST(geom);
