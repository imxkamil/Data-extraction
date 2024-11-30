import csv
import json


date = "30092024"
input_file_path = fr'C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-final.csv'
# Define the output file path
output_file_path = fr'C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-final.json'



# Initialize a list to hold the key-value pairs
key_value_pairs = []

# Read the CSV file
with open(input_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)  # Read the headers
    for row in csv_reader:
        record_dict = {headers[i]: row[i] for i in range(len(headers))}
        key_value_pairs.append(record_dict)

# Save the key-value pairs to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(key_value_pairs, json_file, ensure_ascii=False, indent=4)

print(f"JSON file saved at: {output_file_path}")
