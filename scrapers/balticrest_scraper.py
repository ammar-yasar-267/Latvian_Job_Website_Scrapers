import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Create the output directory
output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path if needed
os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize the WebDriver
driver = webdriver.Chrome()  # Make sure to have ChromeDriver installed and in PATH

# Open the target URL
url = "https://www.balticrest.com/latvija/lv/karjera/vakances/"  # Replace with the actual URL
driver.get(url)

# Allow the page to load completely
driver.implicitly_wait(10)

# Locate all expandable items
vacancy_items = driver.find_elements(By.CSS_SELECTOR, "div.vacanciesBlock div.item")

# Prepare the CSV file in the new folder
csv_file = os.path.join(output_folder, "balticrest_jobs.csv")
with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow(["Job Title", "Job Details", "Requirements", "Work Schedule", "Salary", "Contact Email", "Address"])

    # Iterate through each vacancy item
    for item in vacancy_items:
        try:
            # Find the toggle button and expand the item
            toggle_button = item.find_element(By.CSS_SELECTOR, "div.headToggle")
            ActionChains(driver).move_to_element(toggle_button).click(toggle_button).perform()
            time.sleep(1)  # Allow the content to expand
            
            # Extract details
            job_title = item.find_element(By.CSS_SELECTOR, "div.headToggle h3").text.strip()
            details_section = item.find_element(By.CSS_SELECTOR, "div.text")
            
            # Extract job details, requirements, schedule, salary, etc.
            job_details = details_section.find_element(By.CSS_SELECTOR, "div.text__item--left").text.strip()
            requirements = details_section.find_element(By.CSS_SELECTOR, "div.text__item--right").text.strip()
            
            # Parse specific fields
            work_schedule = "N/A"
            salary = "N/A"
            email = "N/A"
            address = "N/A"

            # Look for specific details in the right text block
            for div in details_section.find_elements(By.CSS_SELECTOR, "div.text__item--right div"):
                text = div.text.strip()
                if "Darba grafiki" in text or "Darba grafiks" in text:
                    work_schedule = text
                elif "Atalgojums" in text or "Darba samaksa" in text:
                    salary = text
                elif "e-pastu" in text:
                    email_element = div.find_element(By.TAG_NAME, "a")
                    email = email_element.get_attribute("href").replace("mailto:", "").strip()
                elif "Adrese" in text:
                    address = text
            
            # Write data to the CSV file
            writer.writerow([job_title, job_details, requirements, work_schedule, salary, email, address])
        
        except Exception as e:
            print(f"Error processing item: {e}")

# Close the WebDriver
driver.quit()

print(f"Scraping completed. Data saved to {csv_file}")
