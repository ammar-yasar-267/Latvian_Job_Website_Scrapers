import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Initialize the WebDriver
driver = webdriver.Chrome()  # Or specify the path if needed
driver.get("https://vakances.maxima.lv/jobs")

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

# Save to a CSV file
df = pd.DataFrame(jobs_list)
df.to_csv("maxima_jobs.csv", index=False)
print("Job data has been saved to maxima_jobs.csv")

# Close the WebDriver
driver.quit()
