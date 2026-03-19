import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import yaml

# -----------------------------------
# STEP 1 — Load Config
# -----------------------------------
with open("../config/config.yaml") as file:
    config = yaml.safe_load(file)

db = config["database"]

engine = create_engine(
    f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"
)

print("[INFO] Connected to database")

# -----------------------------------
# STEP 2 — Load Data
# -----------------------------------
ais = pd.read_csv(config["paths"]["ais_csv"])
weather = pd.read_csv(config["paths"]["weather_csv"])
water = pd.read_csv(config["paths"]["water_csv"])

print(f"[INFO] AIS rows: {len(ais)}")
print(f"[INFO] Weather rows: {len(weather)}")
print(f"[INFO] Water rows: {len(water)}")

# -----------------------------------
# STEP 3 — DATASET LINEAGE
# -----------------------------------
ais['dataset_id'] = 1
weather['dataset_id'] = 2
water['dataset_id'] = 3

# -----------------------------------
# STEP 4 — GEOSPATIAL CLEANING (WATER)
# -----------------------------------
water_before = len(water)
water = water.dropna(subset=['latitude', 'longitude'])
water_after = len(water)

print(f"[WARNING] Removed {water_before - water_after} invalid water rows")

if water.empty:
    print("[CRITICAL] Water dataset removed due to missing geospatial data")

# -----------------------------------
# STEP 5 — SELECT REQUIRED COLUMNS
# -----------------------------------
columns = [
    "dataset_id",
    "timestamp",
    "latitude",
    "longitude",
    "feature_type",
    "normalized_value"
]

ais = ais[columns]
weather = weather[columns]
water = water[columns]

# -----------------------------------
# STEP 6 — MERGE DATA
# -----------------------------------
df = pd.concat([ais, weather, water], ignore_index=True)
print(f"[INFO] Total rows after merge: {len(df)}")

# -----------------------------------
# STEP 7 — TIMESTAMP FIX
# -----------------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -----------------------------------
# STEP 8 — VALIDATION
# -----------------------------------
valid_df = df[
    (df["latitude"].between(-90, 90)) &
    (df["longitude"].between(-180, 180)) &
    (df["timestamp"].notnull()) &
    (df["normalized_value"].notnull())
]

rejected_df = df.drop(valid_df.index)

print(f"[WARNING] Rejected rows: {len(rejected_df)}")

rejected_df.to_csv(
    "../rejected_records/rejected_records.csv",
    index=False
)

# -----------------------------------
# STEP 9 — CONFIDENCE ENGINE (RULE-BASED)
# -----------------------------------
def assign_confidence(df):
    df['confidence_score'] = 0.5  # base

    # dataset reliability adjustment
    df.loc[df['dataset_id'] == 1, 'confidence_score'] += 0.3
    df.loc[df['dataset_id'] == 2, 'confidence_score'] += 0.2
    df.loc[df['dataset_id'] == 3, 'confidence_score'] += 0.1

    # penalty for missing geo
    df.loc[
        df['latitude'].isna() | df['longitude'].isna(),
        'confidence_score'
    ] -= 0.5

    return df


def assign_truth(df):
    df['truth_flag'] = True

    df.loc[df['normalized_value'].isna(), 'truth_flag'] = False
    df.loc[df['confidence_score'] <= 0.0, 'truth_flag'] = False

    return df


valid_df = assign_confidence(valid_df)
valid_df = assign_truth(valid_df)

print("[INFO] Confidence and truth assigned")

# -----------------------------------
# STEP 10 — DEDUPLICATION
# -----------------------------------
before = len(valid_df)

valid_df = valid_df.drop_duplicates(
    subset=['timestamp', 'latitude', 'longitude', 'feature_type']
)

after = len(valid_df)

print(f"[INFO] Removed {before - after} duplicate rows")

# -----------------------------------
# STEP 11 — ADD UNIT COLUMN
# -----------------------------------
valid_df['unit'] = 'unknown'

# -----------------------------------
# STEP 12 — FINAL COLUMNS
# -----------------------------------
valid_df = valid_df[[
    'dataset_id',
    'timestamp',
    'latitude',
    'longitude',
    'feature_type',
    'normalized_value',
    'unit',
    'confidence_score',
    'truth_flag'
]]

# -----------------------------------
# STEP 13 — BATCH INSERT
# -----------------------------------
print("[INFO] Starting batch insert...")

start_time = datetime.now()

batch_size = 5000

for i in range(0, len(valid_df), batch_size):
    batch = valid_df.iloc[i:i+batch_size]

    batch.to_sql(
        "marine_signals",
        engine,
        if_exists="append",
        index=False
    )

    print(f"[INFO] Inserted rows {i} to {i + len(batch)}")

end_time = datetime.now()

# -----------------------------------
# STEP 14 — LOGGING
# -----------------------------------
log_df = pd.DataFrame([{
    "dataset_id": None,
    "records_ingested": len(valid_df),
    "records_rejected": len(rejected_df),
    "start_time": start_time,
    "end_time": end_time,
    "status": "SUCCESS",
    "notes": "Multi-dataset ingestion with validation and confidence scoring"
}])

log_df.to_sql(
    "ingestion_log",
    engine,
    if_exists="append",
    index=False
)

print("[SUCCESS] Pipeline completed successfully!")
