from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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

#all_cines = driver.

time.sleep(5)
busqueda = driver.find_element_by_id('cinemaBillboardSearch')
busqueda.click()
time.sleep(3)
print('pasaron 3 segundos')
busqueda.send_keys(Keys.ARROW_DOWN)
time.sleep(3)
print('pasaron 3 segundos')
busqueda.send_keys(Keys.ENTER)
time.sleep(3)


def getMovieList(main_driver):
    time.sleep(5)
    movie_list = main_driver.find_elements_by_xpath('//div[contains(@id,"getTicket_")]')
    return movie_list

movie_list = getMovieList(driver)
number_movies = len(movie_list)
urls_movies = []
for x in range(number_movies):
    print('****1****')
    movie_list = getMovieList(driver)
    while len(movie_list) == 0:
        print('****2****')
        driver.refresh()
        time.sleep(10)
        movie_list = getMovieList(driver)
        time.sleep(5)


    actions = ActionChains(driver)
    time.sleep(5)
    actions.send_keys(Keys.SPACE).perform()
    time.sleep(3)
    boton = movie_list[x].find_element_by_class_name('poster')
    actions = ActionChains(driver)
    print('Numero ', x)
    actions.click(on_element=boton).perform()
    urls_movies.append(driver.current_url)
    driver.back()

time.sleep(5)
print('Obtencion de datos')

for urls in urls_movies:
    driver.get(urls)
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
        time.sleep(2)
        horarios_box = sucursal.find_elements_by_xpath('//div[@class="d-flex flex-wrap"]')
        time.sleep(2)
        contador = 0
        for funcion in funciones_box:
            funcion_name = funcion.find_element_by_tag_name('span').text + ' ' + funcion.find_element_by_tag_name('h5').text
            print('Funcion: ', funcion_name)
            individual_horarios = horarios_box[contador].find_elements_by_xpath('//div[@class="d-flex mr-2 radio-group-cnpls  mt-3"]')
            horarios = []
            for horario in individual_horarios:
                time.sleep(2)
                horarios.append(horario.find_element_by_tag_name('label').text)
                time.sleep(2)
            print('Horarios: ', horarios)

print(urls_movies)