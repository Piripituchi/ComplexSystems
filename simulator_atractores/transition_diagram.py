#!/usr/bin/env python3
'''
Modulo:   transition_diagram.py
Autor:    Jesus Eduardo Angeles Hernandez
Fecha:    2021/06/11

Descripcion: Este codigo corresponde a un graficador del diagrama de diagrama de transiciones
             de un automata celular, fue desarrollado para la asignatura Complex Systems en la
             Escuela Superior de Computo del IPN.
'''
__author__ = "Jesus Eduardo Angeles Hernandez"
__email__ = "jeduardohdez98@gmail.com"
__status__= "Terminado"

import itertools as it
import networkx as nx
import tkinter as tk
import matplotlib.pyplot as plt
import pygraphviz as pgv
from tkinter import scrolledtext as st
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from tkinter.constants import END


#sudo apt-get install graphviz pkg-config
#sudo apt-get install graphviz libgraphviz-dev
#pip3 install pygraphviz
#sudo apt-get install graphviz graphviz-dev




def decode_rules(n_rule):
    rules=[
        [0,0,0],
        [0,0,1],
        [0,1,0],
        [0,1,1],
        [1,0,0],
        [1,0,1],
        [1,1,0],
        [1,1,1],
    ]
    binary_rule=str(bin(n_rule)).lstrip("0b")[::-1]
    for i in range(0,len(rules)):
        if i<len(binary_rule):
            rules[i].insert(3,binary_rule[i])
        else:
            rules[i].insert(3,0)
    return rules

def next_state(rules,last_state):
    new_state=[]
    for center_cell in range(0,len(last_state)):
        left_cell=center_cell-1
        right_cell=center_cell+1
        if left_cell < 0:
            left_cell=len(last_state)-1
        if right_cell == len(last_state):
            right_cell=0
        current_state=[last_state[left_cell],last_state[center_cell],last_state[right_cell]]
        for pattern in range(0,len(rules)):
            if current_state == rules[pattern][0:3:]:
                new_state.append(rules[pattern][3])
                break
    return new_state

def draw_graph(root,long,regla,scrlldtxt):
    r=int(regla.get())
    l=int(long.get())
    dicc=[0,1]
    lista=[list(elem) for elem in list(it.product(dicc,repeat=l))]

    rule=decode_rules(r)

    nodos=[]
    aristas=[]
    atractores=[]
    recorridos=[]

    for vertice in lista:
        while True:
            
            next=[int(elem) for elem in next_state(rule,vertice)]
            verticeStr=int(''.join(map(str,vertice)),2)
            nextStr=int(''.join(map(str,next)),2)
            if (verticeStr,nextStr) in aristas:
                atractores.append(''.join(map(str,next))+'\n')
                break
            nodos.append(verticeStr)
            aristas.append((verticeStr,nextStr))
            recorridos.append(vertice)
            vertice=next
            

    G=nx.DiGraph()
    G.add_nodes_from(nodos)
    G.add_edges_from(aristas)

    pos = nx.nx_agraph.graphviz_layout(G, prog='twopi', args='')

    root.fig.add_subplot(111).cla()
    nx.draw_networkx(G,pos,node_size=10, with_labels=False, arrows=True, arrowsize=5)
    plt.axis('off')
    plt.tight_layout()
    root.canvas.draw()

    scrlldtxt.configure(state="normal")
    scrlldtxt.delete(1.0,END)
    for element in list(set(atractores)):
        scrlldtxt.insert(tk.INSERT,element)
    scrlldtxt.configure(state="disable")

def cerrar(figure):
    figure.quit()     
    figure.destroy()

def ac_gui():
    #-----------------------------Crear widget root (Master frame)----------------------------------
    root = tk.Tk()
    root.wm_title("Diagrama de ciclos")
    #-----------------------------Inicializacion de variables de los widgets----------------------------------
    len_state = tk.IntVar(root, value=10)
    rule= tk.IntVar(root, value=10)
    time= tk.IntVar(root, value=10)
    color=tk.StringVar(root, value="0 0 0")

    #------------------------------Crear frame---------------------------------
    root.fig= plt.figure( dpi=100 ,figsize=(8,6) )

    #-----------------------------Crear area de dibujo de Tkinter----------------------------------
    root.canvas = FigureCanvasTkAgg(root.fig, master=root)  
    root.canvas.draw()
    root.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    #-----------------------Anadir barra de herramientas--------------------------
    toolbar = NavigationToolbar2Tk(root.canvas, root)# barra de iconos
    toolbar.update()
    root.canvas.get_tk_widget().pack(side=tk.LEFT, expand=1)

    #-----------------------Definicion de widgets del simulador--------------------------
    label_rule=tk.Label(root, text="Ingrese la regla del AC")
    label_rule.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    entry_rule=tk.Entry(master=root, bg='white', textvariable=rule)
    entry_rule.pack(side=tk.TOP, after=label_rule,fill=tk.X)
    
    label_len=tk.Label(root, text="Ingrese la longitud de los estados")
    label_len.pack(side=tk.TOP, after=entry_rule,fill=tk.X, expand=1)

    entry_len=tk.Entry(master=root, bg='white', textvariable=len_state)
    entry_len.pack(side=tk.TOP, after=label_len,fill=tk.X, expand=1)

    plot_button = tk.Button(master=root, text="Dibujar Grafica", command=lambda:draw_graph(root,len_state,rule,scrlledtxt))
    plot_button.pack(side=tk.TOP, after=entry_len,fill=tk.X, expand=1)
    
    close_button = tk.Button(master=root, text="Cerrar", command=lambda:cerrar(root))
    close_button.pack(side=tk.TOP, fill=tk.X, expand=1)

    scrlledtxt=st.ScrolledText(master=root, width=30, height=20, state="disable")
    scrlledtxt.pack(side=tk.TOP, after=close_button)
    root.mainloop()

#-----------------------Inicializacion del simulador--------------------------
if __name__ == "__main__":
    ac_gui()
