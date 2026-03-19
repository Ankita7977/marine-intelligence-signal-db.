# NORMALIZATION RULES

## 1. AIS Dataset

- Feature: Ship Speed
- Raw Column: normalized_value (treated as raw input from source dataset)
- Raw Unit: Knots
- Normalized Unit: m/s

- Transformation:
  normalized_value = raw_value * 0.514

- Reason:
  Standardizing speed into SI unit (meters per second) for consistency


## 2. Weather Dataset

- Feature: Environmental Measurement (feature_type = 65)
- Raw Column: normalized_value (treated as raw input)

- Unit Handling:
  Unit is NOT explicitly defined in dataset

- Transformation:
  No transformation applied

- Reason:
  - No unit metadata available in dataset
  - To avoid assumption, values are preserved as-is
  - Marked as "unit unknown" in system


## 3. Water Dataset

- Total Records: 312

- Issue:
  All records have missing latitude and longitude

- Action:
  Dataset excluded from ingestion

- Reason:
  - Geospatial coordinates are mandatory for spatial intelligence
  - Without latitude/longitude, signals cannot be mapped or used
  - Including this dataset would introduce invalid signals

- Handling:
  - Records explicitly removed during preprocessing
  - Removal logged in pipeline (not silently dropped)


## 4. Key Principles

- No assumptions made where data is ambiguous
- All transformations are explicitly defined
- Raw values preserved for traceability
- Invalid data is excluded with documented reasoning
