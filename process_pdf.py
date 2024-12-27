import pdfplumber
import re
import csv
import os

# Function to extract benchmark titles and CIS v8 controls
def extract_benchmarks_and_controls_v8(pdf_path):
    extracted_data = []
    current_benchmark = None  # Track the current benchmark

    with pdfplumber.open(pdf_path) as pdf:
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            
            # Extract text from the page to find benchmarks (chapter titles followed by "Profile Applicability")
            page_text = page.extract_text()

            # Find benchmarks followed by "Profile Applicability"
            benchmark_pattern = r"(\d+\.\d+.*?)\nProfile Applicability"
            benchmarks = re.findall(benchmark_pattern, page_text)

            # If a benchmark is found, update the current benchmark
            if benchmarks:
                current_benchmark = benchmarks[0].strip()  # Capture the full benchmark title

            # Extract table content for CIS controls
            table_content = page.extract_table()

            # Process table rows for v8 CIS controls and link them to the current benchmark
            if current_benchmark and table_content:
                for row in table_content:
                    # Ensure the row has enough columns (at least 2) to avoid IndexError
                    if len(row) > 1:
                        version = row[0]  # Control version (e.g., "v8", "v7")
                        control = row[1]  # Control number and title (e.g., "v8 Control 3.11")
                        
                        # Only process v8 controls
                        if version == 'v8' and control:
                            control_text = f"{version} {control.strip()}"
                            
                            # Append the v8 control to the current benchmark
                            extracted_data.append({
                                "Benchmark Title": current_benchmark,  
                                "CIS Control Number and Title": control_text  
                            })
    
    return extracted_data

# Function to write the extracted data to a CSV file
def write_benchmarks_to_csv(extracted_data, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Benchmark Title", "CIS Control Number and Title"])
        writer.writeheader()
        for entry in extracted_data:
            writer.writerow(entry)

# Function to process all PDFs in a folder
def process_pdfs_in_folder(folder_path, output_folder):
    # Get a list of all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        output_file = os.path.join(output_folder, f'{os.path.splitext(pdf_file)[0]}_v8_benchmarks_and_controls.csv')

        v8_benchmark_controls = extract_benchmarks_and_controls_v8(pdf_path)
        
        # Write the extracted data to a CSV file
        write_benchmarks_to_csv(v8_benchmark_controls, output_file)
        print(f"Data successfully written to {output_file}")

# Main function to extract and save v8 benchmarks and controls from all PDFs in a folder
def main():
    folder_path = 'CIS_BENCHMARK/'  # Path to the folder containing PDFs
    output_folder = 'output_csvs/'  # Folder where CSVs will be saved

    # Ensure the output folder exists, create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Process all PDFs in the folder
    process_pdfs_in_folder(folder_path, output_folder)

if __name__ == "__main__":
    main()
