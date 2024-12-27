from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import requests

# Specify the path to your ChromeDriver
# chrome_driver_path = "C:/Users/Administrator/Desktop/CIS/chromedriver"

download_folder = os.path.abspath("C:/Users/Administrator/Desktop/CIS/CIS_BENCHMARK")

# Create the download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

# Set up Chrome options for automatic download
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_folder,  # Set the download directory
    "download.prompt_for_download": False,  # Do not prompt for download
    "plugins.always_open_pdf_externally": True  # Open PDFs directly instead of within Chrome
}
chrome_options.add_experimental_option("prefs", prefs)

# Create a service object with the ChromeDriver path
# service = Service(chrome_driver_path)

# Initialize Chrome WebDriver using the service
driver = webdriver.Chrome(options=chrome_options)

# Open the target website with the PDFs in dropdowns
driver.get('https://downloads.cisecurity.org/#/')  # Replace with the actual website URL

# Allow time for the page to load
time.sleep(2)
try:
    accept_button = driver.find_element(By.CSS_SELECTOR, ".c-button")  # Adjust this selector based on the actual site
    accept_button.click()
    print("Accepted cookies.")
except Exception as e:
    print("No cookie consent button found or already accepted.")
    print(f"Error: {e}")

print("Looking for dropdowns...")
try:
    dropdowns = driver.find_elements(By.CSS_SELECTOR, ".well.section")  # Replace with actual CSS selector
    print(f"Found {len(dropdowns)} dropdowns.")

    # Click each dropdown to reveal PDFs
    for dropdown in dropdowns:
        dropdown.click()
        time.sleep(1)
        print("Clicked a dropdown.")
except Exception as e:
    print("Error finding or clicking dropdowns.")
    print(f"Error: {e}")
print("Looking for 'Download PDF' buttons...")
try:
    pdf_buttons = driver.find_elements(By.XPATH, "//a[@title='Download PDF']")  # Search for buttons by title attribute
    print(f"Found {len(pdf_buttons)} buttons with 'Download PDF' title.")

    if len(pdf_buttons) == 0:
        print("No PDF buttons found.")
    else:
        # Click each "Download PDF" button to download the file
        for i, button in enumerate(pdf_buttons):
            try:
                button.click()  # Click the button to trigger the download
                print(f"Clicked download button {i + 1}.")
                time.sleep(3)  # Allow time for the download to start

            except Exception as e:
                print(f"Error clicking download button {i + 1}: {e}")
except Exception as e:
    print("Error finding or downloading PDFs.")
    print(f"Error: {e}")

# Close the browser
driver.quit()
print("Closed the browser.")