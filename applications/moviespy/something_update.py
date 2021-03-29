#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from .models import Funcion, Dia
from datetime import datetime
from .scrips.buscar import Buscar
from .scrips.buscarsanta import BuscarSanta





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
    lista_funciones_gale = []
    lista_funciones_santa = []
    lista_funciones_multi = []
    lista_funciones_vip = []
    for funcion in funciones:
        hora_funcion = calcularTiempo(int(funcion.hora[0:2]), int(funcion.hora[3:5]))
        print('Dif de tiempo:', hora_funcion - actual)
        if (hora_funcion - actual) < 0:
            setInactivo(funcion)
            
        if (hora_funcion - actual) <= 5 and (hora_funcion - actual) >= 0:
            setInactivo(funcion)
            if funcion.sucursal.id == 4:
                lista_funciones_santa.append(funcion)
            elif funcion.sucursal.id == 3:
                lista_funciones_vip.append(funcion)
            elif funcion.sucursal.id == 2:
                lista_funciones_multi.append(funcion)
            elif funcion.sucursal.id == 1:
                lista_funciones_gale.append(funcion)
            print('Esta hora sigue: ', 'min restantes: ', hora_funcion - actual)

    if (len(lista_funciones_gale) > 0):
        Buscar.buscarFuncion(lista_funciones_gale)
    
    if (len(lista_funciones_multi) > 0):
        Buscar.buscarFuncion(lista_funciones_multi)

    if (len(lista_funciones_vip) > 0):
        Buscar.buscarFuncion(lista_funciones_vip)

    if (len(lista_funciones_santa) > 0):
        Buscar.buscarFuncionSanta(lista_funciones_santa)

def update_something():
    calcular()
   


def printHello():
    print('hello')