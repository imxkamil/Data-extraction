import json
import pandas as pd




date = "30092024"
# Load the JSON file with UTF-8 encoding
json_file_path = fr'C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-final.json'
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Check if data is a list
if isinstance(data, list):
    # Assuming each element in the list is a dictionary
    df = pd.json_normalize(data)
    # Convert to key-value pairs
    keys = []
    values = []
    for index, row in df.iterrows():
        keys.extend(row.index.tolist())
        values.extend(row.values.tolist())
    
    # Create DataFrame
    final_df = pd.DataFrame({'Key': keys, 'Value': values})
else:
    raise ValueError("Expected JSON data to be a list of dictionaries.")

# Save the DataFrame to an Excel file
output_file_path = fr'C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-final.xlsx'
final_df.to_excel(output_file_path, index=False)

print(f'Excel file saved at: {output_file_path}')