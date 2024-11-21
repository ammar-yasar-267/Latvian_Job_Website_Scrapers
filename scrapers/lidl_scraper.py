import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Create the output directory
output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path if needed
os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed

# Open the job listing page
driver.get("https://karjera.lidl.lv/meklet-darbu")  # Replace with the actual URL

# Allow the page to load fully
time.sleep(3)

# Handle cookie popup
try:
    cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookie_button.click()
except Exception as e:
    print(f"Cookie button not found or could not be clicked: {e}")

# Find all job cards
job_cards = driver.find_elements(By.CLASS_NAME, "jobResult")

# Define the CSV file path in the new folder
csv_file = os.path.join(output_folder, "lidl_scraper.csv")

# Open a CSV file for writing
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Job Title", "Location", "URL"])

    for card in job_cards:
        try:
            # Check if the job card is closed
            if "jobResult_open" not in card.get_attribute("class"):
                # Find the expand button/icon and click it
                expand_button = card.find_element(By.CLASS_NAME, "jobOpenDescription")
                expand_button.click()
                time.sleep(1)  # Give time for the content to expand

            # Extract job details
            job_title = card.find_element(By.CLASS_NAME, "jobTitle").text
            job_contractType = card.find_element(By.CLASS_NAME, "jobResult-contractTypeText").text
            job_contractType = job_contractType.replace('Līguma veids:', '').strip()  # Clean up the contract type
            salary_element = card.find_element(By.CLASS_NAME, "jobResult-grossSalaryText")
            job_salary = salary_element.text
            job_location = card.find_element(By.CLASS_NAME, "location").text
            job_url = card.find_element(By.CLASS_NAME, "jobResult-applyButton").get_attribute("href")

            # Write the data row to the CSV file
            writer.writerow([job_title, job_location, job_url])

            # Print the extracted data for debugging
            print(f"Job Title: {job_title}")
            print(f"Contract Type: {job_contractType}")
            print(f"Salary: {job_salary}")
            print(f"Location: {job_location}")
            print(f"URL: {job_url}")
            print("-" * 50)

        except Exception as e:
            print(f"Error processing job card: {e}")
            continue

# Close the WebDriver
driver.quit()

print(f"Scraping complete. Data saved to {csv_file}")
