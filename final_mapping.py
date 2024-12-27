import os
import json
import pandas as pd
import re

# Paths to your input data
json_file_path = '/home/whitewolf/Downloads/Securin/cis_nist_attack_mapping.json'
csv_folder_path = '/home/whitewolf/Downloads/Securin/cleaned_csv'
technique_json_file_path = '/home/whitewolf/Downloads/Securin/threatActors_data.json'  # New JSON file with Techniques details
output_folder_path = '/home/whitewolf/Downloads/Securin/final_mapping'

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Load JSON dataimport os
import json
import pandas as pd
import re

# Paths to your input data
json_file_path = '/home/whitewolf/Downloads/Securin/cis_nist_attack_mapping.json'
excel_file_path = '/home/whitewolf/Downloads/Securin/CIS_Controls_v8_to_Enterprise_ATTCK_v82_Master_Mapping__5262021.xlsx'
csv_folder_path = '/home/whitewolf/Downloads/Securin/cleaned_csv'
technique_json_file_path = '/home/whitewolf/Downloads/Securin/threatActors_data.json'  # New JSON file with Techniques details
output_folder_path = '/home/whitewolf/Downloads/Securin/final_mapping'

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Load JSON data
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)  # json_data is a list of dictionaries

# Load Technique JSON data
with open(technique_json_file_path, 'r') as technique_file:
    technique_data = json.load(technique_file)  # technique_data is a list of dictionaries

# Load the Excel sheet
excel_data = pd.read_excel(excel_file_path, sheet_name='V8-ATT&CK Low (Sub-)Techniques')

# Loop through CSV files in the specified folder
for filename in os.listdir(csv_folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_folder_path, filename)
        df = pd.read_csv(file_path)

        # Prepare list for storing matched data for this CSV
        matched_data = []

        # Iterate through each row in the CSV and match CIS Control Number with JSON CIS Sub-Control
        for _, row in df.iterrows():
            # Assuming "Benchmark Title" and "CIS Control Number and Title" are the columns in CSV
            control_number_title = row['CIS Control Number and Title']

            # Extract control number after "v8" prefix using regular expression
            match = re.search(r'v8\s*([\d.]+)', control_number_title)
            if match:
                control_number = match.group(1).strip()  # Extract the control number part

                # Check the Excel file first
                excel_match = excel_data[excel_data['CIS Control'] == control_number]
                if not excel_match.empty:
                    # Found in Excel, use ATT&CK Technique ID
                    technique_id = excel_match['Combined ATT&CK (Sub-)Technique ID'].values[0]
                    attack_technique_description = excel_match.get('Technique Description', "N/A")
                    cis_description = "Mapped through Excel"

                    # Collect all threat actors associated with this technique ID
                    threat_actors = []
                    threat_actor_descriptions = []
                    for tech_entry in technique_data:
                        for technique in tech_entry.get("techniques", []):
                            if technique.get("id") == technique_id:
                                # Add threat actor name and description if available
                                threat_actors.append(tech_entry.get("name", "N/A"))
                                threat_actor_descriptions.append(tech_entry.get("description", "N/A"))

                    # Convert NoneType to "N/A" before joining
                    threat_actors_str = "; ".join(str(actor) if actor else "N/A" for actor in threat_actors) if threat_actors else "N/A"
                    threat_actor_descriptions_str = "; ".join(str(desc) if desc else "N/A" for desc in threat_actor_descriptions) if threat_actor_descriptions else "N/A"

                    # Append the matched information
                    matched_data.append({
                        'Benchmark Title': row['Benchmark Title'],
                        'Matched CIS Sub-Control': control_number,
                        'JSON Title': "N/A",
                        'CIS Description': cis_description,
                        'Technique ID': technique_id,
                        'Attack Technique Description': attack_technique_description,
                        'Threat Actors': threat_actors_str,
                        'Threat Actor Descriptions': threat_actor_descriptions_str,
                    })
                    continue  # Skip JSON check since found in Excel

                # Fallback to JSON file if not found in Excel
                for item in json_data:
                    json_cis_control = str(item["CIS Sub-Control"])  # Convert to string for easier matching

                    # Check if the control number matches the CIS Sub-Control from JSON
                    if control_number == json_cis_control:
                        # Extract Technique ID from the original JSON item
                        technique_id = item["Technique ID"]
                        cis_description = item.get("Description", "N/A")  # Description from CIS JSON
                        attack_technique_description = item.get("Technique Name", "N/A")  # Technique Name from CIS JSON

                        # Collect all threat actors associated with this technique ID
                        threat_actors = []
                        threat_actor_descriptions = []
                        for tech_entry in technique_data:
                            for technique in tech_entry.get("techniques", []):
                                if technique.get("id") == technique_id:
                                    # Add threat actor name and description if available
                                    threat_actors.append(tech_entry.get("name", "N/A"))
                                    threat_actor_descriptions.append(tech_entry.get("description", "N/A"))

                        # Convert NoneType to "N/A" before joining
                        threat_actors_str = "; ".join(str(actor) if actor else "N/A" for actor in threat_actors) if threat_actors else "N/A"
                        threat_actor_descriptions_str = "; ".join(str(desc) if desc else "N/A" for desc in threat_actor_descriptions) if threat_actor_descriptions else "N/A"

                        # Append the matched information
                        matched_data.append({
                            'Benchmark Title': row['Benchmark Title'],
                            'Matched CIS Sub-Control': json_cis_control,
                            'JSON Title': item["Title"],
                            'CIS Description': cis_description,
                            'Technique ID': technique_id,
                            'Attack Technique Description': attack_technique_description,
                            'Threat Actors': threat_actors_str,
                            'Threat Actor Descriptions': threat_actor_descriptions_str,
                        })

        # Save the matched data to a new CSV file in the output folder
        if matched_data:
            matched_df = pd.DataFrame(matched_data)
            output_file_path = os.path.join(output_folder_path, f"matched_{filename}")
            matched_df.to_csv(output_file_path, index=False)
            print(f"Matched data saved to {output_file_path}.")
        else:
            print(f"No matches found for {filename}.")

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)  # json_data is a list of dictionaries

