from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('/home/rodrigo/web_drivers/chromedriver')
driver.get('https://www.techwithtim.net/')
print(driver.title)
search = driver.find_element_by_name('s')
search.send_keys('test')
search.send_keys(Keys.RETURN)


try:
    algo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main"))
    )
    articles = algo.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name('entry-title')
        print(header.text)

finally:
    driver.quit()

driver.quit()
