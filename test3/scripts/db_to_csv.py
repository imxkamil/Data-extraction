import sqlite3
import csv
import os

def db_to_csv(db_file, csv_file, table_name):
    """Converts a specified table from an SQLite database to a CSV file."""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Execute a query to select all data from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Fetch all rows from the executed query
        rows = cursor.fetchall()

        # Get column names from the cursor
        column_names = [description[0] for description in cursor.description]
        
        # Write to CSV file
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)          # Write data

        print(f"Data from table '{table_name}' has been successfully written to '{csv_file}'.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except FileNotFoundError:
        print(f"The database file at {db_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()

# Define the file paths and table name
date = "27092024"
db_file_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\db\{date}.db"
csv_file_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\db\{date}.csv"  # Change to your desired output path
table_name = "CombinedData"  # Replace with the actual table name from your database

# Call the function to convert the database to CSV
db_to_csv(db_file_path, csv_file_path, table_name)
