"""
Created on Tue Sep  8 14:29:59 2020

@author: PhoenixL

vector and matrix
V=[ 0 for j in range(3)]
from random import *
A=[[random() for i in range(Tcols)] for j in range(Trows)] 
#A of TrowsxTcols
len(A) rows
len(A[0]) columns



"""

import numpy as np
from random import *
from math import *
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import matplotlib.pyplot as grafica


def normalizar(r,lb,ub):
    return (r-lb)/(ub-lb+0.00000052);

    

def desnormalizar(n,lb,ub):
    return n*(ub-lb)+lb;


def maxp(V):
    #(val,pos)=maxp(V)
    n=len(V);
    pos=0;
    val=V[pos];
    for e in range(n):
        if V[e]>val:
            val=V[e];
            pos=e;          
            
    return val,pos

def minp(V):
    #(val,pos)=minp(V)
    n=len(V);
    pos=0;
    val=V[pos];
    for e in range(n):
        if V[e]<val:
            val=V[e];
            pos=e;
                
    return val,pos

    
def DatabaseRead():
    #Database or table
    # DataBrute=DatabaseRead();
    #Excel reading
    #df = pd.read_excel('Desktop/Projects2020/PythonCurse/Neuralnetworks/datasetNN.xls')
    #df = pd.read_excel('datasample.xls')
    df = pd.read_excel('CondicionSalud.xlsx');
    #df = pd.read_excel('Justicia.xlsx');
    Nrows=len(df); Ncols=len(df.columns);
    DataBrute = [[0 for i in range(Ncols)] for j in range(Nrows)]; 
    for r in range(Nrows):
        for c in range(Ncols):
            DataBrute[r][c]=df[df.columns[c]][r];
    return DataBrute
        


def plotgraph(V):
    N=len(V);
    D=[ j for j in range(N)]
    grafica.figure(1)
    grafica.plot(D,V,'b:',linewidth=2)
    grafica.xlabel('Número de datos')
    grafica.ylabel('Señal')
    grafica.show()

    #programa principal


def NormalData(DataExp):
###LMTT092018
###  (DataNorm,MRange)=NormalData(DataExp)
##
    Trows=len(DataExp);
    Tcols=len(DataExp[0]);
    V = [0 for i in range(Trows)];
    MRange = [[0 for i in range(2)] for j in range(Tcols)]; 
    DataNorm = [[0 for i in range(Tcols)] for j in range(Trows)]; 
    for c in range(Tcols):
        for r in range(Trows):
            V[r]=DataExp[r][c];
        (valmax,posmax)=maxp(V);
        (valmin,posmin)=minp(V)    
        for r in range(Trows):
            DataNorm[r][c] = normalizar(DataExp[r][c],valmin,valmax);
        MRange[c][0]=valmin;
        MRange[c][1]=valmax;
    return DataNorm, MRange
    


def CalcD(V1,V2):
    B = len(V1);
    s = 0
    for b in range(B):
        s = s + (V1[b]-V2[b])**2;
    d = s**0.5;
    return d    
    

def Agente(X,DB,MRange):
    ## R = Agente(X,DB,MRange);
    Trows = len(DB);
    Tcols = len(DB[0]);
    Xn = [ 0 for j in range(Tcols-1)];#Tcols-1 = total de entradas
    D = [ 0 for j in range(Trows)];
    V1 = [ 0 for j in range(Tcols-1)];
    V2 = [ 0 for j in range(Tcols-1)];
    y = 0;
    for b in range(Tcols-1):
        Xn[b] = normalizar(X[b],MRange[b][0],MRange[b][1]);
        
  
    for r in range(Trows):
        for c in range(Tcols-1):
            V1[c] = Xn[c];
            V2[c] = DB[r][c];
    
        #Cálculo de distancia Euclideana
        D[r] = CalcD(V1,V2);        
    #end for
    #Distancia mínima
    (val,pos) = minp(D);
    #print('Registro mas parecido:',pos)
    
    #Extraer la respuesta
    yn = DB[pos][Tcols-1]
    
    y = desnormalizar(yn,MRange[Tcols-1][0],MRange[Tcols-1][1]);
    
    return y


def AgenteXAI(X,DB,MRange):
    # (y,Xp,val) = AgenteXAI(X,DB,MRange);
    # Xp es el caso que es similar al presentado.
    # val señala la distancia que existe entre ambos
    Trows = len(DB);
    Tcols = len(DB[0]);
    Xn = [ 0 for j in range(Tcols-1)];#Tcols-1 = total de entradas
    Xp = [ 0 for j in range(Tcols-1)];#Tcols-1 = total de entradas
    D = [ 0 for j in range(Trows)];
    V1 = [ 0 for j in range(Tcols-1)];
    V2 = [ 0 for j in range(Tcols-1)];
    y = 0;
    for b in range(Tcols-1):
        Xn[b] = normalizar(X[b],MRange[b][0],MRange[b][1]);
        
  
    for r in range(Trows):
        for c in range(Tcols-1):
            V1[c] = Xn[c];
            V2[c] = DB[r][c];
    
        #Cálculo de distancia Euclideana
        D[r] = CalcD(V1,V2);        
    #end for
    #Distancia mínima
    (val,pos) = minp(D);
    #print('Registro mas parecido:',pos)
    for b in range(Tcols-1):
        Xp[b] =  round(desnormalizar(DB[pos][b],MRange[b][0],MRange[b][1]));
    
    #Extraer la respuesta
    yn = DB[pos][Tcols-1]
    
    y = round(desnormalizar(yn,MRange[Tcols-1][0],MRange[Tcols-1][1]));
    
    return y,Xp,val

