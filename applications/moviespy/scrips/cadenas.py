from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
MAIN_URL = 'https://orteil.dashnet.org/cookieclicker/'

driver = webdriver.Chrome(DRIVER_PATH)
driver.get(MAIN_URL)


driver.implicitly_wait(10)

cookie = driver.find_element_by_id('bigCookie')
cookie_count = driver.find_element_by_id("cookies")
items = [driver.find_element_by_id("productPrice" + str(i) for i in range(1, -1, -1))]
actions = ActionChains(driver)
actions.click(cookie)

for i in range(5000):
    actions.perform()