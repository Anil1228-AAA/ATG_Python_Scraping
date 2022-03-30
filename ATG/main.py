import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import requests


os.environ['PATH'] += r"C:/chromedriver_win32"
driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')
driver.maximize_window()
time.sleep(3)


# For Login into LinkedIn
username = driver.find_element(by=By.ID, value="session_key")
username.send_keys("anil1999.aaak1228@gmail.com")
password = driver.find_element(by=By.ID, value="session_password")
password.send_keys("Your_Password")
time.sleep(2)


# Submit Button click
login_button = driver.find_element(by=By.CLASS_NAME, value="sign-in-form__submit-button")
login_button.click()
time.sleep(2)


driver.get("https://www.linkedin.com/jobs/search")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Creating empty Python Dictionary
dictn = {'job_title': [], 'company': [], 'location': []}
titles = driver.find_elements(by=By.XPATH, value="//div[@class='full-width artdeco-entity-lockup__title ember-view']/a")
company = driver.find_elements(by=By.XPATH, value="//div[@class='artdeco-entity-lockup__subtitle ember-view']/a")
location = driver.find_elements(by=By.XPATH, value='//div[@class="artdeco-entity-lockup__caption ember-view"]/ul/li[1]')

# Store data into Python Dictionary
index = min(len(titles),len(company),len(location))
print(index)
for i in range(index):
    dictn['job_title'].append(titles[i].text)
    dictn['company'].append(company[i].text)
    dictn['location'].append(location[i].text)

# Creating CSV file using Pandas 
df = pd.DataFrame(dictn)
df.to_csv('job_details.csv')


# Below code for fetching Companies data

time.sleep(2)

# Storing URL of Same Companies to get Data
links = []
for a in driver.find_elements(by=By.XPATH, value='//div[@class="mr1 artdeco-entity-lockup__image artdeco-entity-lockup__image--type-square ember-view"]/a'):
    # print(a.get_attribute('href'))
    links.append(a.get_attribute('href'))



dict1 = {"description": [], "location":[], "no._of_employee": []}
for link in links:
    source = requests.get(link)

    try:
        driver.get(link)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 900)")
        time.sleep(2)
        dict1["description"].append(driver.find_element(by=By.XPATH, value='//div[@class="jobs-company__box"]/p/div').text)
        dict1["no._of_employee"].append(driver.find_element(by=By.XPATH, value='//span[1][@class="jobs-company__inline-information"]').text)
        dict1["location"].append(driver.find_element(by=By.CLASS_NAME, value='jobs-unified-top-card__bullet').text)
    except:
        print("URL not found")

# Creating CSV file using Pandas 
df = pd.DataFrame(dict1)
df.to_csv('company_details.csv')       
