from django.shortcuts import render, redirect
import joblib
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO

# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')

# Prediccion estudiantil
def formularioEstudiantil(request):
    horas = range(0, 24)  # 0 a 23 inclusive
    return render(request, 'formularioEstudiantil.html', {'horas': horas})




# Prediccion salud
#def formularioSalud(request):
    if request.method == 'POST':
        edad = int(request.POST.get('edad'))
        imc = float(request.POST.get('imc'))
        actividad_fisica = int(request.POST.get('actividad_fisica'))
        presion_arterial = int(request.POST.get('presion_arterial'))
        antecedentes_diabetes = int(request.POST.get('antecedentes_diabetes'))

        modelo_lineal = joblib.load('Aplicaciones/Prediccion/modelo_lineal_diabetes.pkl')

        prediccion = modelo_lineal.predict([[edad, imc, actividad_fisica, presion_arterial, antecedentes_diabetes]])

        # Graficar la predicción
        import pandas as pd
        df = pd.DataFrame({
            'Edad': [edad],
            'Predicción': [prediccion[0]],
        })

        # Gráfico de regresión lineal
        plt.figure(figsize=(10, 6))
        sns.regplot(x='Edad', y='Predicción', data=df, ci=None, color='blue', scatter_kws={'color': 'red'})
        plt.title('Regresión Lineal: Edad vs Predicción de Riesgo de Diabetes')
        plt.xlabel('Edad')
        plt.ylabel('Predicción de Riesgo')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graphic = base64.b64encode(image_png).decode('utf-8')

        #Regresión logística
        modelo_logistico = joblib.load('Aplicaciones/Prediccion/modelo_logistico_diabetes.pkl')
        prediccion_logistica = modelo_logistico.predict([[edad, imc, actividad_fisica, presion_arterial, antecedentes_diabetes, prediccion[0]]])

        plt.figure(figsize=(8, 2))
        plt.barh(['Riesgo'], [prediccion_logistica[0]], color='skyblue', edgecolor='black')
        plt.xlim(0, 1)
        plt.xlabel('Probabilidad')
        plt.title(f'Riesgo de Diabetes: {prediccion_logistica[0]:.2%}')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.savefig(buffer, format='png')

        buffer.seek(0)
        grafico_regresion = buffer.getvalue()
        buffer.close()
        grafico2 = base64.b64encode(grafico_regresion).decode('utf-8')

        return render(request, 'graficoSalud.html', {
            'glucosa': prediccion[0], 
            'graphic': graphic, 
            'riesgo_diabetes': prediccion_logistica[0],
            'graphic2': grafico2,
            })
    
    return render(request, 'formularioSalud.html')


# graficos de prediccion
#def graficoSalud(request):
    return render(request, 'graficoSalud.html')

def graficoEstudiantil(request):
    return render(request, 'graficoEstudiantil.html')


#Integrantes

def integrantes(request):
    return render(request, 'integrantes.html')