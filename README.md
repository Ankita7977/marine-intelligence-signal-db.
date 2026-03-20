# Marine Intelligence Signal System (Task 3)

## Overview

This project focuses on building a reliable signal processing system for marine intelligence use cases.

The goal is to take different types of maritime and environmental datasets and convert them into a clean, consistent, and trustworthy signal layer that can be used for further analysis or simulation.

Instead of just storing data, this system ensures that every signal is:
- properly validated  
- traceable to its source  
- transformed using clearly defined rules  

---

## Task Context

This project is part of the Marine Intelligence pipeline development.

In Task 2:
- Data was stored in a unified schema  
- A basic ingestion pipeline was implemented  

In Task 3:
- True normalization logic is implemented  
- Dataset lineage is enforced using dataset_id  
- Confidence scoring is rule-based (not hardcoded)  
- Geospatial integrity issues are handled explicitly  

This upgrade ensures that the system is no longer just a data storage layer,  
but an intelligence-ready signal processing system.

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

Each signal is linked to its source using dataset_id.

This ensures:
- no confusion between datasets  
- full traceability of every record  

---

### 2. Deterministic Normalization

All transformations are clearly defined and documented.

Example (AIS speed conversion):

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

Each signal is marked as valid (truth_flag = TRUE) only if:
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

Water Dataset Handling:

The water dataset was completely excluded from ingestion because all records were missing latitude and longitude.

This decision was made to maintain strict geospatial integrity,  
as signals without coordinates cannot be used in spatial analysis.

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
- dataset_registry → maintains dataset metadata and lineage  
- ingestion_log → tracks ingestion runs  

Geospatial data is stored using POINT geometry, enabling efficient spatial queries.

---

## Ingestion Pipeline

The pipeline performs the following steps:

1. Load datasets  
2. Assign dataset_id  
3. Apply normalization rules  
4. Validate records  
5. Assign confidence scores  
6. Apply truth validation  
7. Remove duplicate records  
8. Insert data in batches  
9. Log ingestion results  

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

This system is built on a simple principle:

Do not assume anything about the data unless it is explicitly defined.

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
- deterministic outputs  

These signals are ready to be used for:
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
