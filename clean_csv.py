import os
import pandas as pd

# Define the input and output folder paths
input_folder_path = '/home/whitewolf/Downloads/Securin/output_csv'
output_folder_path = '/home/whitewolf/Downloads/Securin/cleaned_csv'

# Create the output folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.csv'):
        input_file_path = os.path.join(input_folder_path, filename)
        
        # Read the CSV file
        df = pd.read_csv(input_file_path)
        
        # Remove duplicates
        df_cleaned = df.drop_duplicates()
        
        # Define the output file path
        output_file_path = os.path.join(output_folder_path, filename)
        
        # Save the cleaned DataFrame to the output folder
        df_cleaned.to_csv(output_file_path, index=False)
        
        print(f"Duplicates removed and saved to {output_file_path}.")

print("All CSV files processed and cleaned files saved to the output folder.")
