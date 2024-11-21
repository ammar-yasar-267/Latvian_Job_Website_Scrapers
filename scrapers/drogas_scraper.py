import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Create the output directory
output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path if needed
os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize the WebDriver (ensure the driver is in PATH or provide the executable path)
driver = webdriver.Chrome()

# Open the target URL
url = "https://www.drogas.lv/lv/blog/category/karjera/vakances/"
driver.get(url)

# Allow the page to load
time.sleep(5)

# Handle cookies
try:
    cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
    cookie_button.click()
except Exception as e:
    print(f"Cookie button not found or could not be clicked: {e}")

# Locate all job articles
job_articles = driver.find_elements(By.CSS_SELECTOR, "article.article-grid")

# Define the CSV file path in the new folder
csv_file = os.path.join(output_folder, "drogas_jobs.csv")

# Open a CSV file to save the data
with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["Job Title", "Job URL", "Post Date"])

    # Loop through all job articles
    for article in job_articles:
        try:
            # Extract the job title
            job_title = article.find_element(By.CSS_SELECTOR, "h2.entry-title a").text.strip()

            # Extract the job URL
            job_url = article.find_element(By.CSS_SELECTOR, "h2.entry-title a").get_attribute("href")

            # Extract post date and updated date
            dates = article.find_elements(By.CSS_SELECTOR, "time.entry-date")
            post_date = dates[0].get_attribute("datetime") if dates else ""

            # Write to CSV
            writer.writerow([job_title, job_url, post_date])

            # Print the data to console (for debugging)
            print(f"Job Title: {job_title}")
            print(f"Job URL: {job_url}")
            print(f"Post Date: {post_date}")
            print("-" * 50)

        except Exception as e:
            print(f"Error processing an article: {e}")

# Close the WebDriver
driver.quit()

print(f"Scraping complete. Data saved to {csv_file}")
