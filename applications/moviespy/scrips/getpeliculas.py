from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from .comprobaciones.getcontenido import getMovieList

class ObtenerPeliculas():

    def printNombres():

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

        movie_list = getMovieList(driver)

        while len(movie_list) == 0:
            driver.get(MAIN_URL)
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

        urls = []
        print('NUmero de peliculas: ', len(movie_list))
        for x in range(len(movie_list)):
            print('****1****')
            movie_list = getMovieList(driver)
            while len(movie_list) == 0:
                print('****2****')
                driver.refresh()
                time.sleep(5)
                movie_list = getMovieList(driver)

            actions = ActionChains(driver)
            time.sleep(5)
            actions.send_keys(Keys.SPACE).perform()
            boton = movie_list[x].find_element_by_class_name('poster')
            img_src = boton.find_element_by_tag_name('img').get_attribute('src')
            actions = ActionChains(driver)
            print('Numero ', x)
            actions.click(on_element=boton).perform()
            urls.append(driver.current_url)
            print(driver.current_url)
            driver.back()
           

        driver.quit()
        return urls