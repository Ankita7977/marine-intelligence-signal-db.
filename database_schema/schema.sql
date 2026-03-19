-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

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
USING GIST (geom);

CREATE INDEX idx_marine_signals_timestamp
ON marine_signals(timestamp);

CREATE INDEX idx_marine_signals_feature
ON marine_signals(feature_type);

-- Dataset Registry Table
CREATE TABLE dataset_registry (
dataset_id TEXT PRIMARY KEY,
dataset_name TEXT,
source TEXT,
schema_version TEXT,
update_frequency TEXT,
trust_level TEXT,
ingestion_method TEXT,
last_update_timestamp TIMESTAMP
);

-- Marine Signals Table
CREATE TABLE ingestion_log (
run_id SERIAL PRIMARY KEY,
dataset_id TEXT,
records_ingested INTEGER,
records_rejected INTEGER,
start_time TIMESTAMP,
end_time TIMESTAMP,
status TEXT,
notes TEXT
);


CREATE TABLE dataset_registry (
    dataset_id INT PRIMARY KEY,
    dataset_name TEXT,
    source_type TEXT,
    description TEXT
);

CREATE TABLE marine_signals (
    signal_id SERIAL PRIMARY KEY,
    dataset_id INT,
    timestamp TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    feature_type TEXT,
    normalized_value FLOAT,
    unit TEXT,
    confidence_score FLOAT,
    truth_flag BOOLEAN,
    FOREIGN KEY (dataset_id) REFERENCES dataset_registry(dataset_id)
);

