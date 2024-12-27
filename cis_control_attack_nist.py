import pandas as pd

# Step 1: Load the Excel files directly for NIST and CIS mappings
file1_path = 'nist800-53-r4-mappings.xlsx'  # NIST mappings
file2_path = 'CIS_Controls_v8_Mapping_to_NIST_SP_800_53_Rev_5_Moderate_and_Low_Base.xlsx'  # CIS mappings to NIST

# Load the specific sheets from both files
nist_df = pd.read_excel(file1_path, sheet_name='Mappings')  # Load NIST mapping sheet
cis_nist_df = pd.read_excel(file2_path, sheet_name='All CIS Controls & Safeguards')  # Load CIS-NIST mappings

# Step 2: Clean and select relevant columns from NIST and CIS sheets
# NIST file should have mappings like Control ID, Technique ID, Technique Name
nist_df = nist_df[['Control ID', 'Control Name', 'Technique ID', 'Technique Name']].dropna()

# CIS-NIST mapping file contains CIS Control, NIST Control ID, etc.
cis_nist_df = cis_nist_df[['CIS Control', 'CIS Sub-Control', 'Title','Description' ,'Control Identifier', 'Control or Control Enhancement Name']].dropna()

# Step 3: Merge CIS to NIST mappings
# Merge CIS mappings with NIST mappings based on the Control Identifier (which links the two)
cis_nist_merged_df = pd.merge(cis_nist_df, nist_df, left_on='Control Identifier', right_on='Control ID', how='inner')

# Step 4: Convert the merged DataFrame into JSON format
output_file = 'cis_nist_attack_mapping.json'
cis_nist_merged_json = cis_nist_merged_df.to_dict(orient='records')

# Step 5: Save the final JSON output to a file
import json
with open(output_file, 'w') as json_file:
    json.dump(cis_nist_merged_json, json_file, indent=4)

print(f"Final JSON mapping saved to {output_file}")
