import pandas as pd

# Define the input and output file paths
date = "30092024"
input_file_path = fr'C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-updated.csv'
output_file_path = fr'C:\Users\pdf\Desktop\monitor\test3\data\db\{date}-final.csv'

# Read the CSV file
df = pd.read_csv(input_file_path)

# Drop the specified columns
df = df.drop(columns=['MonitorID', 'PageNum'])

df = df.rename(columns={'FullName': 'NAZWA'})

# Save the modified DataFrame to a new CSV file
df.to_csv(output_file_path, index=False)

print("Columns removed and new file saved.")
