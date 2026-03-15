import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine
from datetime import datetime
import yaml


# -----------------------------------
# STEP 1 — Load Configuration File
# -----------------------------------

with open("../config/config.yaml") as file:
    config = yaml.safe_load(file)

db = config["database"]


# -----------------------------------
# STEP 2 — Connect to PostgreSQL
# -----------------------------------

engine = create_engine(
f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"
)


# -----------------------------------
# STEP 3 — Load Standardized Datasets
# -----------------------------------

ais = pd.read_csv(config["paths"]["ais_csv"])
weather = pd.read_csv(config["paths"]["weather_csv"])
water = pd.read_csv(config["paths"]["water_csv"])

# -----------------------------------
# STEP 4 — Normalize Schema
# -----------------------------------

columns = [
"source_id",
"timestamp",
"latitude",
"longitude",
"feature_type",
"normalized_value",
"source_reference"
]

ais = ais[columns]
weather = weather[columns]
water = water[columns]


# -----------------------------------
# STEP 5 — Merge Datasets
# -----------------------------------

final_pipeline_data = pd.concat(
    [ais, weather, water],
    ignore_index=True
)


# -----------------------------------
# STEP 6 — Convert Timestamp
# -----------------------------------

final_pipeline_data["timestamp"] = pd.to_datetime(
final_pipeline_data["timestamp"],
errors="coerce"
)


# -----------------------------------
# STEP 7 — Validation Rules
# -----------------------------------

valid_df = final_pipeline_data[
(final_pipeline_data["latitude"].between(-90,90)) &
(final_pipeline_data["longitude"].between(-180,180)) &
(final_pipeline_data["timestamp"].notnull()) &
(final_pipeline_data["normalized_value"].notnull())
]

rejected_df = final_pipeline_data.drop(valid_df.index)


# -----------------------------------
# STEP 8 — Save Rejected Records
# -----------------------------------

rejected_df.to_csv(
"../rejected_records/rejected_records.csv",
index=False
)


# -----------------------------------
# STEP 9 — Create Geometry Column
# -----------------------------------

valid_df = valid_df.copy()

valid_df["geom"] = gpd.points_from_xy(
valid_df["longitude"],
valid_df["latitude"]
)

gdf = gpd.GeoDataFrame(
valid_df,
geometry="geom",
crs="EPSG:4326"
)


# -----------------------------------
# STEP 10 — Add Signal Metadata
# -----------------------------------

gdf["truth_level"] = 0
gdf["confidence_score"] = 0.8


# -----------------------------------
# STEP 11 — Register Dataset
# -----------------------------------

registry_df = pd.DataFrame([{
"dataset_id":"UNIFIED_PIPELINE",
"dataset_name":"AIS + Weather + Hydrology Signals",
"source":"Multiple Sources",
"schema_version":"1.0",
"update_frequency":"Daily",
"trust_level":"Medium",
"ingestion_method":"Python Pipeline",
"last_update_timestamp":datetime.now()
}])

registry_df.to_sql(
"dataset_registry",
engine,
if_exists="append",
index=False
)


# -----------------------------------
# STEP 12 — Insert Signals into DB
# -----------------------------------

start_time = datetime.now()

gdf.to_sql(
"marine_signals",
engine,
if_exists="append",
index=False
)

end_time = datetime.now()


# -----------------------------------
# STEP 13 — Log Ingestion
# -----------------------------------

log_df = pd.DataFrame([{
"dataset_id":"UNIFIED_PIPELINE",
"records_ingested":len(valid_df),
"records_rejected":len(rejected_df),
"start_time":start_time,
"end_time":end_time,
"status":"SUCCESS",
"notes":"Unified AIS + Weather + Hydrology ingestion"
}])

log_df.to_sql(
"ingestion_log",
engine,
if_exists="append",
index=False
)


# -----------------------------------
# STEP 14 — Pipeline Completed
# -----------------------------------

print("Pipeline completed successfully")
