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
    if request.method == 'POST':
        horas_estudio_semanal = int(request.POST.get('horas_estudio_semanal'))
        asistencia = int(request.POST.get('asistencia'))
        participacion = int(request.POST.get('participacion'))
        evaluacion_parcial1 = float(request.POST.get('evaluacion_parcial1'))
        evaluacion_parcial2 = float(request.POST.get('evaluacion_parcial1'))
        evaluacion_parcial3 = float(request.POST.get('evaluacion_parcial1'))

        modelo_lineal = joblib.load('Aplicaciones/Prediccion/modelo_lineal_notas.pkl')
        modelo_logistico = joblib.load('Aplicaciones/Prediccion/modelo_logistico_notas.pkl')
        
        prediccion = modelo_lineal.predict([[horas_estudio_semanal, asistencia, participacion, evaluacion_parcial1, evaluacion_parcial2, evaluacion_parcial3]])
        prediccion_logistica = modelo_logistico.predict([[horas_estudio_semanal, asistencia, participacion, evaluacion_parcial1, evaluacion_parcial2, evaluacion_parcial3, prediccion[0]]])

        # --- Generar gráficos ---
        # Gráfico 1: Predicción lineal (Nota final)
        plt.figure(figsize=(8, 5))
        plt.bar(['Nota Final'], [prediccion[0]], color='skyblue', edgecolor='black')
        plt.ylim(0, 37)  # Nota entre 0 y 10
        plt.ylabel('Nota Predicha')
        plt.title(f'Predicción de Nota Final: {prediccion[0]:.2f}')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Guardar en buffer
        buf_lineal = BytesIO()
        plt.savefig(buf_lineal, format='png')
        plt.close()
        buf_lineal.seek(0)
        grafico_lineal = base64.b64encode(buf_lineal.read()).decode('utf-8')

        # Gráfico 2: Modelo Logistico
        plt.figure(figsize=(8, 2))
        plt.barh(['Riesgo'], [prediccion_logistica[0]], color='skyblue', edgecolor='black')
        plt.xlim(0, 1)
        plt.xlabel('Probabilidad')
        plt.title(f'Riesgo de Fracaso: {prediccion_logistica[0]:.2%}')
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        
        buf_log = BytesIO()
        plt.savefig(buf_log, format='png')
        plt.close()
        buf_log.seek(0)
        grafico_logistico = base64.b64encode(buf_log.read()).decode('utf-8')


        # Contexto para el template
        contexto = {
            'grafico_lineal': grafico_lineal,
            'grafico_logistico': grafico_logistico,
            'nota_final': f'{prediccion[0]:.2f}',
            'riesgo_fracaso': prediccion_logistica[0]
        }

        return render(request, 'graficoEstudiantil.html', contexto)



    return render(request, 'formularioEstudiantil.html')




# Prediccion salud
def formularioSalud(request):
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
def graficoSalud(request):
    return render(request, 'graficoSalud.html')

def graficoEstudiantil(request):
    return render(request, 'graficoEstudiantil.html')


#Integrantes

def integrantes(request):
    return render(request, 'integrantes.html')