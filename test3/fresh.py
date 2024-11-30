import csv
from PyPDF2 import PdfReader
import re
import time
import pandas as pd


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


# Poz. 45811. SILCON HOLDING SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ W UPADŁOŚCI we Wrocławiu 24
# 45787,Złocki Damian,17

pdf_path = r"C:\Users\pdf\Desktop\monitor\test3\data\raw\20092024.pdf"
# new path for each iteration
# x = 24
# PageNum = x-1
# MonitorID = 45811

# pages_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_page_{x}.csv"
# paragraph_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_paragraph_{MonitorID}.txt"
# extract_pages(pdf_path, pages_path, PageNum)
# time.sleep(1)
# get_paragraph(pages_path, paragraph_path, MonitorID)
# time.sleep(1)
# extract_identifiers(paragraph_path)





file_path = r'C:\Users\pdf\Desktop\monitor\test3\data\db\20092024.csv'
# Open the CSV file and read its contents
with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)  # Use DictReader to read rows as dictionaries
    # Loop through each row in the CSV file
    for row in reader:
        # Print the MonitorID and PageNum
        print(f"Executing scripts for: MonitorID: {row['MonitorID']}, PageNum: {row['PageNum']}")
        MonitorID = row['MonitorID']
        PageNum = row['PageNum']
        pages_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_page_{PageNum}.csv"
        paragraph_path = fr"C:\Users\pdf\Desktop\monitor\test3\data\temp\20092024_paragraph_{MonitorID}.txt"
        PageNum_Corrected = int(PageNum) - 1
        MonitorID_Corrected = int(MonitorID)
        extract_pages(pdf_path, pages_path, PageNum_Corrected)
        time.sleep(1)
        get_paragraph(pages_path, paragraph_path, MonitorID_Corrected)
        time.sleep(1)
        extract_identifiers(paragraph_path)
        print('well done')




# ffffd