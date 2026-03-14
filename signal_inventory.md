# Marine Intelligence Signal Inventory

This document describes the different signals stored in the
Marine Intelligence Signal Database.

Signals are collected from multiple datasets such as AIS vessel data,
weather data, and hydrology data. These datasets are normalized into
a common schema and stored in the marine_signals table.

## Common Signal Schema

All signals follow a standardized schema with the following fields:

- source_id
- timestamp
- latitude
- longitude
- feature_type
- normalized_value
- source_reference

This schema ensures that signals from different datasets can be
stored and analyzed in a consistent format.

## Vessel Signals

Vessel signals originate from AIS (Automatic Identification System)
datasets.

Feature Type:
vessel_speed

Description:
This signal represents the speed of a vessel recorded at a specific
geographic location and timestamp.

## Weather Signals

Weather signals originate from environmental weather datasets.

Feature Type:
precipitation

Description:
This signal represents rainfall measurements collected at a specific
location and time.

## Hydrology Signals

Hydrology signals originate from water monitoring datasets.

Feature Type:
water_level

Description:
This signal represents the water level measured in rivers or
water bodies.

## Signal Inventory Summary

The Marine Intelligence Signal Database currently contains signals
from the following categories:

- vessel_speed
- precipitation
- water_level

These signals are stored in the **marine_signals** table and can be
queried using spatial and temporal filters.

Example signal inventory query:

SELECT feature_type, COUNT(*)
FROM marine_signals
GROUP BY feature_type;

This query provides the number of signals stored for each signal type.

## Conclusion

The unified signal schema enables the Marine Intelligence system
to integrate multiple environmental and vessel datasets into a
single geospatial signal database.

This data forms the foundation for future analytics, visualization,
and intelligence scoring layers.
