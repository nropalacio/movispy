
from django.contrib import admin
from django.urls import path
from . import views

app_name = "moviespy_app"


urlpatterns = [
    path(
        '',
        views.InicioView.as_view(),
        name='inicio'
    ),
    path('moviespy/', views.PruebaTemplateView.as_view()),
    path(
        'consulta-funciones/',
        views.ListAllFunciones.as_view(),
        name='consulta'
    ),
    path(
        'datos-dia/',
        views.FuncionesDelDiaView.as_view(),
        name='dia'
    ),
]
