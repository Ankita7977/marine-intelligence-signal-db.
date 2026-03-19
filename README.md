# Marine Intelligence Signal System

## Overview

The Marine Intelligence Signal System transforms heterogeneous maritime and environmental datasets into a **deterministic, traceable, and intelligence-ready signal layer**.

The system focuses on **data correctness, transparency, and reproducibility**, ensuring that all signals can be trusted for downstream analysis and simulation.

---

## Signal Intelligence Layer (Task 3)

This system upgrades a basic data pipeline into an **intelligence-ready signal processing system**.

### Key Capabilities

* **Dataset Lineage**

  * Each signal is linked to its source using `dataset_id`
  * Eliminates ambiguity from unified pipelines

* **Deterministic Normalization**

  * All transformations use explicit, documented formulas
  * No assumptions or inferred values are introduced

* **Confidence Scoring**

  * Confidence is assigned using rule-based logic:

    * Base confidence = 0.5
    * Dataset reliability adjustments:
      * AIS → +0.3 (high reliability tracking data)
      * Weather → +0.2 (moderate reliability)
      * Water → +0.1 (lower reliability due to data gaps)

  * Data quality penalties:
    * Missing latitude/longitude → -0.5

  * Final confidence is computed deterministically:
    → confidence = base + adjustments - penalties

* **Truth Validation**

  * Signals are marked valid (`truth_flag = TRUE`) only if:
    * `normalized_value` is present
    * confidence score is greater than zero

  * Invalid signals are explicitly rejected

* **Geospatial Integrity Handling**

  * Records with missing latitude/longitude are explicitly removed during preprocessing
  * All removals are logged and documented (no silent drops)

* **Deduplication**

  * Duplicate signals are removed based on:
    * timestamp
    * latitude
    * longitude
    * feature_type

* **Batch Processing**

  * Data is inserted in batches for scalability and reliability

---

## System Architecture

The system uses **PostgreSQL** for structured signal storage.

### Core Tables

* `marine_signals`  
  Stores validated, normalized, and intelligence-ready signals

* `dataset_registry`  
  Maintains dataset-level metadata and lineage

* `ingestion_log`  
  Tracks ingestion runs, rejected records, and system status

Indexes are applied on key fields such as timestamp and feature type to support scaling.

---

## Ingestion Pipeline

The ingestion pipeline performs the following steps:

1. Load datasets
2. Assign dataset-level lineage (`dataset_id`)
3. Validate records (timestamp, coordinates, values)
4. Apply confidence scoring logic
5. Apply truth validation rules
6. Remove duplicate signals
7. Insert data using batch processing
8. Log ingestion results

---

## Validation Rules

Strict validation rules are applied before ingestion:

* Latitude must be between **-90 and 90**
* Longitude must be between **-180 and 180**
* Timestamp must be valid and non-null
* `normalized_value` must not be null

Invalid records are explicitly rejected and stored separately.

---

## Repository Structure

```
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
│   └── llm_reasoning.md
│
├── ingestion_pipeline/
│   └── ingest_signals.py
│
├── data/
│   └── dataset_registry.csv
│
└── README.md
```

---

## System Design Principles

This system is built with a strong emphasis on **data integrity and transparency**:

* No assumptions are made where data is ambiguous
* No missing values are artificially filled
* All transformations are explicitly documented
* All signals remain traceable to their source
* Invalid data is never silently ignored

---

## Outcome

The system produces:

* **Traceable signals** — every record linked to a dataset
* **Validated signals** — incorrect data is filtered out
* **Deterministic outputs** — no randomness or hidden logic
* **Simulation-ready data** — usable for downstream systems

---

## Technologies Used

* PostgreSQL
* Python
* Pandas
