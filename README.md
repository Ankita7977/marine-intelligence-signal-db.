# Marine Intelligence Signal Database

## Project Overview

The Marine Intelligence Signal Database is a spatial data fabric designed to ingest, normalize, and store heterogeneous maritime and environmental signals.

This system is built using **PostgreSQL and PostGIS** to support geospatial intelligence analysis.

The data fabric ensures that all incoming signals are:

* Structured
* Validated
* Traceable
* Geospatially indexed

The database supports ingestion of multiple datasets including:

* AIS vessel signals
* Weather signals
* Hydrology monitoring signals

These signals are stored in a unified schema to enable large-scale marine intelligence analysis.

---

## Database Architecture

The system uses **PostgreSQL with PostGIS** to store spatial signals.

Main tables implemented:

* `marine_signals` – stores normalized signal data
* `dataset_registry` – tracks registered datasets
* `ingestion_log` – records ingestion runs

A spatial index is implemented on the geometry column to support efficient geospatial queries.

---

## Signal Inventory

After ingestion, the database currently contains the following signals:

| Feature Type  | Record Count |
| ------------- | ------------ |
| vessel_speed  | 1,447,936    |
| precipitation | 312          |
| water_level   | 366          |

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
│   ├── ai_code_review.md
│   ├── ai_schema_review.md
│   └── data_authenticity.md
│
├── ingestion_pipeline/
│   └── ingest_signals.py
│
├── notebooks/
│   └── normalization.ipynb
│
├── signal_inventory.md
└── README.md
```

---

### Explanation

The Marine Intelligence Signal Database currently stores signals from multiple maritime and environmental sources.

The ingested signals include:

* **AIS vessel movement signals** represented by `vessel_speed`
* **Weather observations** represented by `precipitation`
* **Hydrology monitoring signals** represented by `water_level`

The AIS vessel dataset forms the largest portion of the database, containing over 1.4 million vessel movement records.

Environmental datasets provide additional contextual signals that can support marine intelligence analysis.

---

## Ingestion Pipeline

The ingestion pipeline performs the following steps:

1. Load raw datasets
2. Normalize dataset schema
3. Validate signal records
4. Generate spatial geometry
5. Insert records into the PostGIS database
6. Log ingestion results

The pipeline supports AIS vessel, weather, and hydrology datasets.

---

## Validation Rules

Before inserting records into the database, validation rules are applied:

* Latitude must be between **-90 and 90**
* Longitude must be between **-180 and 180**
* Timestamp must follow **ISO format**
* `normalized_value` must not be null

Invalid records are stored separately and counted in the ingestion log.

---

## AI-Assisted Engineering

AI tools were used to review the database schema and ingestion pipeline.

The AI review helped identify improvements in:

* data validation
* ingestion logging
* schema reliability
* reproducibility of the pipeline

Documentation of AI-assisted reviews is available in the `docs/` folder.

---

## Technologies Used

* PostgreSQL
* PostGIS
* Python
* Pandas
* Geospatial SQL

## Task 3 — Signal Intelligence Layer

This stage improves system trust and traceability.

### Features added:

- Dataset lineage using dataset_id
- Confidence scoring based on dataset source
- Truth validation for signal values
- Removal of invalid geospatial data

### Result:

A deterministic, auditable signal intelligence system
