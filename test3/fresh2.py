import csv
from PyPDF2 import PdfReader
import re
import time
import pandas as pd
import os


def extract_pages(pdf_file, p2c_path, page_number):
    """
    Extracts text from a specific page of the PDF and the following page, and writes it to a text file.
    """
    # Initialize PDF reader
    reader = PdfReader(pdf_file)

    with open(p2c_path, mode='w', encoding='utf-8') as file:
        for i in range(page_number, page_number + 2):
            try:
                page_text = reader.pages[i].extract_text()
                file.write(page_text + "\n")  # Write text instead of writing to CSV
                # print(f"Page {i + 1} text written to {p2c_path}.")
            except IndexError:
                print(f"Page {i + 1} does not exist in the PDF.")

def get_paragraph(input_file_path, output_file_path, poz_num):
    """Extracts content between 'Poz. poz_num' and 'Poz. poz_num + 1' from the input file."""
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Create regex patterns to find "Poz. poz_num" and "Poz. poz_num + 1"
    start_pattern = rf"Poz\. {poz_num}"
    end_pattern = rf"Poz\. {poz_num + 1}"

    # Use regex to find the content between the specified patterns
    pattern = rf"{start_pattern}(.*?){end_pattern}"

    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        modified_content = match.group(0)  # Get the full match including start and end patterns

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        # print("Content modified successfully and saved to:", output_file_path)
    else:
        print(f"Content between '{start_pattern}' and '{end_pattern}' not found.")

def extract_identifiers(file_path):
    """Extracts numbers following 'KRS', 'PESEL', 'NIP', and 'REGON'."""
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()

        # Define the regex pattern to match 'KRS', 'PESEL', 'NIP', or 'REGON'
        pattern = r"(KRS|PESEL|NIP|REGON)\s*(\d+)"

        # Find all matches in the input text
        matches = re.findall(pattern, input_text)

        # Initialize result dictionary with None for all values
        identifiers = {'KRS': None, 'PESEL': None, 'NIP': None, 'REGON': None}

        # Loop through matches and assign the first found occurrence for each identifier
        for identifier, number in matches:
            if identifier in identifiers and identifiers[identifier] is None:
                identifiers[identifier] = number

        # Print found identifiers (for debugging)
        for key, value in identifiers.items():
            print(f"Found {key}: {value}")

        return identifiers
    
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return {'KRS': None, 'PESEL': None, 'NIP': None, 'REGON': None}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'KRS': None, 'PESEL': None, 'NIP': None, 'REGON': None}

# Path to CSV file
csv_file_path = r'C:\Users\pdf\Desktop\monitor\test3\data\db\20092024-test.csv'
pdf_path = r"C:\Users\pdf\Desktop\monitor\test3\data\raw\20092024.pdf"  # PDF path

# Read the CSV and process each row
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Check if output file exists, if not, create it and add headers
    output_csv_file = r'C:\Users\pdf\Desktop\monitor\test3\data\db\20092024-updated.csv'
    file_exists = os.path.exists(output_csv_file)

    # Open the output CSV file in append mode
    with open(output_csv_file, mode='a', newline='', encoding='utf-8') as outfile:
        fieldnames = reader.fieldnames + ['PESEL', 'NIP', 'REGON', 'KRS']  # Original + new headers
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write the header if the file doesn't exist (first time writing)
        if not file_exists:
            writer.writeheader()

        # Loop through each row in the original CSV file
        for row in reader:
            MonitorID = row['MonitorID']
            PageNum = row['PageNum']

            print(f"Processing: MonitorID: {MonitorID}, PageNum: {PageNum}")

            # Define paths for temp files
            pages_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_page_{PageNum}.csv"
            paragraph_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_paragraph_{MonitorID}.txt"

            # Correct the PageNum for 0-based index and convert MonitorID
            PageNum_Corrected = int(PageNum) - 1
            MonitorID_Corrected = int(MonitorID)

            # Step 1: Extract pages from the PDF based on PageNum_Corrected
            extract_pages(pdf_path, pages_path, PageNum_Corrected)
            time.sleep(1)

            # Step 2: Extract paragraph from the page based on MonitorID
            get_paragraph(pages_path, paragraph_path, MonitorID_Corrected)
            time.sleep(1)

            # Step 3: Extract identifiers (KRS, PESEL, NIP, REGON) from the paragraph
            identifiers = extract_identifiers(paragraph_path)

            # Step 4: Update the row with identifiers
            row.update({
                'PESEL': identifiers['PESEL'],
                'NIP': identifiers['NIP'],
                'REGON': identifiers['REGON'],
                'KRS': identifiers['KRS']
            })

            # Step 5: Write the updated row to the output CSV file
            writer.writerow(row)

            print(f"Completed processing for MonitorID: {MonitorID}, PageNum: {PageNum}\n")


# fff