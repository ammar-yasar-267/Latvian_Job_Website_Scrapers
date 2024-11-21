import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Create the output directory
output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path if needed
os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH

# Open the target URL
url = "https://www.lido.lv/lv/karjera/"  # Replace this with the actual URL if different
driver.get(url)

# Allow the page to load
driver.implicitly_wait(5)

# Locate all job items
job_items = driver.find_elements(By.CSS_SELECTOR, "ul.vacancies__list li.vacancies__item")

# Define the CSV file path in the new folder
csv_file = os.path.join(output_folder, "lido_jobs.csv")

# Open a CSV file to save the data
with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Job Title", "Job Location", "Job URL"])

    # Loop through each job item and extract details
    for job in job_items:
        try:
            # Extract job title
            job_title = job.find_element(By.CSS_SELECTOR, "a.vacancies__link").text.strip()

            # Extract job location
            job_location = job.find_element(By.CSS_SELECTOR, "div.vacancies__restaurant").text.strip()

            # Extract job URL
            job_url = job.find_element(By.CSS_SELECTOR, "a.vacancies__link").get_attribute("href")

            # Write to CSV
            writer.writerow([job_title, job_location, job_url])

        except Exception as e:
            print(f"Error processing a job item: {e}")

# Close the WebDriver
driver.quit()

print(f"Scraping complete. Data saved to {csv_file}")
