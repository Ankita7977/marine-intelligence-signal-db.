# Marine Intelligence Signal System

## Overview

This project focuses on building a reliable signal processing system for marine intelligence use cases.

The goal is to take different types of maritime and environmental datasets and convert them into a clean, consistent, and trustworthy signal layer that can be used for further analysis or simulation.

Instead of just storing data, the system ensures that every signal is:
- properly validated  
- traceable to its source  
- transformed using clear rules  

---

## What This Project Solves

In real-world datasets:
- data is often inconsistent  
- units are not standardized  
- some records are incomplete or unreliable  

This system addresses those issues by:
- applying proper normalization  
- removing invalid data  
- assigning confidence scores based on data quality  

---

## Key Features

### 1. Dataset Lineage

Each signal is linked to its source using `dataset_id`.

This ensures:
- no confusion between datasets  
- full traceability of every record  

---

### 2. Deterministic Normalization

All transformations are clearly defined and documented.

Example:
AIS vessel speed is converted from knots to meters per second using:

speed_mps = speed_knots * 0.514444

For datasets where unit information is missing (like weather data), values are kept as-is to avoid incorrect assumptions.

---

### 3. Confidence Scoring

Confidence is calculated using a rule-based approach:

- Base confidence = 0.5  
- Dataset adjustments:
  - AIS → +0.3  
  - Weather → +0.2  

- Penalty:
  - Missing latitude/longitude → -0.5  

Final confidence:
confidence = base + adjustments - penalties

---

### 4. Truth Validation

Each signal is marked as valid (`truth_flag = TRUE`) only if:
- value is present  
- timestamp is valid  
- confidence score is greater than zero  

Invalid data is not silently ignored — it is explicitly rejected.

---

### 5. Geospatial Integrity

Geospatial data is critical for marine intelligence.

- Records without latitude/longitude are removed  
- These removals are logged  
- No data is silently dropped  

Note:  
The water dataset was excluded completely because it did not contain valid geospatial information.

---

### 6. Deduplication

Duplicate records are removed based on:
- timestamp  
- latitude  
- longitude  
- feature_type  

---

### 7. Batch Processing

Data is inserted into the database in batches to improve performance and reliability.

---

## System Architecture

The system uses PostgreSQL with PostGIS for storing signals.

### Main Tables

- marine_signals → stores processed and validated signals  
- dataset_registry → maintains dataset metadata  
- ingestion_log → tracks ingestion runs  

Geospatial data is stored using POINT geometry (PostGIS), enabling efficient spatial queries.

---

## Ingestion Pipeline

The pipeline performs the following steps:

1. Load datasets  
2. Assign dataset_id  
3. Apply normalization rules  
4. Validate records  
5. Assign confidence scores  
6. Apply truth validation  
7. Remove duplicates  
8. Insert data in batches  
9. Log results  

---

## Validation Rules

Before inserting data:

- Latitude must be between -90 and 90  
- Longitude must be between -180 and 180  
- Timestamp must be valid  
- normalized_value must not be null  

Invalid records are stored separately for transparency.

---

## Project Structure

marine-intelligence-signal-db  
│  
├── config/  
│   └── config.yaml  
│  
├── database_schema/  
│   └── schema.sql  
│  
├── docs/  
│   ├── normalization_rules.md  
│   ├── confidence_rules.md  
│  
├── ingestion_pipeline/  
│   └── ingest_signals.py  
│  
├── data/  
│   └── dataset_registry.csv  
│  
└── README.md  

---

## Design Approach

This system is built with a simple principle:

Do not assume anything about the data unless it is clearly defined.

So:
- no fake values are added  
- no units are guessed  
- no data is silently ignored  

Everything is:
- explicit  
- documented  
- reproducible  

---

## Final Outcome

The system produces:
- clean and validated signals  
- fully traceable records  
- consistent outputs  

These signals can be directly used for:
- analysis  
- modeling  
- simulation systems  

---

## Technologies Used

- PostgreSQL  
- PostGIS  
- Python  
- Pandas  

---

## Final Note

This project focuses on building a system that can be trusted, not just one that runs.
