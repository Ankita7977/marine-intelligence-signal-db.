import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine
from datetime import datetime

ais = pd.read_csv("data/ais_standardized.csv")
weather = pd.read_csv("data/weather_standardized.csv")
water = pd.read_csv("data/water_standardized.csv")

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

final_pipeline_data = pd.concat(
    [ais, weather, water],
    ignore_index=True
)

final_pipeline_data["timestamp"] = pd.to_datetime(
    final_pipeline_data["timestamp"],
    errors="coerce"
)

valid_df = final_pipeline_data[
(final_pipeline_data["latitude"].between(-90,90)) &
(final_pipeline_data["longitude"].between(-180,180)) &
(final_pipeline_data["normalized_value"].notnull())
]

rejected_df = final_pipeline_data.drop(valid_df.index)

rejected_df.to_csv("rejected_records.csv", index=False)

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

gdf["truth_level"] = 0
gdf["confidence_score"] = 0.8

engine = create_engine(
"postgresql://postgres:admin%40123@localhost:5432/marine_intelligence"
)

start_time = datetime.now()

gdf.to_sql(
"marine_signals",
engine,
if_exists="append",
index=False
)

end_time = datetime.now()

log_df = pd.DataFrame([{
"dataset_id":"UNIFIED_PIPELINE",
"records_ingested":len(valid_df),
"records_rejected":len(rejected_df),
"start_time":start_time,
"end_time":end_time,
"status":"SUCCESS",
"notes":"Unified AIS + Water + Weather ingestion"
}])

log_df.to_sql(
"ingestion_log",
engine,
if_exists="append",
index=False
)
