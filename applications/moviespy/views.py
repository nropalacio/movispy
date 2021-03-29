from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Pelicula
from django.http import HttpResponseRedirect, HttpResponse
import time
from .scrips.getpeliculas import ObtenerPeliculas
from .scrips.getsanta import LocalizarHorasSalasSantaAna
from .scrips.getlista import getListaBYNombre, obteneNombres, getlistaBuena, obtenerMaximo, getlistaModificada, obteneTodosNombres
from .scrips.getPrimaryData import getlistaData
from .scrips.quickstart import GoogleConnection
from .scrips.updatedrive import comprobarDia, getDatosDia, guardar
from .models import Pelicula, Dia, Sucursal, Funcion
from .guardar import Guardar
from .scrips.prueba_xpath import LocalizarHorasSalas
from .scrips.buscar import Buscar
from .scrips.buscarsanta import BuscarSanta
from datetime import datetime
from django.urls import reverse_lazy
from .forms import Fecha
import csv
import xlwt
from django.shortcuts import redirect
# Create your views here.

class InicioView(ListView):
    """ vista que carga la pagina de inicio """
    template_name = 'inicio.html'
    context_object_name = 'result'
    shortDate = datetime.today().strftime('%Y-%m-%d')

    def get_queryset(self):
        shortDate = datetime.today().strftime('%Y-%m-%d')
        peliculas = obteneTodosNombres(shortDate)
        func = Funcion.objects.filter(fecha__dia=shortDate)
        peliculas = nombres = Funcion.objects.values('pelicula').filter(fecha__dia=shortDate).distinct()
        resultados = [len(peliculas), len(func)]
        return resultados
    
    def post(self, request):

        if 'iniciar' in request.POST:
            
            def diaExist():
                shortDate = datetime.today().strftime('%Y-%m-%d')
                if Dia.objects.filter(dia = shortDate):
                    return True
                else:
                    return False

                    
            
            if diaExist() == True:
                enviar = 'moviespy_app:inicio'
            else:
                try:
                    shortDate = datetime.today().strftime('%Y-%m-%d')
                    d = Dia()
                    d.dia = datetime.today()
                    d.activo = True
                    d.save()

                    #Inicia busqueda de urls
                    urls = ObtenerPeliculas.printNombres()

                    #Inicia busqueda de datos
                    funsiones = LocalizarHorasSalas.iniciar(urls, d)
                    for f in funsiones:
                        f.save()

                    time.sleep(5)
                    print('Inicia busqueda de santa ana')
                    funcionessanta = LocalizarHorasSalasSantaAna.iniciar(urls, d)
                    for f in funcionessanta:
                        f.save()
                    
                    print('busqueda de datos por sucursal')
                    #Nuevo cambio ahora las busquedas seran por sucursal
                    sucursales = []
                    for x in range(3):
                        funciones = Funcion.objects.all().filter(fecha__dia=shortDate, sucursal__id=x+1)   
                        sucursales.append(funciones) 

                    #Realiza la busqueda por sucursal
                    time.sleep(5)
                    Buscar.buscarFuncion(sucursales[0])
                    time.sleep(5)
                    Buscar.buscarFuncion(sucursales[1])
                    time.sleep(5)
                    Buscar.buscarFuncion(sucursales[2])
                        

                    time.sleep(5)
                    print('Inicia busqueda de salas de santa ana')
                    funciones2 = Funcion.objects.all().filter(fecha__dia=shortDate, sucursal__id=4)
                    Buscar.buscarFuncionSanta(funciones2)

                    enviar = 'moviespy_app:dia'
                except Exception as e:
                    print(e)
                    shortDate = datetime.today().strftime('%Y-%m-%d')
                    enviar = 'moviespy_app:inicio'
                    Dia.objects.filter(dia=shortDate).delete()

        return redirect(reverse_lazy(enviar))



class ListAllFunciones(ListView):
    template_name = 'moviespy/consulta.html'
    ordering = 'id'
    context_object_name = 'dia'
    #context_object_name = 'funciones'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        if palabra_clave:
            fecha = Dia.objects.filter(dia = palabra_clave)
            print('la fecha es: ', len(fecha))
            if len(fecha) == 1:
                
                lista_grande = []
                lista1 = []
                lista2 = []
                lista3 = []
                lista4 = []



                
                nombres = obteneNombres(1, palabra_clave)
                for nombre in nombres:
                    lista1.append(getlistaModificada(nombre, 1, palabra_clave))

                lista_grande.append(lista1)

                nombres = obteneNombres(2, palabra_clave)
                for nombre in nombres:
                    lista2.append(getlistaModificada(nombre, 2, palabra_clave))

                lista_grande.append(lista2)

                nombres = obteneNombres(3, palabra_clave)
                for nombre in nombres:
                    lista3.append(getlistaModificada(nombre, 3, palabra_clave))

                lista_grande.append(lista3)

                nombres = obteneNombres(4, palabra_clave)
                for nombre in nombres:
                    lista4.append(getlistaModificada(nombre, 4, palabra_clave))

                lista_grande.append(lista4)

                ##############################################
                    
                nombres = obteneNombres(1, palabra_clave)
                datos = []
                for nombre in nombres:
                    datos.append(getlistaData(nombre, 1, palabra_clave))

                lista_grande.append(datos)


                nombres = obteneNombres(2, palabra_clave)
                datos = []
                for nombre in nombres:
                    datos.append(getlistaData(nombre, 2, palabra_clave))

                lista_grande.append(datos)


                nombres = obteneNombres(3, palabra_clave)
                datos = []
                for nombre in nombres:
                    datos.append(getlistaData(nombre, 3, palabra_clave))

                lista_grande.append(datos)

                nombres = obteneNombres(4, palabra_clave)
                datos = []
                for nombre in nombres:
                    datos.append(getlistaData(nombre, 4, palabra_clave))

                lista_grande.append(datos)


                dia = [True, lista_grande, palabra_clave]
            else:
                dia= [False, 'No hay nada que mostrar']



            
        else:
            dia = [False, 'Realice una busqueda']
        
        return dia









