from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


DRIVER_PATH = '/home/rodrigo/web_drivers/chromedriver'
MAIN_URL = 'https://www.cinepolis.com.sv/cartelera'

driver = webdriver.Chrome(DRIVER_PATH)
driver.get(MAIN_URL)
actions = ActionChains(driver)
driver.maximize_window()



try:
    elements = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'getTicket_3018'))
    )
    the_button = elements.find_element_by_tag_name('button')
    the_button.click()
    time.sleep(5)
    actions.send_keys(Keys.ARROW_DOWN).perform()
    actions.send_keys(Keys.ARROW_DOWN).perform()
    actions.send_keys(Keys.ARROW_DOWN).perform()
    actions.send_keys(Keys.ARROW_DOWN).perform()
    actions.send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(5)
    detalles = driver.find_element_by_class_name('movie-details')
    titulo = detalles.find_element_by_tag_name('h1').text
    cines_det = driver.find_element_by_id('main-app')
    time.sleep(5)

    cines = cines_det.find_element_by_tag_name('ul')
    nombre = cines.find_element_by_tag_name('li')
    dragon = nombre.find_element_by_tag_name('h3').text
    el_div = nombre.find_element_by_xpath('//div[@class="d-flex mt-3"]')
    casi = el_div.find_element_by_tag_name('span').text
    la_caja_de_divs = nombre.find_element_by_xpath('//div[@class="d-flex flex-wrap"]')
    los_horarios_div = la_caja_de_divs.find_elements_by_xpath('//div[@class="d-flex mr-2 radio-group-cnpls  mt-3"]')
    el_primero = []
    for horario in los_horarios_div:
        el_primero.append(horario.find_element_by_tag_name('label').text)
        horario.find_element_by_tag_name('label').click()

    print(titulo)
    print(dragon)
    print(casi)

    #el_boton.click()
    time.sleep(5)
    caja_boton = cines.find_element_by_xpath('//button[@id="buyTickets"]')
    caja_boton.find_element_by_tag_name("span").click()
    print("si aqui esta")
    time.sleep(10)

    #Aqui empieza la parte que nos va a dar 10
    caja_asientos = driver.find_element_by_xpath('//div[@class="vue-virtual-collection-container"]')
    asientos = caja_asientos.find_elements_by_class_name("cell-container")
    conteo_hijos = []
    conteo = 0
    for asiento in asientos:
        if len(asiento.find_elements_by_css_selector("*")) == 3 and len(asiento.find_elements_by_tag_name("img")) != 0 and asiento.find_element_by_tag_name("img").get_attribute("class") == "seat-disable":
            conteo += 1


finally:
    driver.quit()

print(titulo)
print(dragon)
print(casi)
#print(los_horarios_div)
print(el_primero)
#print(asiento1)
print(conteo_hijos)
print("######################")
print(conteo)
#print(sala)

driver.quit()
