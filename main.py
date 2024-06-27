#Import webdriver and Options from selenium
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import Scrapers

#A function that allows for a page to load before attempting to interact with it
def page_load():
    WebDriverWait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete') 

#Recieves User Specific Information From Config.txt File
with open("config.txt", "r") as c:
    username = c.readline().split("=")[1].strip()
    password = c.readline().split("=")[1].strip()
    user = c.readline().split("=")[1].strip()
    profile_name = c.readline().split("=")[1].strip()
    url = c.readline().split("=")[1].strip()

#Directory for the Chrome Driver
chromeDriverPath = "C:\\SeleniumDrivers\\chromedriver.exe"

#Path of the chrome profile you want to use for login
user_data = "C:\\Users\\" + user + "\\AppData\\Local\\Google\\Chrome\\User Data\\" + profile_name

#Creates a webdriver entity with the specified requirments
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
options.add_argument("user-data-dir="+str(user_data))
options.add_argument("profile-directory="+str(profile_name))
service = Service(executable_path=chromeDriverPath)
driver = webdriver.Chrome(service=service, options=options)

#Opens the specefied url in the config.txt file
driver.get(url)

page_load()

#Mykonicaminolta Login process
username_field = driver.find_element(By.ID, "LoginPortletFormID")
username_field.send_keys(username)

password_field = driver.find_element(By.ID, "LoginPortletFormPassword")
password_field.send_keys(password)

login_button = driver.find_element(By.ID,"LoginPortletFormSubmit")
login_button.click()

#Locates the Service Dropdown Menu and Clicks it
dropdown = driver.find_element(By.XPATH, "//li[@class='dropdown']/a[@class='dropdown-toggle' and contains(text(), 'Service')]")
dropdown.click()

#Waits until dropdown Menu becomes visable #TODO: Find a work around in order to run this in headless mode
dropdown_menu_items = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, 'Service'))
)

#Clickes the Shared ServiceNow Link to transport to SNOW
shared_servicenow_link = dropdown_menu_items.find_element(By.LINK_TEXT, 'Shared ServiceNow')
shared_servicenow_link.click()

#Waits for SNOW to open before swapping to the window handle
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])

#A request prompt for the URL of the frame source of the task
task_frame_source = input("Please paste the frame source of the task you would like to scrape.\n")

#Removes the view source from the url to allow for scraping
driver.get(task_frame_source[12:])

page_load()

#TODO: Migrate to scrapers.py
soup = BeautifulSoup(driver.page_source, features="lxml")
input_element = soup.find_all('input', class_='questionsetreference form-control element_reference_input')

for value in input_element:
    input_value = value.get('value')
    # print(f"Value of the input elements: {input_value}")

Scrapers.nameScraper(soup)
Scrapers.sctaskScraper(soup)

#TODO:Fix this
script_tags = soup.find_all('script')
for value in script_tags:
    try:
        attention = value.find('input', {'id': 'sys_original.ni.VE64553651dbcfce1069ac819b1396197e'}).get("value").strip()
    except:
        print("no")


input("Press Enter to exit")
driver.quit()
