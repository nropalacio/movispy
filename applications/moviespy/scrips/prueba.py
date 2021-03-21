from prueba_xpath import LocalizarHorasSalas
from getpeliculas import ObtenerPeliculas
#from buscar import Buscar
from time import sleep

#urls = ['https://www.cinepolis.com.sv/peliculas/tom-y-jerry']
#urls = ObtenerPeliculas.printNombres()
#sleep(5)


try:
    urls = ObtenerPeliculas.printNombres()
    #clearLocalizarHorasSalas.iniciar(urls)
except Exception as e:
    print('Hubo un error, intentalo de nuevo: ', e)
