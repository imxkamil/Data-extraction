import csv
import re
from PyPDF2 import PdfReader
import sqlite3
import time




# date = "20092024"
date = "30092024"
core_path = r'C:\Users\monitoring2\Desktop\ei\monitor\foo\data'
# ttt_file = r"\raw\30092024.pdf"





pdf_path = fr"{core_path}\raw\{date}.pdf"
p2c_path = fr"{core_path}\raw\{date}_raw.csv"
f1_path = fr'{core_path}\temp\{date}_format1_III_IX.csv'
f21_path = fr'{core_path}\temp\{date}_format2_III_IV.csv'
f22_path = fr'{core_path}\temp\{date}_format2_IX.csv'
filter_path1 = fr'{core_path}\temp\{date}_format2_final_III_IV.csv'
filter_path2 = fr'{core_path}\temp\{date}_format2_final_IX.csv'
processed_path1 = fr'{core_path}\processed\{date}_format2_processed_III_IV.csv'
processed_path2 =fr'{core_path}\processed\{date}_format2_processed_IX.csv'
db_file1 = fr'{core_path}\temp\{date}_format2_processed_III_IV.db'
db_file2 = fr'{core_path}\temp\{date}_format2_processed_IX.db'
output_db = fr'{core_path}\db\{date}.db'






def pdf_to_csv(pdf_file, csv_file):
    # Initialize PDF reader
    reader = PdfReader(pdf_file)

    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Extract text from the first 10 pages
        for i in range(10):
            try:
                page_text = reader.pages[i].extract_text()
                writer.writerow([page_text])  # Writing each page's text to a new row
            except IndexError:
                # If the PDF has fewer than 10 pages, stop
                print(f"Page {i+1} does not exist.")
                break

def format1(input_file_path, output_file_path):

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    start_index = content.find("OGŁOSZENIA WYMAGANE PRZEZ PRAWO UPADŁOŚCIOWE")
    end_index = content.find("OGŁOSZENIA WYMAGANE PRZEZ USTAWĘ O RACHUNKOWOŚCI")

    if start_index != -1:
        if end_index != -1:
            modified_content = content[start_index:end_index + len("OGŁOSZENIA WYMAGANE PRZEZ USTAWĘ O RACHUNKOWOŚCI")]
        else:
            modified_content = content[start_index:]
        
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print("Content modified successfully and saved to:", output_file_path)
    else:
        print("Starting phrase not found.")

