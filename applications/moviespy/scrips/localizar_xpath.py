from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from datetime import datetime

class Localizar():


    def iniciar():

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

        return driver, actions

    def moverSucursal(driver, sucursal):

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
        cine = ''
        if sucursal == 1:
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ENTER)
            time.sleep(1)
            cine = 'Cinépolis Galerías'
        elif sucursal == 2:
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ENTER)
            time.sleep(1)
            cine = 'MiCine Multiplaza Panamericana'
        elif sucursal == 3:
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ARROW_DOWN)
            time.sleep(1)
            busqueda.send_keys(Keys.ENTER)
            time.sleep(1)
            cine = 'Cinépolis VIP Galerías'
        
        return cine

    def obtenerDatos(urls):
        
        ########################
        def moverSucursal(driver, sucursal):

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
            cine = ''
            if sucursal == 1:
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ENTER)
                time.sleep(1)
                cine = 'Cinépolis Galerías'
            elif sucursal == 2:
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ENTER)
                time.sleep(1)
                cine = 'MiCine Multiplaza Panamericana'
            elif sucursal == 3:
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                busqueda.send_keys(Keys.ENTER)
                time.sleep(1)
                cine = 'Cinépolis VIP Galerías'
        
            return cine

        ######################
        
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



        for x in range(3):
            print('##############################')
            print('###### Print funcion, ', str(x))
            print('##############################')
            driver.get(MAIN_URL)
        # Maximizar la pagina
            driver.maximize_window()
        # Cargo el paquete actions, que me permite presionar comandos
            actions = ActionChains(driver)


            cine = moverSucursal(driver, x+1)
            print('Cine: ', cine)
            print('-------------')
            for url in urls:
                driver.get(url)
                actions = ActionChains(driver)
                time.sleep(5)
                movie_details = driver.find_elements_by_class_name('movie-details')
                while len(movie_details) == 0:
                    driver.get(url)
                    time.sleep(5)
                    movie_details = driver.find_elements_by_class_name('movie-details')
                
                actions.send_keys(Keys.SPACE).perform()
                
                nombre = movie_details[0].find_element_by_tag_name('h1').text
                print('Pelicula: ', nombre)
                print('-------------')
                
                sucursales_box = driver.find_element_by_id('main-app')
                ##time.sleep(5)
                sucursales_box_ul = sucursales_box.find_element_by_tag_name('ul')
                time.sleep(5)

                box_li = sucursales_box_ul.find_element_by_xpath('//li[1]/div[1]/div[1]')
                sucursal = box_li.find_element_by_tag_name('h3').text
                fun_div = sucursales_box_ul.find_element_by_xpath('//li[1]/div[2]')
                # Obtengo las cajas individuales de las funciones
                individual_fun_box = fun_div.find_elements_by_xpath('*')
                num_funciones = len(individual_fun_box)
                # Itero cada caja por separado
                cont_fun = 0
                cont_hor = 0
                for individual in individual_fun_box:
                    if len(individual.find_elements_by_css_selector("*")) > 1:
                        cont_fun += 1
                        nombres_horas_divs = individual.find_elements_by_xpath('*')
                        tipo_funcion = nombres_horas_divs[0].find_element_by_tag_name('span').text + '' + nombres_horas_divs[0].find_element_by_tag_name('h5').text
                        print('Funcion #: ', str(cont_fun), ' - ', tipo_funcion)
                        print('-------------')
                        horarios_div = nombres_horas_divs[2].find_elements_by_xpath('*')
                        for h in horarios_div:
                            cont_hor += 1
                            hora = h.find_element_by_tag_name('label').text
                            print('HOra #: ', str(cont_hor), ' - ', hora)

        driver.quit()


        #######################################################Termina
       
    
    
    