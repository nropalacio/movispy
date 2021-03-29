from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from .comprobaciones.getcontenido import getMovieList, getMovieDetails, selectCine, selectFuncion, selectHora, getSeatList


class BuscarSanta:
    
    def buscarFuncion(funsiones):

        ###########################################################
        DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
        MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'
        ###########################################################
        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(MAIN_URL)
        driver.maximize_window()
        actions = ActionChains(driver)

        movie_list = getMovieList(driver)
        while len(movie_list) == 0:
            driver.refresh()
            sleep(5)
            movie_list = getMovieList(driver)

        #Selecciono la sucursal de santa ana
        busqueda = driver.find_element_by_id('cityBillboardSearch')
        busqueda.click()
        sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        print('pasaron 3 segundos')
        busqueda.send_keys(Keys.ENTER)
        sleep(1)

        for fun in funsiones:
            driver.get(fun.url_pelicula)
            actions = ActionChains(driver)
            sleep(5)
            try:
                movie_details = getMovieDetails(driver)
                while len(movie_details) == 0:
                    #Regresa a la pagina porque esto lo manda a la pagina principal
                    driver.get(fun.url_pelicula)
                    actions = ActionChains(driver)
                    sleep(5)
                    #Vuelve a cargar las peliculas y repite el bucle
                    movie_details = getMovieDetails(driver)
                
                
                num_f = selectFuncion(driver, 1, fun.tipo_funcion)
                print('Probo ests sucursal')
                
                num_h = selectHora(driver, 1, num_f, fun.hora)
                print('Probo esta hora')
               #'//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]'
                #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]/div['+ str(tipo_funcion)+']/label
                le_hora = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div['+ str(num_f)+']/div[2]/div['+ str(num_h)+']/label')
                driver.execute_script("arguments[0].scrollIntoView(true);", le_hora)
                sleep(5)
                le_hora.click()
                print('Le dio click a la hoa')
                boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'buyTickets')))
                print('Llego al boton')
                boton.click()
                sleep(5)
                element = getSeatList(driver)
                ###################################################################
                
                while len(element) == 0:
                    driver.get(fun.url_pelicula)
                    actions = ActionChains(driver)
                    sleep(5)
                    movie_details = getMovieDetails(driver)
                    while len(movie_details) == 0:
                        #Regresa a la pagina porque esto lo manda a la pagina principal
                        driver.get(fun.url_pelicula)
                        actions = ActionChains(driver)
                        sleep(5)
                        #Vuelve a cargar las peliculas y repite el bucle
                        movie_details = getMovieDetails(driver)

                    le_hora = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div['+ str(num_f)+']/div[2]/div['+ str(num_h)+']/label')
                    driver.execute_script("arguments[0].scrollIntoView(true);", le_hora)
                    sleep(5)
                    le_hora.click()
                    print('Le dio click a la hoa')
                    boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'buyTickets')))
                    print('Llego al boton')
                    boton.click()
                    sleep(5)
                    element = getSeatList(driver)
                
                ####################################################################
                
                print('Sera aqui')
                asientos = element[0].find_elements_by_class_name("cell-container")
                print('yyyy')
                conteo_hijos = []
                conteo = 0
                for asiento in asientos:
                    if len(asiento.find_elements_by_css_selector("*")) == 3 and len(asiento.find_elements_by_tag_name("img")) != 0 and asiento.find_element_by_tag_name("img").get_attribute("class") == "seat-disable":
                        conteo += 1
                                        
                fun.asientos = conteo
                la_sala = driver.find_element_by_xpath('//*[@id="containerMovieDetail"]/div[4]/span').text#//*[@id="containerMovieDetail"]/div[4]/span
                fun.sala = la_sala[12:]
                fun.save()

                #//*[@id="roomContainer"]/div/div[4]/div/div
                #//*[@id="roomContainer"]/div/div[3]/div/div

            except Exception as e:
                print('Ocurrio un error durante el proceso', e)
                fun.asientos = 0
                fun.sala = 'Sin sala'
                fun.save()

        driver.quit()





        