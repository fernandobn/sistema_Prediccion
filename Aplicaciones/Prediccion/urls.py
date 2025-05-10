from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('formularioEstudiantil/', views.formularioEstudiantil, name='formularioEstudiantil'),
    path('formularioSalud/', views.formularioSalud, name='formularioSalud'),
    path('graficoSalud/', views.graficoSalud, name='graficoSalud'),
    path('graficoEstudiantil/', views.graficoEstudiantil, name='graficoEstudiantil'),
    path('integrantes/', views.integrantes, name='integrantes'),


]