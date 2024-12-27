# Securin_CIS
# Project Overview

This repository contains Python scripts for mapping CIS Benchmarks, ATT&CK Techniques, and NIST Controls, as well as automating data extraction and filtering tasks related to cybersecurity frameworks.

---

## Table of Contents

1. [Scripts Overview](#scripts-overview)
2. [Setup Instructions](#setup-instructions)
3. [Usage](#usage)
4. [Dependencies](#dependencies)
5. [License](#license)

---

## Scripts Overview

### 1. extract_attacks.py
**Purpose:** Retrieves Enterprise ATT&CK techniques from the MITRE ATT&CK API and saves them as a CSV file.

**Output:**
- CSV file: `mitre_attack_techniques_by_id.csv`.
- Raw text file: `mitre_attack_techniques_raw.txt`.

### 2. controls_json.py
**Purpose:** Generates a JSON file mapping CIS controls to ATT&CK techniques from an Excel sheet.

**Output:**
- JSON file: `cis_to_attack_low_mit_mapping.json`.

### 3. control_mapping.py
**Purpose:** Identifies CIS mappings with missing ATT&CK Technique IDs and generates a report.

**Output:**
- CSV file: `nan_attack_low_mit_technique_report.csv`.

### 4. cis_nist.py
**Purpose:** Maps CIS controls to NIST controls and merges relevant data.

**Output:**
- Merged CSV: `merged_nist_cis_techniques.csv`.
- JSON file: `cis_nist_attack_mapping.json`.

### 5. download_html.py
**Purpose:** Automates the downloading of CIS Benchmark PDFs from a target website.

**Output:**
- Downloads PDFs to a specified folder.

### 6. clean_csv.py
**Purpose:** Cleans CSV files by removing duplicate rows.

**Output:**
- Cleaned CSV files saved to the specified folder.

### 7. cis_control_attack_nist.py
**Purpose:** Maps CIS controls to NIST and ATT&CK techniques and saves the mappings in JSON.

**Output:**
- JSON file: `cis_nist_attack_mapping.json`.

### 8. final_mapping.py
**Purpose:** Maps CIS controls to ATT&CK techniques using both Excel and JSON mappings and generates enriched CSVs.

**Output:**
- Enriched CSV files saved in a specified folder.

### 9. llm_mapping.py
**Purpose:** Filters mappings based on relevance scores generated using a language model.

**Output:**
- Filtered CSV files saved in a specified folder.

### 10. download_pdf.py
**Purpose:** Automates the downloading of CIS Benchmark PDFs from a website.

**Output:**
- Downloads PDFs to the specified folder.

### 11. process_pdf.py
**Purpose:** Extracts CIS v8 benchmarks and controls from PDFs and saves them as CSV files.

**Output:**
- CSV files saved in the `output_csvs/` folder.

---

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies:**
   Install required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Paths:**
   Update file paths in the scripts as necessary to match your local environment.

---

## Usage

- **Run a Specific Script:**
  ```bash
  python <script_name>.py
  ```

- **Batch Processing:**
  Some scripts like `process_pdf.py` can process multiple files in a folder.

---

## Dependencies

- Python 3.8+
- Required Libraries:
  - pandas
  - pdfplumber
  - selenium
  - openpyxl
  - requests

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

For questions or contributions, please contact shashank.prakash@securin.io
.

