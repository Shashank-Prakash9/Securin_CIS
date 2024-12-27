import pandas as pd
import json

# Load the Excel file
file_path = 'CIS_Controls_v8_to_Enterprise_ATTCK_v82_Master_Mapping__5262021.xlsx'  # Replace this with the path to your Excel file

df_mapping = pd.read_excel(file_path, sheet_name='V8-ATT&CK Low Mit. & (Sub-)Tech')

# Filter the relevant columns for mapping
df_filtered = df_mapping[['CIS Control', 'CIS Safeguard', 'ATT&CK Technique ID', 'ATT&CK Sub-Technique ID', 'ATT&CK (Sub-)Technique Name']]

# Remove rows where ATT&CK Technique ID contains `.0`
df_filtered = df_filtered[~df_filtered['CIS Safeguard'].astype(str).str.endswith('.0')]

# Convert the dataframe to JSON format, organizing it by CIS Control
cis_to_attack_mapping = df_filtered.groupby('CIS Control').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Write the JSON to a file
json_output_path = 'cis_to_attack_low_mit_mapping.json'
with open(json_output_path, 'w') as json_file:
    json.dump(cis_to_attack_mapping, json_file, indent=4)

print(f"JSON file saved to: {json_output_path}")
