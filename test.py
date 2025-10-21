import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# -----------------------------
# Step 1: Extract CSVs
# -----------------------------
try:
    evap_data = pd.read_csv("evapotranspiration.csv")
    soil_data = pd.read_csv("soil_moisture.csv")
    logging.info("✅ CSV files loaded successfully")
except Exception as e:
    logging.error(f"Error loading CSVs: {e}")
    raise

# -----------------------------
# Step 2: Transform / Merge
# -----------------------------
evap_data['Date'] = pd.to_datetime(evap_data['Date'], format="%d-%m-%Y")
soil_data['Date'] = pd.to_datetime(soil_data['Date'], format="%d-%m-%Y")

merged = pd.merge(evap_data, soil_data, on=["Date", "StateName", "DistrictName"], how="inner")

merged["Water_Efficiency"] = merged["Avg Soilmoisture Level (at 15cm)"] / merged["Evapo Level (mm)"].replace(0,1)
merged["Moisture_Deficit"] = merged["Evapo Level (mm)"] - merged["Avg Soilmoisture Level (at 15cm)"]

# ✅ Rename columns to match MySQL table schema
merged.rename(columns={
    "Evapo Level (mm)": "Evapotranspiration_Level",
    "Evapo Volume (Tmcft)": "Evapotranspiration_Volume",
    "Aggregate Evapo Level (mm)": "Aggregate_Evapotranspiration_Level",
    "Aggregate Evapo Volume (Tmcft)": "Aggregate_Evapotranspiration_Volume",
    "Avg Soilmoisture Level (at 15cm)": "Avg_Soilmoisture_Level",
    "Avg SoilMoisture Volume (at 15cm)": "Avg_Soilmoisture_Volume",
    "Aggregate Soilmoisture Perg (at 15cm)": "Aggregate_Soilmoisture_Percentage",
    "Volume Soilmoisture percg (at 15cm)": "Volume_Soilmoisture_Percentage"
}, inplace=True)

logging.info("✅ Data transformation complete")

# -----------------------------
# Step 3: Load into MySQL
# -----------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Welcome@123",
        database="gov_data"
    )
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS district_water_stats (
        Date DATE,
        StateName VARCHAR(50),
        DistrictName VARCHAR(50),
        Evapotranspiration_Level FLOAT,
        Evapotranspiration_Volume FLOAT,
        Aggregate_Evapotranspiration_Level FLOAT,
        Aggregate_Evapotranspiration_Volume FLOAT,
        Avg_Soilmoisture_Level FLOAT,
        Avg_Soilmoisture_Volume FLOAT,
        Aggregate_Soilmoisture_Percentage FLOAT,
        Volume_Soilmoisture_Percentage FLOAT,
        Water_Efficiency FLOAT,
        Moisture_Deficit FLOAT
    )
    """
    cursor.execute(create_table_query)
    logging.info("✅ Table created successfully or already exists")

    insert_query = """
    INSERT INTO district_water_stats(
        Date, StateName, DistrictName,
        Evapotranspiration_Level, Evapotranspiration_Volume,
        Aggregate_Evapotranspiration_Level, Aggregate_Evapotranspiration_Volume,
        Avg_Soilmoisture_Level, Avg_Soilmoisture_Volume,
        Aggregate_Soilmoisture_Percentage, Volume_Soilmoisture_Percentage,
        Water_Efficiency, Moisture_Deficit
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    data_to_insert = [tuple(row) for row in merged[[
        "Date","StateName","DistrictName",
        "Evapotranspiration_Level","Evapotranspiration_Volume",
        "Aggregate_Evapotranspiration_Level","Aggregate_Evapotranspiration_Volume",
        "Avg_Soilmoisture_Level","Avg_Soilmoisture_Volume",
        "Aggregate_Soilmoisture_Percentage","Volume_Soilmoisture_Percentage",
        "Water_Efficiency","Moisture_Deficit"
    ]].to_numpy()]

    cursor.executemany(insert_query, data_to_insert)
    conn.commit()
    logging.info(f"✅ {cursor.rowcount} rows inserted successfully")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.error("❌ Invalid username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.error("❌ Database does not exist")
    else:
        logging.error(f"❌ MySQL error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        logging.info("✅ MySQL connection closed")
