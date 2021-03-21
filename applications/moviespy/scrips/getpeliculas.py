from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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

        #all_cines = driver.

        def getMovieList(main_driver):
            time.sleep(5)
            caja = main_driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/section[5]/div/div')#
            movie_list = caja.find_elements_by_xpath('*')
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

        urls = []
        print('NUmero de peliculas: ', len(movie_list))
        for x in range(len(movie_list)+1):
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
            if img_src.find("belt_Preventa") == -1:
                actions = ActionChains(driver)
                print('Numero ', x)
                actions.click(on_element=boton).perform()
                urls.append(driver.current_url)
                print(driver.current_url)
                driver.back()
            else:
                driver.refresh()

        driver.quit()
        return urls