import os
from bs4 import BeautifulSoup
import requests
import csv

# Target URL
url = "https://elvi.lv/elvi-vakances/"  # Replace with the actual URL

# Send a GET request to the URL
response = requests.get(url)

# Check response status
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all containers
    containers = soup.find_all("div", class_="vakancies-container")

    # Create the output directory
    output_folder = os.path.join(os.path.dirname(__file__), "../outputs")  # Adjust the relative path if needed
    os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist

    # Define the CSV file path
    csv_file = os.path.join(output_folder, "elvi_jobs.csv")

    # Prepare CSV file
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(["Region", "Job Title", "Location", "Link"])

        # Process each container
        for container in containers:
            # Extract the region
            region = container.find("h2").text.strip()

            # Find all job items
            jobs = container.find_all("li")
            for job in jobs:
                try:
                    # Extract job details
                    job_title = job.find("h3").text.strip()
                    location = job.find("span").text.strip()
                    link = job.find("a")["href"]

                    # Write to CSV
                    writer.writerow([region, job_title, location, link])
                except Exception as e:
                    print(f"Error processing job: {e}")

    print(f"Scraping completed. Data saved to {csv_file}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