### Test: give X based on MRange
### (y,Xp,val) = AgenteXAI(X,DB,MRange);print('respuesta:',round(y), 'caso similar:',Xp,' distancia:',val)



### Matriz de correlación de Pearson    
    
def DataExtract(ExpData):
    #X,Y = DataExtract(ExpData);
    TD = len(ExpData);
    Cols = len(ExpData[0]);
    #TD total of data
    # TI Inputs, only one output
    TI = Cols - 1;
    X = [[0 for i in range(Cols)] for j in range(TD)];
    Y = [ 0 for j in range(TD)]
    for dd in range(TD):
        for i in range(TI+1): #or Cols, to consider independent term
            if (i==0):
                X[dd][i] = 1.0;
            else:
                X[dd][i] = ExpData[dd][i-1];#Avoid output
            
        Y[dd] = ExpData[dd][Cols-1];
            
            
    return X,Y
    
        
def ExtractX(ExpData):
    # X = ExtractX(ExpData);
    TD = len(ExpData);
    Cols = len(ExpData[0]);
    #TD total of data
    # TI Inputs, only one output
    TI = Cols - 1;
    X = [[0 for i in range(TI)] for j in range(TD)];
    for dd in range(TD):
        for i in range(TI):
            X[dd][i] = ExpData[dd][i-1];#Avoid output

    return X
    

def mean(data):
    return sum(data) / len(data)

def std_dev(data):
    mu = mean(data)
    return (sum((x - mu) ** 2 for x in data) / len(data)) ** 0.5

def covariance(x, y):
    mean_x = mean(x)
    mean_y = mean(y)
    return sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)

def pearson_correlation(x, y):
    return covariance(x, y) / (std_dev(x) * std_dev(y))

def transpose(matrix):
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def correlation_matrix(data_matrix):
    # corr_matrix = correlation_matrix(data_matrix)
    # Transponer la matriz para que cada sublista sea una variable (columna)
    variables = transpose(data_matrix)
    n = len(variables)
    corr_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(1.0)
            else:
                r = pearson_correlation(variables[i], variables[j])
                row.append(round(r, 4))
        corr_matrix.append(row)
    return corr_matrix

         
def plot_correlation_heatmap(corr_matrix, labels=None):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 10))  # Aumentar tamaño del gráfico
    cax = ax.matshow(corr_matrix, cmap="bwr", vmin=-1, vmax=1)

    if labels is None:
        labels = [f"X{i+1}" for i in range(len(corr_matrix))]

    # Posicionar etiquetas
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=8)  # Rotar y ajustar tamaño
    ax.set_yticklabels(labels, fontsize=8)

    # Mostrar los valores dentro de cada celda
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix)):
            value = round(corr_matrix[i][j], 2)
            #ax.text(j, i, f"{value}", va='center', ha='center', color='black', fontsize=6)

    plt.colorbar(cax, label='Correlación de Pearson')
    plt.title("Matriz de Correlación", fontsize=14)
    plt.tight_layout()
    plt.show()   
    
    # Guardar en alta resolución
    plt.savefig("grafico_alta_resolucion.png",
    dpi=600,               # resolución
    bbox_inches='tight',   # recortar bordes
    pad_inches=0.1)        # margen opcional

    plt.close()


    # Ejemplo de uso:
    # Cada fila es una observación, cada columna es una variable
    # data = [
    #     [10, 15, 5],   # observación 1
    #     [20, 25, 10],  # observación 2
    #     [30, 35, 10],  # observación 3
    #     [40, 45, 20],  # observación 4
    #     [50, 55, 25]   # observación 5
    # ]

    # corr = correlation_matrix(data)
    # corr = correlation_matrix(DataNorm)


        
    # labels = ['X1', 'X2', 'X3' ]
    #labels = ['Temperatura (°C)',	'Humedad (%)',	'Calidad del Aire (%)',	'Iluminación (%)	','Temperatura corporal (°C)',	'Pulso cardiaco (pulsos por minuto)','Condición de salud (1-5)']
    #plot_correlation_heatmap(corr, labels)
        
    #Significado: 1 (rojo) relación lineal directa entre variables,
    # -1 (azul) Relación inversa entre variables.
    # 0 (Blanco) No hay relación entre las variables
    
    
    ## labels = ['Género',	'Edad',	'Ciudad',	'Delito principal',	'Antecedentes previos',	'Nivel socioeconómico',	'Puntuación de riesgo (0-100)']


	

