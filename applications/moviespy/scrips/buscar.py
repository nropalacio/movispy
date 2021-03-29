from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from .comprobaciones.getcontenido import getMovieList, getMovieDetails, selectCine, selectFuncion, selectHora, getSeatList


class Buscar:
    
    def buscarFuncion(funsiones):

        ###########################################################
        DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
        MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'
        ###########################################################
        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(MAIN_URL)
        driver.maximize_window()
        actions = ActionChains(driver)
        img = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAtCAYAAADhoUi4AAAABHNCSVQICAgIfAhkiAAAAi9JREFUaEPtmktOwzAQhmfcx5Y62ZQVFReAHoEDIMQFgBugHgAJblBuUJbsegOKxBIhVmzhArW7pm0GTZRUTkhLQy0cwCNFlRJnPL/n87TyFKHAtNYtADgnojMA6BSNcXRviIjXUsrRsvkx/0BrvU9EdwDAoippRNQPw7BXFFxGEGeGiF6rLCYVgYg9KWU/LyojaDweDxDxNB1Ur9dBCFGJLBERzGYz4M/EJkEQyJWClFKcnXjPNBoNQPxEpHNx0+l0IQoRD/L7KROxUmohv9lsOg++KADOUhRF8SMiugrD8NIcFwtKqtoeES2qR61Wi8dxlqqAHaPG13w+N7EbIeIAAO6llG9xvFrrTlLVlpZnFsUIujLOCGdmhU2SIjFApdQQAI6+CtZVgeCs8L5Zw1hUlwVNAGCLX8ijlaY5fcaiftrM7DAp+UJlxshFggUtLQTm6rBYF4J4z/C1bFHNIuEF+QxZ2HAeOV8ULGBUxoVHziNXhhcLYz1yHjkLGJVx4ZHzyJXhxcJYj5xHzgJGZVx45DxyZXixMPZbyPHRkHEIbiEMNy7iUx+tNf0FMckSHmbO5dysq71Z+Tg4I6iqLZRVknPdiJtfL8jsFxGRF2QPeEue/leGqtqGXJXMogxxr2LtVnfVGsnmdygiXnCVewKAriWkXbqJEHGXfynwny1eAGDbZTQbzv0uhDhptVq3i7a+1noHAI4LHD9vOJm114UQ7SiK2qZDInoMguAhvfcBcs3yY6nLfpsAAAAASUVORK5CYII='





        movie_list = getMovieList(driver)
        while len(movie_list) == 0:
            driver.refresh()
            sleep(5)
            movie_list = getMovieList(driver)

        busqueda = driver.find_element_by_id('cinemaBillboardSearch')
        busqueda.click()
        sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ENTER)
        sleep(1)

        print('*****Seleciono todos los cines*****')
        for fun in funsiones:
            print('*****Incia nueva funcion*****')
            driver.get(fun.url_pelicula)
            actions = ActionChains(driver)
            sleep(3)
            try:
                print('*****Carga movie details*****')
                movie_details = getMovieDetails(driver)
                while len(movie_details) == 0:
                    print('*****No cargo intenta de nuevo*****')
                    #Regresa a la pagina porque esto lo manda a la pagina principal
                    driver.get(fun.url_pelicula)
                    actions = ActionChains(driver)
                    sleep(3)
                    #Vuelve a cargar las peliculas y repite el bucle
                    movie_details = getMovieDetails(driver)
                

                actions.send_keys(Keys.SPACE).perform()
                sleep(3)
                num_c = selectCine(driver, fun.sucursal.nombre)
                print('Probo este cine:', num_c)
                print('*****busco el cine*****')

                num_f = selectFuncion(driver, num_c, fun.tipo_funcion)
                print('Probo ests sucursal')
                print('*****busco la funcion*****')
                
                num_h = selectHora(driver, num_c, num_f, fun.hora)
                print('Probo esta hora')
                print('*****busco la hora*****')
               #'//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]'
                #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]/div['+ str(tipo_funcion)+']/label
                le_hora = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(num_c)+']/div[2]/div['+ str(num_f)+']/div[2]/div['+ str(num_h)+']/label')
                driver.execute_script("arguments[0].scrollIntoView(true);", le_hora)
                sleep(3)
                le_hora.click()
                boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'buyTickets')))
                print('Va al boton')
                driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                sleep(2)
                print('Llego al boton')
                boton.click()
                sleep(6)
                element = getSeatList(driver)
                
                ####################################################################
                
                asientos = element[0].find_elements_by_class_name("cell-container")
                conteo_hijos = []
                conteo = 0
                for asiento in asientos:
                    if len(asiento.find_elements_by_css_selector("*")) == 3 and len(asiento.find_elements_by_tag_name("img")) != 0 and asiento.find_element_by_tag_name("img").get_attribute("class") == "seat-disable":
                        conteo += 1
                    
