#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from .models import Funcion, Dia
from datetime import datetime
from .scrips.buscar import Buscar


lista_funciones = []

def obteneFunciones():
    shortDate = datetime.today().strftime('%Y-%m-%d')
    funciones = Funcion.objects.all().filter(fecha__dia=shortDate).exclude(activo = False)
    return funciones

def setInactivo(funcion):
    funcion.activo = False
    funcion.save()

def calcularTiempo(hora, minutos):
    tiempo = (hora*60) + minutos
    return tiempo


def calcular():
    print('Inicio Chequeo')
    actual = calcularTiempo(datetime.now().hour, datetime.now().minute)
    funciones = obteneFunciones()
    lista_funciones = []
    for funcion in funciones:
        hora_funcion = calcularTiempo(int(funcion.hora[0:2]), int(funcion.hora[3:5]))
        print('Dif de tiempo:', hora_funcion - actual)
        if (hora_funcion - actual) < 0:
            setInactivo(funcion)
            
        if (hora_funcion - actual) <= 5 and (hora_funcion - actual) >= 0:
            setInactivo(funcion)
            lista_funciones.append(funcion)
            print('Esta hora sigue: ', 'min restantes: ', hora_funcion - actual)
    if (len(lista_funciones) > 0):
        Buscar.buscarFuncion(lista_funciones)

def update_something():
    calcular()