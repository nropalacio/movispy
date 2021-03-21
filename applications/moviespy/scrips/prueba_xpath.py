from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from ..models import Funcion, Sucursal, Dia
from datetime import datetime

class LocalizarHorasSalas():

    

    def iniciar(urls, dia):
        
        def getMovieDetails(driver):
            movie_details = driver.find_elements_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[1]/div/h3')
            return movie_details

        def getMovieList(main_driver):
            sleep(5)
            movie_list = main_driver.find_elements_by_xpath('//div[contains(@id,"getTicket_")]')
            return movie_list 

        l_funciones = []

        ###########################################################
        DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
        MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'
        ###########################################################
        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(MAIN_URL)
        driver.maximize_window()
        actions = ActionChains(driver)
        ###########################################################
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
        #Asi se evalua por cada cine
        #  Cinépolis Galerías -1
        # MiCine Multiplaza Panamericana - 2
        # Cinépolis VIP Galerías - 3
        for url in urls:
            #Va a la url
            print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*-*-*-*-*-*-*-')
            driver.get(url)
            actions = ActionChains(driver)
            sleep(5)
            g_url = url
            #Obtengo la caja de movie details, si no esta llena da cero
            movie_details = getMovieDetails(driver)
            while len(movie_details) == 0:
                #Regresa a la pagina porque esto lo manda a la pagina principal
                driver.get(url)
                actions = ActionChains(driver)
                sleep(5)
                #Vuelve a cargar las peliculas y repite el bucle
                movie_details = getMovieDetails(driver)

                #Ahora si, voy a dar un salto para verificar que este donde quiero
            actions.send_keys(Keys.SPACE).perform()

            for x in range(3):
                print('###########################################')
                print('Inicia la busqueda para el cine, ', str(x+1))
                print('###########################################')   
                #Me muevo a main app
                main_app = driver.find_element_by_id('main-app')

                #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[1]/h1
                g_peli = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[1]/h1').text
                #Me muevo a la caja de las funciones
                nombre_cine = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(x+1)+']/div[1]/div[1]/h3').text
                print(nombre_cine)
                g_sucursal = Sucursal.objects.get(nombre = nombre_cine)
                #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li[2]/div[1]/div[1]/h3
                cine_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(x+1)+']/div[2]')
                #Cuento el contenido de la caja, asi sabre si hay funciones disponibles
                fun_num = cine_box.find_elements_by_xpath('*')
                contenido = fun_num[0].find_elements_by_css_selector("*")

                #Verifico si hay funciones
                if len(contenido) > 1:
                    #Va a iterar dependiendo del numero de funciones
                    for f in range(len(fun_num)):
                        #Me muevo a la caja indicada
                        main_app = driver.find_element_by_id('main-app')
                        box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(x+1)+']/div[2]/div['+ str(f+1)+']')
                        tipo_funcion_t = box.find_element_by_tag_name('span').text + '' + box.find_element_by_tag_name('h5').text
                        print(tipo_funcion_t)
                        #Me muevo a la caja de los horarios
                        horario_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(x+1)+']/div[2]/div['+ str(f+1)+']/div[2]')
                        #Obtengo el contenido de la caja
                        horario_contenido = horario_box.find_elements_by_xpath("*")
                        print('Horario contenido')
                        print(len(horario_contenido))
                        for h in range(len(horario_contenido)):
                            main_app = driver.find_element_by_id('main-app')
                            hora_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(x+1)+']/div[2]/div['+ str(f+1)+']/div[2]/div['+ str(h+1) +']')
                            hora = hora_box.find_element_by_tag_name('label').text
                            print(hora)
                            fn = Funcion()
                            fn.sucursal = g_sucursal
                            print('ok')
                            fn.fecha = dia
                            print('ok')
                            fn.pelicula = g_peli
                            print('ok')
                            fn.url_pelicula = g_url
                            print('ok')
                            fn.tipo_funcion = tipo_funcion_t
                            print('ok')
                            fn.hora = hora
                            print('ok')
                            fn.sala = ''
                            print('ok')
                            fn.asientos = 0
                            print('ok')
                            fn.activo = True
                            print('ok')

                            l_funciones.append(fn)
                #Espero un poco antes
                
                #Ahora si, voy a dar un salto para verificar que este donde quiero
                #actions.send_keys(Keys.SPACE).perform()
        sleep(5)
        print('Llego al final')
        driver.quit()

        return l_funciones

#main_app = driver.find_element_by_id('main-app')
#cine_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div[1]/div[2]/div['+ str(x+1)+']')

