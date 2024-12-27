from attackcti import attack_client
import pandas as pd

# Initialize the ATT&CK client
client = attack_client()

# Retrieve the Enterprise ATT&CK techniques
techniques = client.get_enterprise_techniques()
# print(techniques)
with open('mitre_attack_techniques_raw.txt', 'w') as txt_file:
    for technique in techniques:
        txt_file.write(str(technique) + '\n\n')

# Extract relevant information
technique_data = []
for technique in techniques:
    technique_data.append({
        'ID': technique['external_references'][0]['external_id'],
        'Name': technique['name'],
        'Description': technique.get('description', 'No description available')
    })

# Sort by ID
technique_data_sorted = sorted(technique_data, key=lambda x: x['ID'])

# Convert to DataFrame
df = pd.DataFrame(technique_data_sorted)

# Save to CSV
df.to_csv('mitre_attack_techniques_by_id.csv', index=False)

# Display the DataFrame
print(df)
