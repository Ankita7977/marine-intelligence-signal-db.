This document describes the different signals stored in the
Marine Intelligence Signal Database.

Signals are collected from multiple datasets such as AIS vessel data,
weather data, and hydrology data. These datasets are converted into a
common schema and stored in the marine_signals table.

## Common Signal Schema

All signals follow a standardized schema with the following fields:

- source_id
- timestamp
- latitude
- longitude
- feature_type
- normalized_value
- source_reference

## Vessel Signals

Vessel signals come from AIS datasets.

These signals represent information about ship movement.

Feature Type:
vessel_speed

Description:
This signal shows the speed of a vessel at a specific location and time.

## Weather Signals

Weather signals come from weather datasets.

Feature Type:
precipitation

Description:
This signal represents rainfall measurements at a specific location and time.

## Hydrology Signals

Hydrology signals come from water monitoring datasets.

Feature Type:
water_level

Description:
This signal represents the water level measured in rivers or water bodies.

## Summary

The Marine Intelligence Signal Database stores signals from multiple
data sources using a unified schema.

Currently the database contains the following signal types:

- vessel_speed
- precipitation
- water_level

This unified structure allows spatial and temporal analysis of marine
and environmental signals.
