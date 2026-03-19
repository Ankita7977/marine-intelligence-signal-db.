-- =========================================
-- Enable PostGIS Extension
-- =========================================
CREATE EXTENSION IF NOT EXISTS postgis;


-- =========================================
-- Dataset Registry Table (LINEAGE)
-- =========================================
CREATE TABLE dataset_registry (
    dataset_id INT PRIMARY KEY,
    dataset_name TEXT,
    source_type TEXT,
    description TEXT
);


-- =========================================
-- Marine Signals Table (INTELLIGENCE READY)
-- =========================================
CREATE TABLE marine_signals (
    signal_id SERIAL PRIMARY KEY,
    dataset_id INT,
    timestamp TIMESTAMP,
    latitude FLOAT,
    longitude FLOAT,
    geom GEOGRAPHY(Point, 4326),  -- Geospatial support
    feature_type TEXT,
    normalized_value FLOAT,
    unit TEXT,
    confidence_score FLOAT,
    truth_flag BOOLEAN,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key (LINEAGE)
    FOREIGN KEY (dataset_id) REFERENCES dataset_registry(dataset_id)
);


-- =========================================
-- INDEXES (SCALABILITY + PERFORMANCE)
-- =========================================
CREATE INDEX idx_marine_dataset_id 
ON marine_signals(dataset_id);

CREATE INDEX idx_marine_timestamp 
ON marine_signals(timestamp);

CREATE INDEX idx_marine_feature_type 
ON marine_signals(feature_type);

-- Spatial Index (IMPORTANT for PostGIS)
CREATE INDEX idx_marine_geom 
ON marine_signals USING GIST (geom);


-- =========================================
-- PARTITIONING (FUTURE-READY DESIGN)
-- =========================================
-- NOTE:
-- Table can be partitioned later using:
-- RANGE (timestamp) → for time-based scaling
-- LIST (feature_type) → for signal-type scaling