def format21(input_file_path, output_file_path):

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    end_index = content.find("OSTĘPOWANIA CYWILNEGO")

    if end_index != -1:
        modified_content = content[:end_index + len("OSTĘPOWANIA CYWILNEGO")]
        
        with open(output_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(modified_content)
        print("New file created successfully.")
    else:
        print("Ending phrase not found.")

def format22(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    start_index = content.find("OGŁOSZENIA WYMAGANE PRZEZ PRAWO RESTRUKTURYZACYJNE")

    if start_index != -1:
        modified_content = content[start_index:]
        
        with open(output_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(modified_content)
        print("New file created successfully.")
    else:
        print("Phrase not found.")

def processing(input_file_path, output_file_path):

    # Open the input CSV file and read it
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Prepare a list to store the processed data
    processed_data = []

    # Loop through each line and extract MonitorID, FullName, and PageNum
    for line in lines:
        # Use a regular expression to match the required components
        match = re.match(r'(\d{5})\s+(.*?)(\s*\d{2})?\s*$', line.strip())
        if match:
            monitor_id = match.group(1)  # First five digits as MonitorID
            full_name = match.group(2).strip()  # Everything in between as FullName
            
            # Check if there is a page number; if not, set it to '0'
            if match.group(3):
                page_num = match.group(3).strip()[-2:]  # Last two digits as PageNum
            else:
                page_num = '0'  # Default to '0' if no page number is present
            
            # Add the processed data to the list
            processed_data.append([monitor_id, full_name, page_num])

    # Write the processed data to a new CSV file
    with open(output_file_path, 'w', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write the header row
        csvwriter.writerow(['MonitorID', 'FullName', 'PageNum'])
        
        # Write the processed rows
        csvwriter.writerows(processed_data)

    print(f"File {input_file_path} processed and saved as {output_file_path}.")

def csv_to_db(csv_file, db_file):

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table with specified columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            MonitorID INTEGER,
            FullName TEXT,
            PageNum INTEGER
        )
    ''')

    # Open and read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Skip header row
        next(reader)
        
        # Insert data into the SQLite table
        for row in reader:
            # Insert into the database (ensuring the correct data types)
            cursor.execute('''
                INSERT INTO records (MonitorID, FullName, PageNum)
                VALUES (?, ?, ?)
            ''', (int(row[0]), row[1], int(row[2])))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Data successfully written to {db_file}")

def join_tables(db_file1, db_file2, output_db):
    """
    Joins two tables with the same structure (MonitorID, FullName, PageNum) from different databases
    and stores them in an output database.

    Parameters:
        db_file1 (str): Path to the first database file.
        db_file2 (str): Path to the second database file.
        output_db (str): Path to the output database file where the combined table will be stored.
    """
    
    # Connect to the first database
    conn1 = sqlite3.connect(db_file1)
    cursor1 = conn1.cursor()
    
    # Connect to the second database
    conn2 = sqlite3.connect(db_file2)
    cursor2 = conn2.cursor()

    # Connect to the output database (create it if it doesn't exist)
    conn_output = sqlite3.connect(output_db)
    cursor_output = conn_output.cursor()

    # List the tables in both databases (just for checking)
    cursor1.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables1 = cursor1.fetchall()
    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables2 = cursor2.fetchall()
    print(f"Tables in {db_file1}: {tables1}")
    print(f"Tables in {db_file2}: {tables2}")

    # Assuming the table name is the same in both databases, you need to replace 'your_table_name' with the actual table name
    table_name1 = tables1[0][0]  # Assuming there's only one table
    table_name2 = tables2[0][0]  # Assuming there's only one table

    # Create a new table in the output database (if it doesn't already exist)
    cursor_output.execute("""
    CREATE TABLE IF NOT EXISTS CombinedData (
        MonitorID INTEGER,
        FullName TEXT,
        PageNum INTEGER
    )
    """)

    # Copy all rows from the first table
    cursor1.execute(f"SELECT MonitorID, FullName, PageNum FROM {table_name1}")
    rows1 = cursor1.fetchall()
    cursor_output.executemany("INSERT INTO CombinedData (MonitorID, FullName, PageNum) VALUES (?, ?, ?)", rows1)
    print(f"Inserted {len(rows1)} rows from {table_name1} into the output database.")

    # Copy all rows from the second table
    cursor2.execute(f"SELECT MonitorID, FullName, PageNum FROM {table_name2}")
    rows2 = cursor2.fetchall()
    cursor_output.executemany("INSERT INTO CombinedData (MonitorID, FullName, PageNum) VALUES (?, ?, ?)", rows2)
    print(f"Inserted {len(rows2)} rows from {table_name2} into the output database.")

    # Commit changes to the output database
    conn_output.commit()

    # Close all connections
    conn1.close()
    conn2.close()
    conn_output.close()

    print(f"Tables from {db_file1} and {db_file2} successfully joined into {output_db}.")




def filter1(input_file_path, output_file_path):
    """Removes special symbols like '.', '„', '”', and '"'."""
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = content.replace('.', '').replace('„', '').replace('”', '').replace('"', '')

    with open(output_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(content)

    print(f"Filter 1 applied: {output_file_path} has no special symbols.")

def filter2(input_file_path, output_file_path):
    """Adds a new line before every 'Poz 12345' pattern."""
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r'(?<=\S)(Poz \d{5})'

    modified_content = re.sub(pattern, r'\n\1', content)

    with open(output_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(modified_content)

    print(f"Filter 2 applied: {output_file_path} has a new line before every 'Poz 12345' pattern.")

def filter222(input_file, output_file):
    """Filters lines that start with 'Poz' followed by 5 digits or end with 1-2 digits."""
    pattern = re.compile(r'^Poz \d{5}|.*\d{1,2}$')

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            line = line.strip()
            if pattern.match(line):
                outfile.write(line + '\n')

    print(f"Filter 222 applied: Filtered lines written to {output_file}.")

def filter223(input_file, output_file):
    """Combines lines where the first line doesn't end with a digit."""
    pattern_end_with_digits = re.compile(r'.*\d{1,2}$')
    combined_lines = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        previous_line = ''
        
        for line in infile:
            line = line.strip()

            if pattern_end_with_digits.match(line):
                if previous_line:
                    combined_lines.append(previous_line + ' ' + line)
                    previous_line = ''
                else:
                    combined_lines.append(line)
            else:
                if previous_line:
                    previous_line += ' ' + line
                else:
                    previous_line = line

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for combined_line in combined_lines:
            outfile.write(combined_line + '\n')

    print(f"Filter 223 applied: Processed lines written to {output_file}.")

def filter3(input_file_path, output_file_path):
    """Removes the string 'Poz' only when it appears at the beginning of a line."""
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Use regular expressions to replace 'Poz' at the beginning of each line
    content = re.sub(r'^Poz', '', content, flags=re.MULTILINE)

    with open(output_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(content)

    print(f"Filter 3 applied: {output_file_path} has 'Poz' removed only at the start of lines.")

def apply_all_filters(input_file, output_file):
    """Applies all filters in sequence, outputting to a final file."""
    # Intermediate file paths
    intermediate_file1 = output_file.replace('final', 'filter1')
    intermediate_file2 = output_file.replace('final', 'filter2')
    intermediate_file3 = output_file.replace('final', 'filter3')
    intermediate_file4 = output_file.replace('final', 'filter4')

    # Apply filters sequentially
    filter1(input_file, intermediate_file1)
    filter2(intermediate_file1, intermediate_file2)
    filter222(intermediate_file2, intermediate_file3)
    filter223(intermediate_file3, intermediate_file4)
    filter3(intermediate_file4, output_file)  # Final output

    print(f"All filters applied. Final output saved to {output_file}.")


# Iniciate running functions in the right order
def pdf2db(pdf_path):
    start_time = time.time()
    pdf_to_csv(pdf_path, p2c_path)
    print("pdf_to_csv done")
    time.sleep(3)
    format1(p2c_path, f1_path)
    print("format1 done")
    time.sleep(3)
    format21(f1_path, f21_path)
    print("format21 done")
    time.sleep(3)
    format22(f1_path, f22_path)
    print("format22 done")
    time.sleep(3)
    apply_all_filters(f21_path, filter_path1)
    print("filter for first file done")
    time.sleep(3)
    apply_all_filters(f22_path, filter_path2)
    print("filter for second file done")
    time.sleep(3)
    processing(filter_path1, processed_path1)
    print("processing for first file done")
    time.sleep(3)
    processing(filter_path2, processed_path2)
    print("processing for second file done")
    time.sleep(3)
    csv_to_db(processed_path1, db_file1)
    print("csv_to_db for first file done")
    time.sleep(3)
    csv_to_db(processed_path2, db_file2)
    print("csv_to_db for secoind file done")
    time.sleep(3)
    join_tables(db_file1, db_file2, output_db)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("joining files done")
    print(f"everything done in: {elapsed_time:.2f} seconds")

# Runs all the previous functions
pdf2db(pdf_path)







