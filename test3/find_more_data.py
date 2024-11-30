import csv
from PyPDF2 import PdfReader
import re
import time
import pandas as pd

# Poz. 45811. SILCON HOLDING SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ W UPADŁOŚCI we Wrocławiu 24
# 45787,Złocki Damian,17



poz_num = 45811
test_num = 24
# poz_num = 45787
# test_num = 17

pdf_path = r"C:\Users\pdf\Desktop\monitor\test3\data\raw\20092024.pdf"
p2c_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_page_{test_num}.csv"
paragraph_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_paragraph_{poz_num}.txt"

page_number = test_num - 1 # proper indexing

def tttttextract_page(pdf_file, csv_file, page_number):
    """
    Extracts text from a specific page of the PDF and writes it to a CSV file.

    :param pdf_file: Path to the input PDF file.
    :param csv_file: Path to the output CSV file.
    :param page_number: The page number to extract text from (0-indexed).
    """
    # Initialize PDF reader
    reader = PdfReader(pdf_file)

    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Try to extract text from the specified page
        try:
            page_text = reader.pages[page_number].extract_text()
            writer.writerow([page_text])  # Writing the text of the specific page to a new row
            print(f"Page {page_number + 1} text written to {csv_file}.")
        except IndexError:
            # If the specified page number is out of range
            print(f"Page {page_number + 1} does not exist in the PDF.")

def extract_pages(pdf_file, csv_file, page_number):
    """
    Extracts text from a specific page of the PDF and the following page, and writes it to a CSV file.

    :param pdf_file: Path to the input PDF file.
    :param csv_file: Path to the output CSV file.
    :param page_number: The page number to extract text from (0-indexed).
    """
    # Initialize PDF reader
    reader = PdfReader(pdf_file)

    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Extract text from the specified page and the next page
        for i in range(page_number, page_number + 2):  # Extract current and next page
            try:
                page_text = reader.pages[i].extract_text()
                writer.writerow([page_text])  # Write the text of the current page to a new row
                print(f"Page {i + 1} text written to {csv_file}.")
            except IndexError:
                # If the specified page number is out of range
                print(f"Page {i + 1} does not exist in the PDF.")

def ttttget_paragraph(input_file_path, output_file_path, poz_num):
    """Extracts content between poz_num and poz_num + 1 from the input file."""
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Create regex pattern to find poz_num and poz_num + 1
    start_pattern = rf"{poz_num}"
    end_pattern = rf"{poz_num + 1}"

    # Use regex to find the content between the specified numbers
    pattern = rf"{start_pattern}(.*?){end_pattern}"

    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        modified_content = match.group(0)  # Get the full match including poz_num and poz_num + 1

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print("Content modified successfully and saved to:", output_file_path)
    else:
        print(f"Content between {poz_num} and {poz_num + 1} not found.")

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
        
        print("Content modified successfully and saved to:", output_file_path)
    else:
        print(f"Content between '{start_pattern}' and '{end_pattern}' not found.")
    
def extract_identifiers(file_path):
    """Extracts numbers following 'KRS', 'PESEL', 'NIP', and 'REGON' until a non-digit character is reached, accounting for whitespace."""
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()

        # Define the regex pattern to match 'KRS', 'PESEL', 'NIP', or 'REGON' followed by any amount of whitespace and digits
        pattern = r"(KRS|PESEL|NIP|REGON)\s*(\d+)"

        # Find all matches in the input text
        matches = re.findall(pattern, input_text)

        if matches:
            # Print the found identifiers with their corresponding numbers
            for identifier, number in matches:
                print(f"Found {identifier}: {number}")
            return matches
        else:
            print("No identifiers found.")
            return []
    
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def process_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # List to store the new rows with additional columns
    new_rows = []

    # Loop through each row of the dataframe
    for index, row in df.iterrows():
        monitor_id = row['MonitorID']
        page_num = row['PageNum']

        # Call the functions
        save_pdf(page_num)  # Save the PDF based on PageNum
        paragraph = cut_paragraph(monitor_id)  # Cut the paragraph based on MonitorID
        identifiers = extract_identifiers(paragraph)  # Extract identifiers like PESEL, KRS, NIP, REGON

        # Create a new row with existing data and the new identifiers
        new_row = {
            **row,  # Existing data
            'PESEL': identifiers['PESEL'],
            'KRS': identifiers['KRS'],
            'NIP': identifiers['NIP'],
            'REGON': identifiers['REGON']
        }

        new_rows.append(new_row)

    # Create a new dataframe with the additional columns
    new_df = pd.DataFrame(new_rows)

    # Save the new dataframe to the output CSV file
    new_df.to_csv(output_file, index=False)




















extract_pages(pdf_path, p2c_path, page_number)
time.sleep(2)
get_paragraph(p2c_path, paragraph_path, poz_num)
time.sleep(2)
extract_identifiers(paragraph_path)
time.sleep(2)