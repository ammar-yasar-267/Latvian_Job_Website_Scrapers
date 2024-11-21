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
driver.get("https://karjera.bite.lv/jobs")  # Replace with the actual URL

# Allow the page to load fully
time.sleep(3)

# Prepare the CSV file in the new folder
csv_file = os.path.join(output_folder, "bite_jobs.csv")
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Job Title", "Job Category", "Location", "Job URL"])

    # Find all job cards
    job_cards = driver.find_elements(By.CSS_SELECTOR, "ul#jobs_list_container > li.block-grid-item")

    for card in job_cards:
        try:
            # Extract job title
            job_title_element = card.find_element(By.CSS_SELECTOR, "span.company-link-style")
            job_title = job_title_element.text.strip()

            # Extract job category and location
            details = card.find_element(By.CSS_SELECTOR, "div.text-md").text.strip()
            details_parts = details.split("·")
            job_category = details_parts[0].strip() if len(details_parts) > 0 else ""
            job_location = details_parts[1].strip() if len(details_parts) > 1 else ""

            # Extract job URL
            job_url = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            # Write the data to the CSV file
            writer.writerow([job_title, job_category, job_location, job_url])

            # Print the data (optional)
            print(f"Job Title: {job_title}")
            print(f"Category: {job_category}")
            print(f"Location: {job_location}")
            print(f"URL: {job_url}")
            print("-" * 50)

        except Exception as e:
            print(f"Error processing job card: {e}")
            continue

# Close the WebDriver
driver.quit()

print(f"Job listings have been saved to {csv_file}")
