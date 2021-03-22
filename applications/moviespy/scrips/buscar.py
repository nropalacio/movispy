from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from .moversucursal import moverSucursal, getMovieDetails

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

        def getMovieList(main_driver):
            sleep(5)
            caja = main_driver.find_elements_by_xpath('//*[@id="main-app"]/div/div[5]/section[5]/div/div')#
            if len(caja) == 0:
                movie_list =[]
            else:
                movie_list = caja[0].find_elements_by_xpath('*')
            return movie_list

        def selectCine(driver, cine):
            print('Este cine quiere comparar: ', type(cine))
            c = 0
            #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li[1]/div[1]/div[1]/h3
            for x in range(3):
                cine_pantalla = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(x+1)+']/div[1]/div[1]/h3').text
                print('CIne de la app: ', cine_pantalla)
                print('El del objeto funcion: ', cine)
                if cine_pantalla == cine:
                    c = x+1
            return c
        
        
        
        def selectFuncion(driver, cine, tipo_funcion):
            num_fun = 0
            tipos_funciones = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]')
            fun_num = tipos_funciones.find_elements_by_xpath('*')
            print('El largo de la lista es: ', len(fun_num))
            for f in range(len(fun_num)):
                box = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(f+1)+']/div[1]')
                tipo_funcion_t = box.find_element_by_tag_name('span').text + '' + box.find_element_by_tag_name('h5').text
                if tipo_funcion == tipo_funcion_t:
                    num_fun = f+1
            return num_fun

        def selectHora(driver, cine, tipo_funcion, hora):
            num_hora = 0
            box_horas=driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]')
            horas = box_horas.find_elements_by_xpath('*')
            cont = 0
            la_hora = 0
            print('Hora pelicula: ', hora)
            for h in horas:
                print('Hora cajas: ', h.find_element_by_tag_name('label').text)
                cont += 1
                if hora == h.find_element_by_tag_name('label').text:
                    la_hora = cont
            return la_hora

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
                
                num_c = selectCine(driver, fun.sucursal.nombre)
                print('Probo este cine:', num_c)
                
                num_f = selectFuncion(driver, num_c, fun.tipo_funcion)
                print('Probo ests sucursal')
                
                num_h = selectHora(driver, num_c, num_f, fun.hora)
                print('Probo esta hora')
               #'//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]'
                #//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(cine)+']/div[2]/div['+ str(tipo_funcion)+']/div[2]/div['+ str(tipo_funcion)+']/label
                le_hora = driver.find_element_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li['+str(num_c)+']/div[2]/div['+ str(num_f)+']/div[2]/div['+ str(num_h)+']/label')
                driver.execute_script("arguments[0].scrollIntoView(true);", le_hora)
                sleep(10)
                le_hora.click()
                print('Le dio click a la hoa')
                boton = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'buyTickets')))
                print('Llego al boton')
                boton.click()
                sleep(5)
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'seatsContainer')))
                
                ###################################################################
                
                
                
                
                
                
                ####################################################################
                
                print('Sera aqui')
                asientos = element.find_elements_by_class_name("cell-container")
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
                fun.asientos = 404
                fun.sala = 'Error'
                fun.save()

        driver.quit()





        