import os
import sqlite3
import pandas as pd

# Create a table (if not exists)
def create_table():
    # Connect to SQLite database (creates if it doesn't exist)
    try:
        conn = sqlite3.connect('airData.db')
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS currentData")
        conn.commit()
        cursor.execute('''
           CREATE TABLE currentData (
               SiteName TEXT,
               County	TEXT,
               AQI	samllint,
               pollutant TEXT,
               status TEXT,
               so2	decimal(3,1),
               co decimal(4,2),
               o3 decimal(4,1),
               o3_8hr decimal(4,1),
               pm10 smallint,
               pm2_5 smallint,
               no2 dicimal(4,1),
               nox decimaml(4,1),
               no decimal(4,1),
               wind_speed decimal(4,1),
               wind_direc smallint,
               publishtime timestamp,
               co_8hr decimal(4,1),
               pm2_5_avg decimal(4,1),
               pm10_avg smallint,
               so2_avg	smallint,
               longitude decimal(12,8),
               latitude decimal(12,8),
               siteId smallint,
               PRIMARY KEY (SiteName, siteId)
           )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.close()

# Function to insert data from CSV to the table
def addCurrentData():
    file_path = "./tmp/current.csv"
    # Connect to SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect('airData.db')
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    try:
        data = pd.read_csv(file_path, encoding='utf8', skiprows=2)
        data_columns = data.columns.tolist()
        data_values = data.values.tolist()
        
        for row in data_values:
            try:
                cursor.execute('''
                    INSERT INTO currentData 
                    (SiteName, County, AQI, pollutant, status, so2, co, o3, o3_8hr, pm10, pm2_5, no2, nox, no, wind_speed, wind_direc, publishtime, co_8hr, pm2_5_avg, pm10_avg, so2_avg, longitude, latitude, siteId)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', row)
                conn.commit()
            except sqlite3.IntegrityError:
                continue
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    conn.close()

def updateCurrent():
    # Create table and insert data from all CSV files in the directory
    create_table()
    addCurrentData()

if __name__ == "__main__":
    updateCurrent()