import sqlite3
import pandas as pd

# Connect to SQLite database (creates if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_table (
            SiteName TEXT,
            Date TEXT,
            TestTarget TEXT,
            Test0 INTEGER,
            Test1 INTEGER,            
            Test2 INTEGER,            
            Test3 INTEGER,            
            Test4 INTEGER,                   
            Test5 INTEGER,
            Test6 INTEGER,
            Test7 INTEGER,
            Test8 INTEGER,
            Test9 INTEGER,
            Test10 INTEGER,
            Test11 INTEGER,
            Test12 INTEGER,
            Test13 INTEGER,
            Test14 INTEGER,                   
            Test15 INTEGER,
            Test16 INTEGER,
            Test17 INTEGER,
            Test18 INTEGER,
            Test19 INTEGER,
            Test20 INTEGER,
            Test21 INTEGER,
            Test22 INTEGER,
            Test23 INTEGER,
            PRIMARY KEY (Date, TestTarget)
        )
    ''')
    conn.commit()

# Function to insert data from CSV to the table
def insert_data_from_csv():
    try:
        data = pd.read_csv('./2022/二林_2022.csv', encoding='big5')
        data_columns = data.columns.tolist()
        data_values = data.values.tolist()
        
        cursor.executemany('''
            INSERT INTO my_table 
            (SiteName, Date, TestTarget, Test0, Test1, Test2, Test3, Test4, Test5, Test6, Test7, Test8, Test9, Test10, Test11, Test12, Test13, Test14, Test15, Test16, Test17, Test18, Test19, Test20, Test21, Test22, Test23)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data_values)
        conn.commit()
    except Exception as e:
        print("Error:", e)

# Create table and insert data
create_table()
insert_data_from_csv()

# Close the connection
conn.close()