#//*[@id="roomContainer"]/div/div[4]/div/div/div[70]/div/div/img
                print('guardo conteo')
                fun.asientos = conteo
                la_sala = driver.find_element_by_xpath('//*[@id="containerMovieDetail"]/div[4]/span').text#//*[@id="containerMovieDetail"]/div[4]/span
                print('guardo sala')
                fun.sala = la_sala[12:]
                fun.save()

                #//*[@id="roomContainer"]/div/div[4]/div/div
                #//*[@id="roomContainer"]/div/div[3]/div/div

            except Exception as e:
                print('Ocurrio un error durante el proceso', e)
                if fun.sala != '0':
                    print('No hay cambios')
                elif fun.sala == '':
                    fun.asientos = 0
                    fun.sala = '0'
                    fun.save()
                

        driver.quit()

    def buscarFuncionSanta(funsiones):

        ###########################################################
        DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
        MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'
        ###########################################################
        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(MAIN_URL)
        driver.maximize_window()
        actions = ActionChains(driver)
        img = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAtCAYAAADhoUi4AAAABHNCSVQICAgIfAhkiAAAAi9JREFUaEPtmktOwzAQhmfcx5Y62ZQVFReAHoEDIMQFgBugHgAJblBuUJbsegOKxBIhVmzhArW7pm0GTZRUTkhLQy0cwCNFlRJnPL/n87TyFKHAtNYtADgnojMA6BSNcXRviIjXUsrRsvkx/0BrvU9EdwDAoippRNQPw7BXFFxGEGeGiF6rLCYVgYg9KWU/LyojaDweDxDxNB1Ur9dBCFGJLBERzGYz4M/EJkEQyJWClFKcnXjPNBoNQPxEpHNx0+l0IQoRD/L7KROxUmohv9lsOg++KADOUhRF8SMiugrD8NIcFwtKqtoeES2qR61Wi8dxlqqAHaPG13w+N7EbIeIAAO6llG9xvFrrTlLVlpZnFsUIujLOCGdmhU2SIjFApdQQAI6+CtZVgeCs8L5Zw1hUlwVNAGCLX8ijlaY5fcaiftrM7DAp+UJlxshFggUtLQTm6rBYF4J4z/C1bFHNIuEF+QxZ2HAeOV8ULGBUxoVHziNXhhcLYz1yHjkLGJVx4ZHzyJXhxcJYj5xHzgJGZVx45DxyZXixMPZbyPHRkHEIbiEMNy7iUx+tNf0FMckSHmbO5dysq71Z+Tg4I6iqLZRVknPdiJtfL8jsFxGRF2QPeEue/leGqtqGXJXMogxxr2LtVnfVGsnmdygiXnCVewKAriWkXbqJEHGXfynwny1eAGDbZTQbzv0uhDhptVq3i7a+1noHAI4LHD9vOJm114UQ7SiK2qZDInoMguAhvfcBcs3yY6nLfpsAAAAASUVORK5CYII='

        movie_list = getMovieList(driver)
        while len(movie_list) == 0:
            driver.refresh()
            sleep(5)
            movie_list = getMovieList(driver)

        #Selecciono la sucursal de santa ana
        busqueda = driver.find_element_by_id('cityBillboardSearch')
        busqueda.click()
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ENTER)
        sleep(1)

        print('*****Seleciono todos los cines*****')

        for fun in funsiones:
            print('*****Incia nueva funcion*****')
            driver.get(fun.url_pelicula)
            actions = ActionChains(driver)
            sleep(5)
            try:
                print('*****Carga movie details*****')
                movie_details = getMovieDetails(driver)
                while len(movie_details) == 0:
                    print('*****No cargo intenta de nuevo*****')
                    #Regresa a la pagina porque esto lo manda a la pagina principal
                    driver.get(fun.url_pelicula)
                    actions = ActionChains(driver)
                    sleep(5)
                    #Vuelve a cargar las peliculas y repite el bucle
                    movie_details = getMovieDetails(driver)
                    
                actions.send_keys(Keys.SPACE).perform()
                sleep(2)
                print('*****Ya cargo ahora busca*****')
                num_f = selectFuncion(driver, 1, fun.tipo_funcion)
                print('*****Busca la funcion*****')
                
                num_h = selectHora(driver, 1, num_f, fun.hora)
                print('*****Busco la hora*****')
               #'//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]'
                #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]/div['+ str(tipo_funcion)+']/label
                le_hora = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div['+ str(num_f)+']/div[2]/div['+ str(num_h)+']/label')
                driver.execute_script("arguments[0].scrollIntoView(true);", le_hora)
                sleep(3)
                print('*****CLICK hora*****')
                le_hora.click()
                boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'buyTickets')))
                print('Va al boton')
                driver.execute_script("arguments[0].scrollIntoView(true);", boton)
                sleep(2)
                print('*****CLICK boton*****')
                boton.click()
                sleep(6)
                element = getSeatList(driver)
                ###################################################################
                ####################################################################
                print('Sera aqui')
                asientos = element[0].find_elements_by_class_name("cell-container")
                print('yyyy')
                conteo_hijos = []
                conteo = 0
                for asiento in asientos:
                    if len(asiento.find_elements_by_css_selector("*")) == 3 and len(asiento.find_elements_by_tag_name("img")) != 0 and asiento.find_element_by_tag_name("img").get_attribute("class") == "seat-disable":
                        conteo += 1

                print('*****GUARDA CONTEO*****')            
                fun.asientos = conteo
                la_sala = driver.find_element_by_xpath('//*[@id="containerMovieDetail"]/div[4]/span').text#//*[@id="containerMovieDetail"]/div[4]/span
                print('*****GUARDA LA SALA*****')
                fun.sala = la_sala[12:]
                fun.save()

                #//*[@id="roomContainer"]/div/div[4]/div/div
                #//*[@id="roomContainer"]/div/div[3]/div/div

            except Exception as e:
                print('Ocurrio un error durante el proceso', e)
                if fun.sala != '0':
                    print('No hay cambios')
                elif fun.sala == '':
                    fun.asientos = 0
                    fun.sala = '0'
                    fun.save()

        driver.quit()





        