# CONFIDENCE RULES

## 1. Base Confidence

All signals start with a base confidence score: 

→ base = 0.5


## 2. Dataset Reliability Adjustment

Confidence is adjusted based on dataset characteristics:

- AIS (satellite vessel tracking)
  → +0.3 (high reliability)

- Weather (meteorological observations)
  → +0.2 (moderate reliability)

- Water dataset
  → EXCLUDED due to missing geospatial data


## 3. Dataset Mapping Logic

Dataset adjustments are applied using dataset_id:

- dataset_id = 1 (AIS) → +0.3
- dataset_id = 2 (Weather) → +0.2

Water dataset is excluded and not processed in pipeline


## 4. Data Quality Penalty

If critical fields are missing:

- Missing latitude OR longitude
  → -0.5 penalty

- Missing normalized_value
  → signal considered invalid


## 5. Final Confidence Score

final_confidence = base + dataset_adjustment - penalties


## 6. Confidence Bounds

0 ≤ confidence_score ≤ 1


## 7. Truth Rules

A signal is considered truthful only if:

- normalized_value is NOT NULL
- timestamp is valid
- confidence_score > 0

Else:

→ truth_flag = FALSE


## 8. Key Principles

- No hardcoded confidence values
- Confidence is derived from:
  → data source reliability
  → data completeness
  → validation checks
- Fully deterministic and reproducible logic
