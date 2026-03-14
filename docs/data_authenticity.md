This document explains how the datasets used in the Marine Intelligence
system are verified before they are stored in the database.

The purpose of this verification is to ensure that the data comes
from trusted sources and follows the correct format.

## Datasets Used

The Marine Intelligence system uses three datasets:

1. AIS Vessel dataset
2. Weather dataset
3. Water level dataset

These datasets are converted into a common schema before being stored
in the marine_signals database table.

## Source Verification

Before using any dataset, the source of the dataset is verified.

The following checks are performed:

- The dataset is downloaded from a trusted source
- The dataset format is checked
- The dataset structure is verified


 ## Schema Validation
Before ingestion, all datasets are checked to ensure they contain
the required columns.

 ## Required columns include:

- source_id
- timestamp
- latitude
- longitude
- feature_type
- normalized_value
- source_reference

  ## Data Validation

The ingestion pipeline performs several validation checks.

These include:

- Latitude must be between -90 and 90
- Longitude must be between -180 and 180
- Timestamp must be valid
- Normalized value must not be null

Records that fail validation are stored in a rejected records file.

## Dataset Registry

All datasets used in the system are registered in the dataset_registry table.

This table stores important information such as:

- dataset name
- source
- schema version
- trust level
- update frequency

This helps track where the data came from.
