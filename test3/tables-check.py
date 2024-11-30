import sqlite3

def print_db_table_names(db_file):
    """Prints the names of all tables in the specified SQLite database."""
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Execute a query to retrieve the names of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
        # Fetch all rows from the executed query
        tables = cursor.fetchall()
        
        # Print table names
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(table[0])  # Each table name is in the first element of the tuple
        else:
            print("No tables found in the database.")

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

# Define the path to the database file
db_file_path = r"C:\Users\pdf\Desktop\monitor\test3\data\db\20092024.db"

# Call the function to print table names
print_db_table_names(db_file_path)
