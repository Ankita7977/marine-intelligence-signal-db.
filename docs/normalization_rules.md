# NORMALIZATION RULES

## 1. AIS Dataset

- Feature: Ship Speed
- Raw Column: speed_knots
- Normalized Column: normalized_value
- Raw Unit: Knots
- Normalized Unit: m/s

- Transformation:
  normalized_value = speed_knots * 0.514444

- Reason:
  Standardizing speed into SI unit (meters per second) for consistency


## 2. Weather Dataset

- Feature: Environmental measurement (temperature / precipitation)
- Raw Column: dataset-specific field (e.g., temperature_c or precipitation_mm)
- Normalized Column: normalized_value

- Unit Handling:
  Unit is NOT explicitly defined in dataset

- Transformation:
  No transformation applied

- Reason:
  - No unit metadata available
  - To avoid assumptions, values are preserved as-is
  - Marked as "unit unknown" in system


## 3. Water Dataset

- Total Records: 312

- Issue:
  All records have missing latitude and longitude

- Action:
  Dataset excluded from ingestion

- Reason:
  - Geospatial coordinates are mandatory
  - Without them, signals cannot be used
  - Including this dataset would introduce invalid signals

- Handling:
  - Records explicitly removed during preprocessing
  - Removal logged in pipeline (not silently dropped)


## 4. Key Principles

- No assumptions made where data is ambiguous
- All transformations are explicitly defined
- Raw values preserved for traceability
- Each signal is linked to its source via dataset_id
- Invalid data is excluded with documented reasoning
