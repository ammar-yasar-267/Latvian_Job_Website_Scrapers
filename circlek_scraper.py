from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from datetime import datetime, timedelta
import time

def convert_relative_date(relative_date):
    today = datetime.today()
    # Remove the "posted on" prefix
    print('Processed relative date:', relative_date.lower().replace("posted on\n", ""))  # Debugging output
    relative_date = relative_date.lower().replace("posted on\n", "").strip()
    if relative_date == "today":
        return today.strftime('%Y-%m-%d')
    elif relative_date == "yesterday":
        return (today - timedelta(days=1)).strftime('%Y-%m-%d')
    elif "day" in relative_date:
        days_ago = int(''.join(filter(str.isdigit, relative_date)))
        return (today - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    else:
        return relative_date  # Return as is if it's already a date or unknown format

# Set up the WebDriver
driver = webdriver.Chrome()

# Open the target URL
url = 'https://circlek.wd3.myworkdayjobs.com/en-US/CircleKStoreJobs?locationCountry=1c026f3b1b8640d8bdfcb95466663e4d'
driver.get(url)

# Allow time for the page to load
time.sleep(5)

# Initialize list to store all job data
jobs = []

while True:
    # Allow time for content to load
    time.sleep(3)

    # Find all job elements on the current page
    job_elements = driver.find_elements(By.CSS_SELECTOR, 'li.css-1q2dra3')
    for job in job_elements:
        # Extract job details
        try:
            title = job.find_element(By.CSS_SELECTOR, '[data-automation-id="jobTitle"]').text
            job_url = job.find_element(By.CSS_SELECTOR, '[data-automation-id="jobTitle"]').get_attribute('href')
        except:
            title, job_url = "N/A", "N/A"

        try:
            location = job.find_element(By.CLASS_NAME, 'css-129m7dg').text
        except:
            location = "N/A"

        try:
            posted_date_relative = job.find_element(By.CSS_SELECTOR, '[data-automation-id="postedOn"]').text
            posted_date = convert_relative_date(posted_date_relative)
        except:
            posted_date = "N/A"

        # Append job details
        jobs.append({
            'Title': title,
            'URL': job_url,
            'Location': location,
            'Posted Date': posted_date
        })

    # Try to click the "Next" button
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="next"]')
        if next_button.is_enabled():
            next_button.click()
        else:
            break  # Exit loop if the button is disabled
    except NoSuchElementException:
        break  # Exit loop if no "Next" button is found

# Save jobs to CSV
df = pd.DataFrame(jobs)
df.to_csv('circlek_jobs_all_pages.csv', index=False, encoding='utf-8')

print('Job listings from all pages have been saved to circlek_jobs_all_pages.csv')

# Close the WebDriver
driver.quit()
