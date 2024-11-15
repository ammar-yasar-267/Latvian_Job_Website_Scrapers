from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time

# Initialize the WebDriver (ensure the driver is in PATH or provide the executable path)
driver = webdriver.Chrome()

# Open the target URL
url = "https://www.drogas.lv/lv/blog/category/karjera/vakances/"
driver.get(url)

# Allow the page to load
time.sleep(5)

cookie_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
cookie_button.click()

# Locate all job articles
job_articles = driver.find_elements(By.CSS_SELECTOR, "article.article-grid")

# Open a CSV file to save the data
csv_file = "drogas_jobs.csv"
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
