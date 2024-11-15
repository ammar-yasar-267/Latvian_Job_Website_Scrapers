from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed

# Open the job listing page
driver.get("https://karjera.lidl.lv/meklet-darbu")  # Replace with the actual URL

# Allow the page to load fully
time.sleep(3)

cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
cookie_button.click()

# Find all job cards
job_cards = driver.find_elements(By.CLASS_NAME, "jobResult")

# Open a CSV file for writing
with open("lidl_scraper.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Job Title", "Location", "URL"])

    # Find all job cards
    job_cards = driver.find_elements(By.CLASS_NAME, "jobResult")

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