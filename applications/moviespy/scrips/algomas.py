from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
MAIN_URL = 'https://www.cinepolis.com.sv/peliculas/tom-y-jerry'

# Cargar el driver
driver = webdriver.Chrome(DRIVER_PATH)

driver.get(MAIN_URL)
actions = ActionChains(driver)


# Maximizar la pagina
driver.maximize_window()

#all_cines = driver.

time.sleep(10)
busqueda = driver.find_element_by_id('cinemaBillboardSearch')
busqueda.click()
time.sleep(3)
print('pasaron 3 segundos')
busqueda.send_keys(Keys.ARROW_DOWN)
time.sleep(3)
print('pasaron 3 segundos')
busqueda.send_keys(Keys.ENTER)
time.sleep(3)


driver.get(MAIN_URL)
actions = ActionChains(driver)




time.sleep(20)
actions.send_keys(Keys.SPACE).perform()
movie_details = driver.find_elements_by_class_name('movie-details')
while len(movie_details) == 0:
    driver.refresh()
    time.sleep(10)
    movie_details = driver.find_elements_by_class_name('movie-details')
    time.sleep(5)
movie_tittle = movie_details[0].find_element_by_tag_name('h1').text
print('Title: ', movie_tittle)
sucursales_box = driver.find_element_by_id('main-app')
time.sleep(5)
sucursales_box_ul = sucursales_box.find_element_by_tag_name('ul')
sucursales_list = sucursales_box_ul.find_elements_by_tag_name('li')
for sucursal in sucursales_list:
    sucursal_name = sucursal.find_element_by_tag_name('h3').text
    print('Sucursal: ', sucursal_name)
    funciones_box = sucursal.find_elements_by_xpath('//div[@class="d-flex mt-3"]')
    print(len(funciones_box))
    horarios_box = sucursal.find_elements_by_xpath('//div[@class="d-flex flex-wrap"]')
    print(len(horarios_box))
driver.quit()

