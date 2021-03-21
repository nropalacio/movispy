
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('moviespy/', views.PruebaTemplateView.as_view()),
]
