from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Pelicula
from django.http import HttpResponseRedirect
import time
from .scrips.getpeliculas import ObtenerPeliculas
from .models import Pelicula, Dia, Sucursal, Funcion
from .guardar import Guardar
from .scrips.prueba_xpath import LocalizarHorasSalas
from .scrips.buscar import Buscar
from datetime import datetime
from django.urls import reverse_lazy

# Create your views here.

class InicioView(TemplateView):
    """ vista que carga la pagina de inicio """
    template_name = 'inicio.html'
    #success_url = reverse_lazy('moviespy_app:consulta')
    def post(self, request):

        def diaExist():
            shortDate = datetime.today().strftime('%Y-%m-%d')
            if Dia.objects.filter(dia = shortDate):
                return True
            else:
                return False
        
                #a
        if 'iniciar' in request.POST:

            if diaExist() == True:
                try:
                    shortDate = datetime.today().strftime('%Y-%m-%d')
                    funciones = Funcion.objects.all().filter(fecha__dia=shortDate)
                    # f = Funcion.objects.get(id = 182)
                    # f4 = Funcion.objects.get(id = 175)
                    # f5 = Funcion.objects.get(id = 183)
                    # f6 = Funcion.objects.get(id = 51)
                    # f7 = Funcion.objects.get(id = 45)
                    Buscar.buscarFuncion(funciones)
                    vergon = 'inicio.html'
                    args = {'result': 'No hay nada que procesar'}
                except Exception as e:
                    vergon = 'inicio.html'
                    args = {'result': 'La cagaste '}
                    print(e)
                vergon = 'inicio.html'
            else:
                try:
                    d = Dia()
                    d.dia = datetime.today()
                    d.activo = True
                    d.save()
                    urls = ObtenerPeliculas.printNombres()
                    funsiones = LocalizarHorasSalas.iniciar(urls, d)
                    for f in funsiones:
                        f.save()
                    vergon = 'moviespy/dia.html'
                    args = {'result': 'Termino un proceso, los datos fueron guardados exitosamente'}
                except Exception as e:
                    args = {'result': e}
                    vergon = 'inicio.html'

        print('********TErmino*********')
        return render(request, vergon, args)
                # d = Dia()
                # d.dia = datetime.today()
                # d.activo = True
                # d.save()
                # urls = ObtenerPeliculas.printNombres()
                # funsiones = LocalizarHorasSalas.iniciar(urls, d)
                # for f in funsiones:
                #     f.save()
                
                #f = Funcion.objects.get(id = 33)
                #f4 = Funcion.objects.get(id = 58)
                #f5 = Funcion.objects.get(id = 67)
                #f6 = Funcion.objects.get(id = 51)
                #f7 = Funcion.objects.get(id = 45)
                #Buscar.buscarFuncion([f])
            
        



class PruebaTemplateView(TemplateView):
    template_name = "moviespy/prueba.html"

    def post(self, request):
        if 'iniciar' in request.POST:




            try:
                #d = Dia()
                #d.dia = datetime.today()
                #d.activo = True
                #d.save()
                #urls = ObtenerPeliculas.printNombres()
                
                #funsiones = LocalizarHorasSalas.iniciar(urls, d)
                #for f in funsiones:
                #    f.save()
                
                f = Funcion.objects.get(id = 33)
                #f4 = Funcion.objects.get(id = 58)
                #f5 = Funcion.objects.get(id = 67)
                #f6 = Funcion.objects.get(id = 51)
                #f7 = Funcion.objects.get(id = 45)
                Buscar.buscarFuncion([f])
                args = {'result': 'Termino un proceso, los datos fueron guardados exitosamente'}
            except Exception as e:
                args = {'result': e}

            print('********TErmino*********')

        
        return render(request, self.template_name, args)

class ListAllFunciones(ListView):
    template_name = 'moviespy/consulta.html'
    ordering = 'id'
    context_object_name = 'funciones'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword", '')
        print('Palabra: ', palabra_clave)
        lista = []#Empleado.objects.filter(full_name__icontains=palabra_clave)
        return lista

class FuncionesDelDiaView(ListView):
    template_name = 'moviespy/dia.html'
    context_object_name = 'funciones'
    ordering = 'hora'


    def get_queryset(self):

        def obteneFunciones(id):
            shortDate = datetime.today().strftime('%Y-%m-%d')
            funciones = Funcion.objects.all().filter(fecha__dia=shortDate, sucursal__id=id).order_by('hora')
            return funciones

        funciones = []
        funciones1 = obteneFunciones(1)
        funciones2 = obteneFunciones(2)
        funciones3 = obteneFunciones(3)
        funciones.append(funciones1)
        funciones.append(funciones2)
        funciones.append(funciones3)
        return funciones

class EmpleadoDeleteView(TemplateView):
    template_name = "moviespy/descargar.html"
    success_url = reverse_lazy('moviespy_app:consulta')
