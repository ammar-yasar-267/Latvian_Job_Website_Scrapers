import os
from bs4 import BeautifulSoup
import requests
import csv

# Target URL
url = "https://ikealatvia.teamtailor.com/jobs"  # Replace with the actual URL

# Send a GET request to the URL
response = requests.get(url)

# Check response status
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the jobs container
    jobs_list = soup.find("ul", id="jobs_list_container")
    jobs = jobs_list.find_all("li", class_="w-full")

    # Create the output directory
    output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path if needed
    os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

    # Define the CSV file path
    csv_file = os.path.join(output_folder, "ikea_jobs.csv")

    # Prepare CSV file
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Job Title", "Department", "Location", "Link"])

        # Extract data for each job
        for job in jobs:
            try:
                # Job title
                title = job.find("span", class_="text-block-base-link").get("title").strip()

                # Department and location
                details = job.find("div", class_="mt-1 text-md").find_all("span")
                department = details[0].text.strip() if len(details) > 0 else "N/A"
                location = details[-1].text.strip() if len(details) > 1 else "N/A"

                # Job link
                link = job.find("a")["href"].strip()

                # Write to CSV
                writer.writerow([title, department, location, link])
            except Exception as e:
                print(f"Error processing job: {e}")

    print(f"Scraping completed. Data saved to {csv_file}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
