from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
MAIN_URL = 'https://www.techwithtim.net/'

driver = webdriver.Chrome(DRIVER_PATH)
driver.get(MAIN_URL)

link = driver.find_element_by_link_text("Python Programming")
link.click()

try:
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'poster'))
    )
    element.click()
    driver.back()
    driver.forward()

finally:
    driver.quit()



time.sleep(5)
driver.quit()