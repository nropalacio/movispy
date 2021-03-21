from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def moverSucursal(driver, sucursal):

    #Con esto se revisa si esta cargado la lista de peliculas
    def getMovieList(main_driver):
        movie_list = main_driver.find_elements_by_xpath('//div[contains(@id,"getTicket_")]')
        return movie_list
            ##########################################################

    #Se obtiene la lista de peliculas, si no cargo, la lista estara vacia
    sleep(5)
    movie_list = getMovieList(driver)

        #Se verifica la lista, mientras la lista este vacia se repite el bucle
    while len(movie_list) == 0:
        #Se refresca la pagina
        driver.refresh()
        #Se esperan 
        sleep(5)
        #Se obtiene la lista y repite el ucle
        movie_list = getMovieList(driver)

    #Una vez verificado, se busca le combo box
    busqueda = driver.find_element_by_id('cinemaBillboardSearch')
    #CLick
    busqueda.click()
    sleep(1)


    #Esta variable se utiliza para guardar en la base de datos
    cine = ''
    if sucursal == 1:
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ENTER)
        sleep(1)
        cine = 'Cinépolis Galerías'
    elif sucursal == 2:
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ENTER)
        sleep(1)
        cine = 'MiCine Multiplaza Panamericana'
    elif sucursal == 3:
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ARROW_DOWN)
        sleep(1)
        busqueda.send_keys(Keys.ENTER)
        sleep(1)
        cine = 'Cinépolis VIP Galerías'

    return cine

def getMovieDetails(driver):
    movie_details = driver.find_elements_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[1]/div/h3')
    return movie_details