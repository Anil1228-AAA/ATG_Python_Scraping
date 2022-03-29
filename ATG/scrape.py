import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

import os


os.environ['PATH'] += r"C:\\chromedriver_win32"
driver = webdriver.Chrome()

url = 'https://www.careerguide.com/career-options'
driver.get(url)
time.sleep(3)

title = driver.find_elements(by=By.XPATH, value='//div[@class="c-body"]/div[8]/div[1]/ul/li')
print(title)
print(len(title))

dict = {'job_title': []}

for i in range(len(title)):
    dict['job_title'].append(title[i].text)

df = pd.DataFrame(dict)
df.to_csv('careerGuide.csv')

driver.quit()


