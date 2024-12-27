import json
import pandas as pd

# Load the JSON data
file_path = 'cis_to_attack_low_mit_mapping.json'  # Replace with your JSON file path
with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize a list to store the CIS Control mappings with NaN ATT&CK Technique IDs
nan_mappings = []

# Loop through the CIS Controls
for cis_control, mappings in data.items():
    for mapping in mappings:
        if pd.isna(mapping['ATT&CK Technique ID']):
            nan_mappings.append({
                'CIS Control': mapping['CIS Control'],
                'CIS Safeguard': mapping['CIS Safeguard'],
                'ATT&CK Technique ID': mapping['ATT&CK Technique ID'],
                'ATT&CK (Sub-)Technique Name': mapping['ATT&CK (Sub-)Technique Name']
            })

# Convert the list of NaN mappings to a DataFrame for easier manipulation and reporting
df_nan_mappings = pd.DataFrame(nan_mappings)

# Save the report to a CSV file
report_path = 'nan_attack_low_mit_technique_report.csv'
df_nan_mappings.to_csv(report_path, index=False)

print(f"Report generated and saved to {report_path}")
