from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

# Prediccion estudiantil
def formularioEstudiantil(request):
    return render(request, 'formularioEstudiantil.html')




# Prediccion salud
def formularioSalud(request):
    return render(request, 'formularioSalud.html')


# graficos de prediccion
def graficoSalud(request):
    return render(request, 'graficoSalud.html')

def graficoEstudiantil(request):
    return render(request, 'graficoEstudiantil.html')


#Integrantes

def integrantes(request):
    return render(request, 'integrantes.html')