class FuncionesDelDiaView(ListView):
    template_name = 'moviespy/dia.html'
    context_object_name = 'funciones'
    ordering = 'hora'


    def get_queryset(self):

        def obteneFunciones(id):
            shortDate = datetime.today().strftime('%Y-%m-%d')
            funciones = Funcion.objects.all().filter(fecha__dia=shortDate, sucursal__id=id).order_by('hora')
            return funciones

        shortDate = datetime.today().strftime('%Y-%m-%d')
        lista_grande = []
        lista1 = []
        lista2 = []
        lista3 = []
        lista4 = []

        fecha = Dia.objects.filter(dia = shortDate)
        if len(fecha) == 1:
            nombres = obteneNombres(1, shortDate)
            for nombre in nombres:
                lista1.append(getlistaModificada(nombre, 1, shortDate))

            lista_grande.append(lista1)

            nombres = obteneNombres(2, shortDate)
            for nombre in nombres:
                lista2.append(getlistaModificada(nombre, 2, shortDate))

            lista_grande.append(lista2)

            nombres = obteneNombres(3, shortDate)
            for nombre in nombres:
                lista3.append(getlistaModificada(nombre, 3, shortDate))

            lista_grande.append(lista3)

            nombres = obteneNombres(4, shortDate)
            for nombre in nombres:
                lista4.append(getlistaModificada(nombre, 4, shortDate))

            lista_grande.append(lista4)

            ##############################################
                
            nombres = obteneNombres(1, shortDate)
            datos = []
            for nombre in nombres:
                datos.append(getlistaData(nombre, 1, shortDate))

            lista_grande.append(datos)


            nombres = obteneNombres(2, shortDate)
            datos = []
            for nombre in nombres:
                datos.append(getlistaData(nombre, 2, shortDate))

            lista_grande.append(datos)


            nombres = obteneNombres(3, shortDate)
            datos = []
            for nombre in nombres:
                datos.append(getlistaData(nombre, 3, shortDate))

            lista_grande.append(datos)

            nombres = obteneNombres(4, shortDate)
            datos = []
            for nombre in nombres:
                datos.append(getlistaData(nombre, 4, shortDate))

            lista_grande.append(datos)

            
            dia = [True, lista_grande]
        else:
            dia = [False, 'No hay datos que mostrar']
        

        return dia

class EmpleadoDeleteView(TemplateView):
    template_name = "moviespy/descargar.html"
    success_url = reverse_lazy('moviespy_app:consulta')


# def export_csv(request, pk):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename= algo.csv'
#     writer=csv.writer(response)
#     writer.writerow(['hola', 'puta'])
#     print('Este valor me paso', pk)
#     return response


def export_excel(request, pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename= horas_'+pk+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    # font_style=xlwt.XFStyle()
    # font_style.font.bold = True

    nombres1 = obteneNombres(1, pk)
    nombres2 = obteneNombres(2, pk)
    nombres3 = obteneNombres(3, pk)
    nombres4 = obteneNombres(4, pk)
    lista1 = []
    lista2 = []
    lista3 = []
    lista4 = []
    for nombre in nombres1:
        lista1.append(getListaBYNombre(nombre, pk, 1))
    
    for nombre in nombres2:
        lista2.append(getListaBYNombre(nombre, pk, 2))

    for nombre in nombres3:
        lista3.append(getListaBYNombre(nombre, pk, 3))
    
    for nombre in nombres4:
        lista4.append(getListaBYNombre(nombre, pk, 4))


    #CREO LA HOJA DE CINEPOLIS GALERIAS
    ws = wb.add_sheet('Cinepolis Galerias')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista1
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1

    
    ws = wb.add_sheet('MiCine Multiplaza Panamericana')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista2
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1


    ws = wb.add_sheet('Cinepolis VIP Galerias')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista3
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1

    ws = wb.add_sheet('MiCine Metro Centro Santa Ana')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista4
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1

    wb.save(response)

    return response


def export_excel_dia(request):
    shortDate = datetime.today().strftime('%Y-%m-%d')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename= horas_'+shortDate+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    # font_style=xlwt.XFStyle()
    # font_style.font.bold = True

    nombres1 = obteneNombres(1, shortDate)
    nombres2 = obteneNombres(2, shortDate)
    nombres3 = obteneNombres(3, shortDate)
    nombres4 = obteneNombres(4, shortDate)
    lista1 = []
    lista2 = []
    lista3 = []
    lista4 = []
    for nombre in nombres1:
        lista1.append(getListaBYNombre(nombre, shortDate, 1))
    
    for nombre in nombres2:
        lista2.append(getListaBYNombre(nombre, shortDate, 2))

    for nombre in nombres3:
        lista3.append(getListaBYNombre(nombre, shortDate, 3))
    
    for nombre in nombres4:
        lista4.append(getListaBYNombre(nombre, shortDate, 4))


    #CREO LA HOJA DE CINEPOLIS GALERIAS
    ws = wb.add_sheet('Cinepolis Galerias')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista1
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1

    
    ws = wb.add_sheet('MiCine Multiplaza Panamericana')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista2
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1


    ws = wb.add_sheet('Cinepolis VIP Galerias')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista3
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1

    ws = wb.add_sheet('MiCine Metro Centro Santa Ana')
    row_num= 0
    font_style=xlwt.XFStyle()
    rows = lista4
    for row in rows:
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        row_num+=1

    wb.save(response)

    return response

