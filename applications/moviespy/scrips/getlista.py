#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from ..models import Funcion, Dia
from datetime import datetime



lista_funciones = []

def obteneNombres(id_sucursal, fecha):
    #shortDate = datetime.today().strftime('%Y-%m-%d')
    nombres = Funcion.objects.values('pelicula').filter(fecha__dia=fecha, sucursal__id = id_sucursal).distinct()
    return nombres

def obteneTodosNombres(fecha):
    #shortDate = datetime.today().strftime('%Y-%m-%d')
    nombres = Funcion.objects.values('pelicula').filter(fecha__dia=fecha).distinct()
    return nombres


#Este es el que voy a ocupar en excel para crear las columnas
def getListaBYNombre(nombre, fecha,  id_sucursal):
    horarios = []
    lista_nombres =[]#nombre, [lista, horarios]
    lista = []#lista nombres

    try:
        print('*************', nombre['pelicula'])
        #print('EL nombre es ', nombre['pelicula'])
        print(type(nombre['pelicula']))
        print('hola')
        lista_nombres.append(nombre['pelicula'])
        print('hola')
        horarios_func = Funcion.objects.values('hora').filter(fecha__dia=fecha, pelicula=nombre['pelicula'], sucursal__id = id_sucursal).order_by('hora')
        print('hola')
        for hora in horarios_func:
            print('JOTUM')
            lista_nombres.append(hora['hora'])
            
        #print(lista_nombres)
    except Exception as e:
        print(e)
    

    return lista_nombres


    

def getlistaBuena(nombres):


    def getHorarios(nombre):
        shortDate = datetime.today().strftime('%Y-%m-%d')
        horarios = []
        horarios_func = Funcion.objects.values('hora').filter(fecha__dia=shortDate, pelicula=nombre['pelicula']).order_by('hora')
        for hora in horarios_func:
            horarios.append(hora['hora'])
        return horarios
        
    lista = []
    for nombre in nombres:
        horario = getHorarios(nombre)
        lista.append(len(horario))

    maximo = max(lista)

        
    lista_buena = []

    for nombre in nombres:
        lista_nombre = []
        horario = []
        lista_nombre.append(nombre['pelicula'])
        horario = getHorarios(nombre)
        for x in range(maximo):
            if x < len(horario):
                lista_nombre.append(horario[x])
            lista_nombre.append(' - ')
        lista_buena.append(lista_nombre)

    return lista_buena




def obtenerMaximo(nombres):
    def getHorarios(nombre):
        shortDate = datetime.today().strftime('%Y-%m-%d')
        horarios = []
        horarios_func = Funcion.objects.values('hora').filter(fecha__dia=shortDate, pelicula=nombre['pelicula']).order_by('hora')
        for hora in horarios_func:
            horarios.append(hora['hora'])
        return horarios
        
    lista = []
    for nombre in nombres:
        horario = getHorarios(nombre)
        lista.append(len(horario))

    return max(lista)




#Este metodo obtendra una lista de esta forma [nombre, horaio1 | 2 y asi |]
def getlistaModificada(nombre, id_sucursal, fecha):


    def getHorarios(nombre, id_sucursal, fecha):
        #shortDate = datetime.today().strftime('%Y-%m-%d')
        horarios = []
        horarios_func = Funcion.objects.values('hora').filter(fecha__dia=fecha, pelicula=nombre['pelicula'], sucursal__id = id_sucursal).order_by('hora')
        for hora in horarios_func:
            horarios.append(hora['hora'])
        return horarios
   
    lista_nombre = []
    horarios = ''
    horario = []
    lista_nombre.append(nombre['pelicula'])
    horario = getHorarios(nombre, id_sucursal, fecha)
    print('horarios')
    print(horario)
    
    for x in range(len(horario)):
        if x == len(horario)-1:
            horarios = horarios + horario[x]
        else:
            horarios = horarios + horario[x] + ' | '
        
    lista_nombre.append(horarios)
    return lista_nombre
