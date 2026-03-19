-- Index for faster queries
CREATE INDEX idx_dataset_id ON marine_signals(dataset_id);
CREATE INDEX idx_timestamp ON marine_signals(timestamp);
CREATE INDEX idx_feature_type ON marine_signals(feature_type);

-- Dataset Registry Table
CREATE TABLE dataset_registry (
    dataset_id INT PRIMARY KEY,
    dataset_name TEXT,
    source_type TEXT,
    description TEXT
);

-- Marine Signals Table (INTELLIGENCE READY)
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

-- Indexes (SCALING SUPPORT)
CREATE INDEX idx_timestamp ON marine_signals(timestamp);
CREATE INDEX idx_feature_type ON marine_signals(feature_type);
