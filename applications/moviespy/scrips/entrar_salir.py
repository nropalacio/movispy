from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'

# Cargar el driver
driver = webdriver.Chrome(DRIVER_PATH)

# Abrir pagina principal
driver.get(MAIN_URL)

# Maximizar la pagina
driver.maximize_window()

# Cargo el paquete actions, que me permite presionar comandos
actions = ActionChains(driver)
time.sleep(10)

driver.execute_script("document.getElementById('getTicket_2948').scrollIntoView();")

  
driver.quit()
