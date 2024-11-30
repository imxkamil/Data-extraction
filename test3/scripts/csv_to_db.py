import sqlite3
import csv

# Path to your CSV file
date = "30092024"

csv_file_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-updated.csv"

# Path where the .db file will be saved
db_file_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-updated.db"

# Connect to the SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Create a table named 'monitor_data' with the appropriate columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS monitor_data (
    MonitorID INTEGER PRIMARY KEY,
    FullName TEXT,
    PageNum INTEGER,
    PESEL TEXT,
    NIP TEXT,
    REGON TEXT,
    KRS TEXT
)
''')

# Open the CSV file and read its contents
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Insert each row from the CSV file into the 'monitor_data' table
    for row in reader:
        cursor.execute('''
        INSERT INTO monitor_data (MonitorID, FullName, PageNum, PESEL, NIP, REGON, KRS)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(row['MonitorID']),
            row['FullName'],
            int(row['PageNum']),
            row['PESEL'],
            row['NIP'],
            row['REGON'],
            row['KRS']
        ))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print(f"CSV data has been transferred to {db_file_path}")
