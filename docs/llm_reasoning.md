# LLM Reasoning

## Deterministic Normalization
All transformations are based on fixed formulas.
No random or inferred values are used.

## Confidence Assignment
Confidence is assigned based on dataset type:
- AIS → High (0.9)
- Weather → Medium (0.6)
- Water → Low (0.3)

Missing geospatial data results in zero confidence.

## Hallucination Prevention
No missing values were filled artificially.
Water dataset removed due to missing coordinates.
All ambiguity is preserved and documented.
