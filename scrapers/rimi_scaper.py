import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Create the output directory
output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path as needed
os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

# Initialize the WebDriver
driver = webdriver.Chrome()  # Or specify the path if needed
driver.get("https://darbs.rimi.lv/jobs")

# Allow the page to load fully
time.sleep(3)

# Handle cookies
try:
    cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelOptinAllowAll")
    cookie_button.click()
except Exception as e:
    print(f"Cookie button not found or could not be clicked: {e}")

# Load all jobs by clicking "Show More" until the button is no longer there
while True:
    try:
        show_more_button = driver.find_element(By.CSS_SELECTOR, "#show_more_button a")
        driver.execute_script("arguments[0].click();", show_more_button)
        time.sleep(2)  # Pause to let new jobs load
    except:
        break  # Break when "Show More" button is not found (all jobs are loaded)

# Use BeautifulSoup to parse the page's HTML after all jobs are loaded
soup = BeautifulSoup(driver.page_source, "html.parser")
jobs_list = []

# Find job items
for job in soup.select("#jobs_list_container li"):
    title_element = job.select_one("a span[title]")
    url_element = job.select_one("a[href]")
    
    if title_element and url_element:
        title = title_element["title"]
        url = url_element["href"]
        full_url = f"{url}"  # Complete the URL
        jobs_list.append({"Job Title": title, "URL": full_url})

# Save to a CSV file in the new folder
output_file = os.path.join(output_folder, "rimi_jobs.csv")
df = pd.DataFrame(jobs_list)
df.to_csv(output_file, index=False, header=["Job Title", "URL"])
print(f"Job data has been saved to {output_file}")

# Close the WebDriver
driver.quit()
