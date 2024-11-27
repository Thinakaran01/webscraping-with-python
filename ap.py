from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time


# Scraping the second website
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

# Wait for the bus items container to load
container2 = WebDriverWait(driver2, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'bus-items'))
)

# Extract bus details
products2 = container2.find_elements(By.XPATH, './div')
for product2 in products2:
    try:
        bus_name.append(product2.find_element(By.XPATH, "//div[contains(@class,'travels')]").text)
        bus_type.append(product2.find_element(By.XPATH, "//div[contains(@class,'bus-type')]").text)
        departing_time.append(product2.find_element(By.XPATH, "//div[contains(@class,'dp-time')]").text)
        duration.append(product2.find_element(By.XPATH, "//div[contains(@class,'dur l-color lh-24')]").text)
        reaching_time.append(product2.find_element(By.XPATH, "//div[contains(@class,'bp-time')]").text)
        star_rating.append(product2.find_element(By.XPATH, "//div[contains(@class,'rating-sec')]").text)
        price.append(product2.find_element(By.XPATH, "//div[contains(@class,'fare d-block')]").text)
        seat_availability.append(product2.find_element(By.XPATH, "//div[contains(@class,'seat-left')]").text)
    except Exception as e:
        print(f"Error extracting bus info: {e}")

# Save bus data to CSV if we have any bus information
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
    df_routes1.to_csv('routesinfo.csv', index=False)
    print("Bus data has been saved to 'routesinfo.csv'.")
else:
    print("No bus information found.")

# Close the second browser
driver2.quit()

