from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Pelicula
from django.http import HttpResponseRedirect
import time
from .scrips.getpeliculas import ObtenerPeliculas
from .models import Pelicula, Dia, Sucursal, Funcion
from .guardar import Guardar
from .scrips.prueba_xpath import LocalizarHorasSalas
from .scrips.buscar import Buscar
from datetime import datetime

# Create your views here.
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
