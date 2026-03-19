# CONFIDENCE RULES

## Dataset-based confidence

AIS → 0.9  
Weather → 0.6  
Water → 0.3  

## Missing geospatial data

If latitude/longitude missing:
→ confidence = 0.0

## Truth rules

If normalized_value is NULL:
→ truth_flag = FALSE

Else:
→ truth_flag = TRUE
