import os
import pandas as pd
from cerebras.cloud.sdk import Cerebras

input_csv_folder = "/home/whitewolf/Downloads/Securin/final_mapping"  # Folder containing the generated CSVs
output_csv_folder = "/home/whitewolf/Downloads/Securin/filtered_mapping"  # Folder for saving filtered CSVs

# Initialize Cerebras client
client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY"),
)

# Create output folder if it doesn't exist
os.makedirs(output_csv_folder, exist_ok=True)

# Function to query the model for a probabilistic relevance score
def evaluate_relevance(cis_desc, attack_desc):
    prompt = f"""
    You are a cybersecurity expert. Evaluate if the following attack technique is relevant to the CIS benchmark description:

    CIS Benchmark Description:
    {cis_desc}

    {attack_desc} is the name of the attack technique that is being evaluated.
   Give me a confidence score between 0 and 1, where 0 is irrelevant and 1 is relevant. Be extremely strict about the relation, i need you to give me a probablistic score between 0 and 1 representing the level of relation. Do not answer anything more.Just give me a number between 0 and 1.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3.1-8b",
        )
        response = chat_completion.choices[0].message.content.strip()
        # Attempt to convert response to float. If it fails, set score to 0.0
        print(f"Response: {response}")
        try:
            score = float(response)
        except ValueError:
            score = 0.0
        return score
    except Exception as e:
        print(f"Error querying API: {e}")
        return 0.0

# Process each CSV in the input folder
for filename in os.listdir(input_csv_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_csv_folder, filename)

        # Load the CSV
        df = pd.read_csv(file_path)

        # Ensure required columns exist
        if "CIS Description" in df.columns and "Attack Technique Description" in df.columns:
            # Prepare a list to store filtered rows
            filtered_rows = []

            # Iterate through rows and filter
            for _, row in df.iterrows():
                cis_description = row["CIS Description"]
                attack_description = row["Attack Technique Description"]

                # Query the model for relevance score
                relevance_score = evaluate_relevance(cis_description, attack_description)
                print(f"Relevance score: {relevance_score}")

                # Append to results if score > 0.7
                if relevance_score > 0.7:
                    filtered_rows.append(row)

            # Create a new DataFrame for filtered data
            filtered_df = pd.DataFrame(filtered_rows)

            # Save the filtered data
            output_file_path = os.path.join(output_csv_folder, f"filtered_{filename}")
            filtered_df.to_csv(output_file_path, index=False)
            print(f"Filtered data saved to {output_file_path}.")
        else:
            print(f"Required columns missing in {filename}. Skipping...")
