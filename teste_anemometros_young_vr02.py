import os
from glob import glob
from io import StringIO
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from tkinter import filedialog
from tkinter import *

#os dados do anemometro estão na pasta 'E:\piero.maduro\Documents\Python_Scripts\testes_anemometros'
root = Tk()
root.withdraw()
ane_folder = filedialog.askdirectory()
ane_folder = ane_folder.replace('\\','/')
os.chdir(ane_folder)

anemometro=[]
files= os.listdir()
mydir = os.getcwd()

for f in files:
    if f.startswith('anemometro'):
        anemometro.append(os.path.join(mydir,f).replace('\\','/'))
    else:
        pass


for faux in anemometro:
    dd=[]
    with open(faux) as f:
        d = f.readlines()
        for a in d:
            dd.append(a.split(' '))

    headerNames= ['data','hora','intensidade','direcao','temp','umidade','pressao']
    df = pd.DataFrame(dd)
    df.columns=headerNames
    df = df.set_index(pd.to_datetime(df.data + ' ' + df.hora, format='%y-%m-%d %H:%M:%S'))
    df.intensidade = pd.to_numeric(df.intensidade, downcast='float')
    df.direcao = pd.to_numeric(df.direcao, downcast='float')
    
    subplot_kw = dict(facecolor='gainsboro')
    fig_kw = dict(nrows=2, ncols=1, sharex='all', figsize=(14, 10), facecolor='white')
    fig1, ax1 = plt.subplots(subplot_kw=subplot_kw, **fig_kw)
    fig1.autofmt_xdate()

    ################# crinado padrãp de exibição dos subplots ######################################################
    for _ax in ax1:
        _ax.set_axisbelow(True)
        _ax.spines['right'].set_visible(False)
        _ax.spines['top'].set_visible(False)
        _ax.xaxis.set_ticks_position('bottom')
        _ax.yaxis.set_ticks_position('left')
        _ax.grid(True, color='white', linestyle='-', linewidth=1.0)
        _ax.tick_params(axis='both', direction='inout', width=1)
        _ax.margins(x=.02, y=.05)

    ###############inserindo offset dos anemometros ################################################################
    # (para isso vc precisa subtrair as direçoes dos anemometros e encontrar o valor mediano)#######################
    offset = - 12.5

    ############### intensidade ane 1 ##############################################################################
    ax1[0].plot(
        df.index, df.intensidade, color='C1', marker='o', zorder=1,
        markersize=4, label='Anemometro 1')
    ############### intensidade ane 2 ##############################################################################
    ax1[1].plot(
        df.index, df.direcao, color='C0', marker='o', zorder=1,
        markersize=4, label='Anemometro 1')
    ############### inserindo titulo e nomes dos eixos Y (o eixo X é o tempo) ######################################
    ax1[0].set_title(u'Anemômetro (com {})'.format(faux.split('_')[-2]), fontsize=16)
    ax1[0].set_ylabel(u'Intensidade [m/s]', color='k', fontsize=12)
    ax1[1].set_ylabel(u'Direção [°]', color='k', fontsize=12)

    ############### criando limite para direção no eixo Y ##########################################################
    yticks = np.linspace(0, 360, 9)
    _ = ax1[1].set_yticks(yticks)

    ############## criando degrade de cores  (22,5°) para ajudar a visualização da direção neste plot temporal #####
    for ytick in yticks[1:-1:2]:
        ax1[1].axhspan(ytick - 22.5, ytick + 22.5, facecolor=[.8, .8, .8],
                        edgecolor='None', zorder=0)

    ax1[1].set_ylim(0, 360)
    ############## criando eixo gemeo para exibir os quadrantes #####################################################
    _ax11 = ax1[1].twinx()
    _ax11.set_yticks(yticks)
    geolabels = ['N', 'NE', 'L', 'SE', 'S', 'SO', 'O', 'NO', 'N']
    _ = _ax11.set_yticklabels(geolabels)

    ############## tirando grid, e contornos superiores e da lateral direita do grafico #############################
    _ax11.grid(False)
    _ax11.spines['top'].set_visible(False)
    _ax11.spines['right'].set_visible(False)

    ############## inserindo legendas ###############################################################################
    handles, labels = ax1[0].get_legend_handles_labels()
    labels = [label.split('.')[0] for label in labels]
    ax1[0].legend(labels)
    fig1
    plt.setp(ax1[0].get_xticklabels() ,visible=False)

