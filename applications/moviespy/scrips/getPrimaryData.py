from ..models import Funcion, Dia
from datetime import datetime


def obteneNombres(id_sucursal, fecha):
    #shortDate = datetime.today().strftime('%Y-%m-%d')
    nombres = Funcion.objects.values('pelicula').filter(fecha__dia=fecha, sucursal__id = id_sucursal).distinct()
    return nombres


def getlistaData(nombre, id_sucursal, fecha):


    def getDatos(nombre, id_sucursal, fecha):
        #shortDate = datetime.today().strftime('%Y-%m-%d')
        datos = []
        datos = Funcion.objects.values('tipo_funcion', 'hora', 'sala', 'asientos').filter(fecha__dia=fecha, pelicula=nombre['pelicula'], sucursal__id = id_sucursal).order_by('hora')
        return datos
        
   
    lista_nombre = []
    horario = []
    lista_nombre.append(nombre['pelicula'])
    datos = getDatos(nombre, id_sucursal, fecha)
    print('datos')
    print(datos)
         
    lista_nombre.append(datos)
    return lista_nombre