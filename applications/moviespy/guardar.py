from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .models import Funcion
from datetime import datetime

class Guardar():

    def guardarFunciones(urls_peliculas):
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

        # all_cines = driver.

        def getMovieList(main_driver):
            time.sleep(5)
            movie_list = main_driver.find_elements_by_xpath('//div[contains(@id,"getTicket_")]')
            return movie_list

        movie_list = getMovieList(driver)

        while len(movie_list) == 0:
            driver.refresh()
            time.sleep(5)
            movie_list = getMovieList(driver)

        busqueda = driver.find_element_by_id('cinemaBillboardSearch')
        busqueda.click()
        time.sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ENTER)
        time.sleep(1)

        # Variables que quiero

        nombre = ''
        sucursal = ''
        tipo_funcion = ''
        hora = ''
        sala = ''
        asientos = 0
        activo = True

        for u in urls_peliculas:
            urls = u

            driver.get(urls)
            actions = ActionChains(driver)
            time.sleep(20)
            actions.send_keys(Keys.SPACE).perform()
            movie_details = driver.find_elements_by_class_name('movie-details')
            while len(movie_details) == 0:
                driver.get(urls)
                time.sleep(5)
                movie_details = driver.find_elements_by_class_name('movie-details')
                time.sleep(5)
            nombre = movie_details[0].find_element_by_tag_name('h1').text
            # print('Title: ', movie_tittle)
            sucursales_box = driver.find_element_by_id('main-app')
            time.sleep(5)

            sucursales_box_ul = sucursales_box.find_element_by_tag_name('ul')
            sucursales_list = sucursales_box_ul.find_elements_by_tag_name('li')

            for x in range(3):
                box_li = sucursales_box_ul.find_element_by_xpath('//li[' + str(x + 1) + ']/div[1]/div[1]')
                sucursal = box_li.find_element_by_tag_name('h3').text
                # print(nombre_suc)
                # Me muevo a la caja donde estan las funciones
                fun_div = sucursales_box_ul.find_element_by_xpath('//li[' + str(x + 1) + ']/div[2]')
                # Obtengo las cajas individuales de las funciones
                individual_fun_box = fun_div.find_elements_by_xpath('*')
                # Itero cada caja por separado
                for individual in individual_fun_box:
                    if len(individual.find_elements_by_css_selector("*")) > 1:
                        nombres_horas_divs = individual.find_elements_by_xpath('*')
                        tipo_funcion = nombres_horas_divs[0].find_element_by_tag_name('span').text + '' + \
                                       nombres_horas_divs[
                                           0].find_element_by_tag_name('h5').text
                        horarios_div = nombres_horas_divs[2].find_elements_by_xpath('*')
                        for h in horarios_div:
                            f = Funcion()
                            hora = h.find_element_by_tag_name('label').text
                            f.pelicula = nombre
                            f.sucursal = sucursal
                            f.url_pelicula = urls
                            f.tipo_funcion = tipo_funcion
                            f.hora = hora
                            f.asientos = asientos
                            f.sala = sala
                            f.fecha = datetime.today()
                            f.activo = activo
                            f.save()

        driver.quit()