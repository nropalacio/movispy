from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime

###########################################################
DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
MAIN_URL = 'https://www.cinepolis.com.sv/peliculas/godzilla-vs-kong'
###########################################################
driver = webdriver.Chrome(DRIVER_PATH)
driver.get(MAIN_URL)
driver.maximize_window()
actions = ActionChains(driver)

shortDate = datetime.today().strftime('%d')
print(shortDate)
sleep(5)
dia = driver.find_element_by_xpath('//*[@id="date"]/div/div[1]/div/label/div[2]/div/div/div[2]/span').text
print('dia: ', dia)
driver.quit()