# Load Technique JSON data
with open(technique_json_file_path, 'r') as technique_file:
    technique_data = json.load(technique_file)  # technique_data is a list of dictionaries

# Loop through CSV files in the specified folder
for filename in os.listdir(csv_folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_folder_path, filename)
        df = pd.read_csv(file_path)

        # Prepare list for storing matched data for this CSV
        matched_data = []

        # Iterate through each row in the CSV and match CIS Control Number with JSON CIS Sub-Control
        for _, row in df.iterrows():
            # Assuming "Benchmark Title" and "CIS Control Number and Title" are the columns in CSV
            control_number_title = row['CIS Control Number and Title']

            # Extract control number after "v8" prefix using regular expression
            match = re.search(r'v8\s*([\d.]+)', control_number_title)
            if match:
                control_number = match.group(1).strip()  # Extract the control number part

                # Iterate over each item in the original JSON list and find matches
                for item in json_data:
                    json_cis_control = str(item["CIS Sub-Control"])  # Convert to string for easier matching

                    # Check if the control number matches the CIS Sub-Control from JSON
                    if control_number == json_cis_control:
                        # Extract Technique ID from the original JSON item
                        technique_id = item["Technique ID"]
                        cis_description = item.get("Description", "N/A")  # Description from CIS JSON
                        attack_technique_description = item.get("Technique Name", "N/A")  # Technique Name from CIS JSON

                        # Collect all threat actors associated with this technique ID
                        threat_actors = []
                        threat_actor_descriptions = []
                        for tech_entry in technique_data:
                            for technique in tech_entry.get("techniques", []):
                                if technique.get("id") == technique_id:
                                    # Add threat actor name and description if available
                                    threat_actors.append(tech_entry.get("name", "N/A"))
                                    threat_actor_descriptions.append(tech_entry.get("description", "N/A"))

                        # Convert NoneType to "N/A" before joining
                        threat_actors_str = "; ".join(str(actor) if actor else "N/A" for actor in threat_actors) if threat_actors else "N/A"
                        threat_actor_descriptions_str = "; ".join(str(desc) if desc else "N/A" for desc in threat_actor_descriptions) if threat_actor_descriptions else "N/A"

                        # Append the matched information
                        matched_data.append({
                            'Benchmark Title': row['Benchmark Title'],
                            'Matched CIS Sub-Control': json_cis_control,
                            'JSON Title': item["Title"],
                            'CIS Description': cis_description,
                            'Technique ID': technique_id,
                            'Attack Technique Description': attack_technique_description,
                            'Threat Actors': threat_actors_str,
                            'Threat Actor Descriptions': threat_actor_descriptions_str,
                        })

        # Save the matched data to a new CSV file in the output folder
        if matched_data:
            matched_df = pd.DataFrame(matched_data)
            output_file_path = os.path.join(output_folder_path, f"matched_{filename}")
            matched_df.to_csv(output_file_path, index=False)
            print(f"Matched data saved to {output_file_path}.")
        else:
            print(f"No matches found for {filename}.")
