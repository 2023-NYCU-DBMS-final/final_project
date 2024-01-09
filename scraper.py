import selenium
from selenium import webdriver
import os
import pathlib
import time

path = os.path.join(pathlib.Path(__file__).parent.absolute(),"tmp")
if not os.path.exists(path):
    os.mkdir(path)
else:
    for file in os.listdir(path):
        os.remove(os.path.join(path,file))
    os.rmdir(path)
    os.mkdir(path)
options = webdriver.EdgeOptions()
prefs = {"download.default_directory": path,
         "disable-popup-blocking": True}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Edge(options=options)
driver.get("https://data.moenv.gov.tw/dataset/detail/AQX_P_432")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
while True:
    try:
        driver.find_element("xpath", "//button[@id='bpa-dropdown-filter-data-btn']").click()
        break
    except selenium.common.exceptions.ElementClickInterceptedException:
        #scroll up 20px
        driver.execute_script("window.scrollTo(0, window.scrollY - 50)")
driver.find_element("id", "bpa-dropdown-filter-data-option-0").click()
time.sleep(1)
os.rename(os.path.join(path,"Preview_Data.csv"), os.path.join(path,"current.csv"))
driver.close()