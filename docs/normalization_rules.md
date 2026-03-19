# NORMALIZATION RULES

## AIS
- Raw Column: normalized_value
- Unit: knots → m/s
- Formula: value * 0.514

## Weather
- Raw Column: normalized_value
- Unit: assumed Celsius
- Transformation: none

## Water
- Issue: Missing latitude & longitude
- Action: dataset removed
- Reason: no geospatial validity
