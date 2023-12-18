from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import csv

# Path to your GeckoDriver executable
webdriver_service = Service('./geckodriver')

# URL of the website
# EHV-NRW Regionalliga Schedule
url = 'https://ehv-nrw.de/leagues/league/sen/rlw/81/'  # Replace this with the URL of the website you want to scrape

# Configure Firefox options
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)

# Create a new instance of Firefox
driver = webdriver.Firefox(service=webdriver_service, options=options)

# Load the webpage
driver.get(url)

# Wait for the table to be loaded (you may need to adjust the waiting time)
driver.implicitly_wait(10)  # Waits for 10 seconds

try:
    # Find the table rows
    rows = driver.find_elements(
        By.XPATH,
        "//div[contains(@class, '-hd-los-schedule-table')]//table//tbody//tr"
    )

    if rows:
        # Create and open a CSV file in write mode
        with open('table_data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the content of each row to the CSV file
            for row in rows:
                # Find cells within each row
                cells = row.find_elements(By.XPATH, './/td')

                # Get the text content of each cell and write to the CSV file
                row_data = [cell.text.strip() for cell in cells]
                csv_writer.writerow(row_data)

        print('Table rows successfully written to table_data.csv')
    else:
        print('Table rows not found.')
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Close the browser
driver.quit()
