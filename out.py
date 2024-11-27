from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode if desired

# Initialize the WebDriver with the correct path and options
service = Service(ChromeDriverManager().install())

driver2 = webdriver.Chrome(service=service, options=chrome_options)
website2 = 'https://www.redbus.in/bus-tickets/hyderabad-to-vijayawada?fromCityId=124&toCityId=134&fromCityName=Hyderabad&toCityName=Vijayawada&busType=Any&onward=27-Nov-2024'
driver2.get(website2)
driver2.maximize_window()

# Initialize lists to store bus details
bus_name = []
bus_type = []
departing_time = []
duration = []
reaching_time = []
star_rating = []
price = []
seat_availability = []


# Function to extract bus details from the current page
def extract_bus_details():
    # Wait for the bus items container to load
    container2 = WebDriverWait(driver2, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'bus-items'))
    )

    # Extract bus details from the current page
    products2 = container2.find_elements(By.XPATH,
                                         './/div[@class="clearfix bus-item-details"]')  # Updated XPath to match bus containers

    for product2 in products2:
        try:
            # Extracting each bus's details using relative XPath
            bus_name.append(
                product2.find_element(By.XPATH, ".//div[contains(@class,'travels')]").text if product2.find_element(
                    By.XPATH, ".//div[contains(@class,'travels')]") else '')
            bus_type.append(
                product2.find_element(By.XPATH, ".//div[contains(@class,'bus-type')]").text if product2.find_element(
                    By.XPATH, ".//div[contains(@class,'bus-type')]") else '')
            departing_time.append(
                product2.find_element(By.XPATH, ".//div[contains(@class,'dp-time')]").text if product2.find_element(
                    By.XPATH, ".//div[contains(@class,'dp-time')]") else '')
            duration.append(product2.find_element(By.XPATH,
                                                  ".//div[contains(@class,'dur l-color lh-24')]").text if product2.find_element(
                By.XPATH, ".//div[contains(@class,'dur l-color lh-24')]") else '')
            reaching_time.append(
                product2.find_element(By.XPATH, ".//div[contains(@class,'bp-time')]").text if product2.find_element(
                    By.XPATH, ".//div[contains(@class,'bp-time')]") else '')
            star_rating.append(
                product2.find_element(By.XPATH, ".//div[contains(@class,'rating-sec')]").text if product2.find_element(
                    By.XPATH, ".//div[contains(@class,'rating-sec')]") else '')
            price.append(product2.find_element(By.XPATH,
                                               ".//div[contains(@class,'fare d-block')]").text if product2.find_element(
                By.XPATH, ".//div[contains(@class,'fare d-block')]") else '')
            seat_availability.append(
                product2.find_element(By.XPATH, ".//div[contains(@class,'seat-left')]").text if product2.find_element(
                    By.XPATH, ".//div[contains(@class,'seat-left')]") else '')
        except Exception as e:
            print(f"Error extracting bus info: {e}")


# Initial extraction from the first loaded page
extract_bus_details()

# Scroll the page until all buses are loaded
last_height = driver2.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for the new buses to load after the scroll
    time.sleep(1)  # Wait for 2 seconds to allow new data to load

    # Extract the newly loaded bus details
    extract_bus_details()

    # Get the new height of the page
    new_height = driver2.execute_script("return document.body.scrollHeight")

    # Break the loop if we have scrolled to the bottom of the page (no more new data)
    if new_height == last_height:
        break

    # Update the last height for the next iteration
    last_height = new_height

# Create a pandas DataFrame with the extracted data
if bus_name:
    df_routes1 = pd.DataFrame({
        'Bus_name': bus_name,
        'Bus_type': bus_type,
        'Departing_time': departing_time,
        'Duration': duration,
        'Reaching_time': reaching_time,
        'Star_rating': star_rating,
        'Price': price,
        'Seat_availability': seat_availability
    })

    # Remove duplicates based on bus_name and other columns to avoid repetitions
    df_routes1 = df_routes1.drop_duplicates()

    # Perform data cleaning (if necessary)
    # Example: Strip extra spaces from all columns
    df_routes1 = df_routes1.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Drop rows with any NaN values
    df_routes1 = df_routes1.dropna()

    # Save the data to a CSV file
    df_routes1.to_csv('routesinfo.csv', index=False)
    print("Bus data has been saved to 'routesinfo.csv'.")
else:
    print("No bus information found.")

# Close the browser
driver2.quit()
