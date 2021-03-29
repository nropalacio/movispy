from selenium import webdriver
from time import sleep
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def getMovieDetails(driver):
    try:
        movie_details = driver.find_elements_by_xpath('//*[@id="main-app"]/div/div[5]/div/div[2]/section/div[2]/div[2]/div[1]/div/div[4]/ul/li/div[1]/div/h3')
    except Exception as e:
        movie_details = []
    return movie_details

def getMovieList(main_driver):
    sleep(5)
    try:
        movie_list = main_driver.find_elements_by_xpath('//div[contains(@id,"getTicket_")]')
    except Exception as e:
        movie_list = []
    return movie_list

def getSeatList(driver):
    sleep(5)
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'seatsContainer')))
    except Exception as e:
        element = []
    return element

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