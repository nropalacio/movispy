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
from .comprobaciones.getcontenido import getMovieDetails, getMovieList

class LocalizarHorasSalasSantaAna():

    

    def iniciar(urls, dia):

        l_funciones = []

        ###########################################################
        DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
        MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'
        ###########################################################

        driver = webdriver.Chrome(DRIVER_PATH)
        driver.get(MAIN_URL)
        driver.maximize_window()
        actions = ActionChains(driver)
        

        #Aqui confirma que los datos de la pagina de cartelera cargaron
        #Para poder seleccionar el cine
        movie_list = getMovieList(driver)
        while len(movie_list) == 0:
            driver.get(MAIN_URL)
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



        #Va a ejecutar la busqueda por cada url obtenida
        for url in urls:
            #Carga la url
            driver.get(url)
            #Carga el actions para realizar acciones
            actions = ActionChains(driver)
            sleep(5)
            #Se asigna la url
            g_url = url



            #Igual, verifico si se cargaron los datos si no se recarga la pagina
            movie_details = getMovieDetails(driver)
            while len(movie_details) == 0:
                #Carga la url de nuevo
                driver.get(url)
                #Carga actios
                actions = ActionChains(driver)
                sleep(5)
                #Vuelve a cargar las peliculas y repite el bucle
                movie_details = getMovieDetails(driver)


            if driver.find_element_by_xpath('//*[@id="date"]/div/div[1]/div/label/div[2]/div/div/div[2]/span').text == datetime.today().strftime('%d'):
                #Ahora si, voy a dar un salto para verificar que este donde quiero
                actions.send_keys(Keys.SPACE).perform()

                
                #Me muevo a main app
                main_app = driver.find_element_by_id('main-app')

                #Obtengo el titulo de la pelicula
                g_peli = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[1]/h1').text
                
                
                #PASO X
                
                #Me muevo a la caja de las funciones
                nombre_cine = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[1]/div[1]/h3').text
                print(nombre_cine)

                #Obtengo el nombre de la sucursal
                g_sucursal = Sucursal.objects.get(id = 4)
                
                #PASO X
                cine_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]')
                #Cuento el contenido de la caja, asi sabre si hay funciones disponibles
                fun_num = cine_box.find_elements_by_xpath('*')
                contenido = fun_num[0].find_elements_by_css_selector("*")

                #Verifico si hay funciones
                if len(contenido) > 1:
                    #Va a iterar dependiendo del numero de funciones
                    for f in range(len(fun_num)):
                        #Me muevo a la caja indicada
                        main_app = driver.find_element_by_id('main-app')
                        box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div['+ str(f+1)+']')
                        
                        #Otengo el nombre de la funcion
                        tipo_funcion_t = box.find_element_by_tag_name('span').text + '' + box.find_element_by_tag_name('h5').text
                        
                        print(tipo_funcion_t)
                        #Me muevo a la caja de los horarios
                        horario_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div['+ str(f+1)+']/div[2]')
                        #Obtengo el contenido de la caja
                        horario_contenido = horario_box.find_elements_by_xpath("*")
                        
                        for h in range(len(horario_contenido)):
                            main_app = driver.find_element_by_id('main-app')
                            hora_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div['+ str(f+1)+']/div[2]/div['+ str(h+1) +']')
                            hora = hora_box.find_element_by_tag_name('label').text
                            
                            fn = Funcion()
                            fn.sucursal = g_sucursal
                            fn.fecha = dia
                            fn.pelicula = g_peli
                            fn.url_pelicula = g_url
                            fn.tipo_funcion = tipo_funcion_t
                            fn.hora = hora
                            fn.sala = ''
                            fn.asientos = 0
                            fn.activo = True
        
                            l_funciones.append(fn)
                
        sleep(5)
        print('Llego al final')
        driver.quit()

        return l_funciones

#main_app = driver.find_element_by_id('main-app')
#cine_box = main_app.find_element_by_xpath('//div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[2]/div[1]/div[2]/div['+ str(x+1)+']')

