# CONFIDENCE RULES

## 1. Base Confidence

All signals start with a base confidence score:

→ base = 0.5


## 2. Dataset Reliability Adjustment

Confidence is adjusted based on dataset characteristics:

- AIS (satellite vessel tracking)
  → +0.3 (high reliability due to real-time tracking)

- Weather (meteorological observations)
  → +0.2 (moderate reliability, sensor-based)

- Water (hydrology dataset)
  → +0.1 (lower reliability due to missing geospatial coverage)


## 3. Data Quality Penalty

If critical fields are missing:

- Missing latitude OR longitude
  → -0.5 penalty

- Missing normalized_value
  → signal considered invalid


## 4. Final Confidence Score

final_confidence = base + dataset_adjustment - penalties


## 5. Truth Rules

A signal is considered truthful only if:

- normalized_value is NOT NULL
- timestamp is valid

If any of the above fail:

→ truth_flag = FALSE

Else:

→ truth_flag = TRUE


## 6. Key Principle

- No hardcoded confidence values
- Confidence is derived from:
  → data source reliability
  → data completeness
  → validation checks
