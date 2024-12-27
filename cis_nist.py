import pandas as pd

# Load the Excel files
file1_path = 'nist800-53-r4-mappings.xlsx'
file2_path = 'CIS_Controls_v8_Mapping_to_NIST_SP_800_53_Rev_5_Moderate_and_Low_Base.xlsx'

# Load the specific sheets from both files
file1_df = pd.read_excel(file1_path, sheet_name='Mappings')
file2_df = pd.read_excel(file2_path, sheet_name='All CIS Controls & Safeguards')

# Select relevant columns from the NIST file
nist_df = file1_df[['Control ID', 'Control Name', 'Technique ID', 'Technique Name']].dropna()

# Select relevant columns from the CIS file
cis_df = file2_df[['CIS Control', 'CIS Sub-Control', 'Title', 'Control Identifier', 'Control or Control Enhancement Name']].dropna()

# Merge the data based on the NIST Control ID and CIS Control Identifier
merged_df = pd.merge(nist_df, cis_df, left_on='Control ID', right_on='Control Identifier', how='inner')

# Display the merged dataframe
print(merged_df)

# Save the result to a CSV file if needed
merged_df.to_csv('merged_nist_cis_techniques.csv', index=False)
