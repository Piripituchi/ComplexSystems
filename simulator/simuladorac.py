#!/usr/bin/env python3
'''
Modulo:   simuladorac.py
Autor:    Jesus Eduardo Angeles Hernandez
Fecha:    2021/03/30

Descripcion: Este codigo corresponde a un simulador de automatas celulares desarrollado
             como 1er practica para la asignatura Complex Systems en la Escuela Superior
             de Computo del IPN.
'''
__author__ = "Jesus Eduardo Angeles Hernandez"
__email__ = "jeduardohdez98@gmail.com"
__status__= "Terminado"


#-----------------------------LIBRERIAS NECESARIAS----------------------------------

import tkinter as tk
from matplotlib import colors
import numpy as np
from tkinter import messagebox as MessageBox
from tkinter import filedialog as FileDialog
from tkinter import scrolledtext as st
from tkinter import colorchooser as ColorChooser
from tkinter.constants import END
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import random
import re

#-----------------------------DEFINICION DE FUNCIONES DE AUTOMATA CELULAR----------------------------------

#-----------------------------Decodificar regla----------------------------------
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

#-----------------------------Obtener estado siguiente----------------------------------
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

#-----------------------------Crear automata----------------------------------
def create_automata(initial_state,rules,time):
    ac_grid=np.zeros((time,len(initial_state)),dtype=int)
    ac_grid[0]=initial_state
    for t_state in range(1,time):
        ac_grid[t_state]=next_state(rules, initial_state)
        initial_state=ac_grid[t_state]
    return ac_grid

#-----------------------------DEFINICION DE FUNCIONES DEL SIMULADOR----------------------------------

#-----------------------------Contar las celulas por cada anillo----------------------------------
def number_cells(automata):
    res=[]
    time,ring=automata.shape
    for iteration in range(0,time):
        count_cell=0
        for cell in range(0,ring):
            if automata[iteration][cell]==1:
                count_cell+=1
        res.append("t = "+str(iteration)+" ; cells = "+str(count_cell)+"\n")
    return res

#-----------------------------Cerrar simulador----------------------------------
def cerrar(figure):
    figure.quit()     
    figure.destroy()

#-----------------------------Dibujar automata----------------------------------
def plot_automata(figure,txtbox_init_state,txtbox_rule,txtbox_time,scrlledtxt_ncells,txtbox_color):
    string_state=str(txtbox_init_state.get())
    if len(string_state)>1000 or len(string_state)<=0:
        return MessageBox.showinfo("Cadena invalida","La longitud de la condicion inicial tiene que estar en el rango de [0,1000]")
    if int(txtbox_rule.get())<0 or int(txtbox_rule.get())>255:
        return MessageBox.showinfo("Regla invalida","El numero que ingreso esta fuera del rango del codigo de Wolfram [0,255]")
    if int(txtbox_time.get())<=0:
        return MessageBox.showinfo("Iteraciones invalidas","El numero de iteraciones tiene que ser mayor que 0")
    if len(string_state)%2==0:
        string_elemental='0'*(int((len(string_state)/2))-1)+'1'+'0'*(int((len(string_state)/2)))
    else:
        string_elemental='0'*(int(round(float(len(string_state))/2)))+'1'+'0'*(int(round(float(len(string_state))/2)))
    init_state=[int(element) for element in list(string_state)]
    elemental_state=[int(element) for element in list(string_elemental)]
    rule=int(txtbox_rule.get())
    time=int(txtbox_time.get())
    color=str(txtbox_color.get())
    cell_cmap=create_colormap(color)
    rule_array=decode_rules(rule)
    user_automata=create_automata(init_state,rule_array,time)
    elemental_automata=create_automata(elemental_state,rule_array,time)
    a=figure.add_subplot(1,2,1).imshow(user_automata, cmap=cell_cmap, aspect="equal")
    b=figure.add_subplot(1,2,2).imshow(elemental_automata, cmap=cell_cmap, aspect="equal")
    print_ncells(scrlledtxt_ncells, user_automata)
    return a,b

#-----------------------------Guardar configuracion----------------------------------
def save_config(txtbox_init_state,txtbox_rule,txtbox_time,txtbox_color):
    string_state=str(txtbox_init_state.get())
    if len(string_state)>1000:
        return MessageBox.showinfo("Cadena invalida","La longitud de la condicion inicial es mayor a 1000 celulas")
    rule=int(txtbox_rule.get())
    time=int(txtbox_time.get())
    color=str(txtbox_color.get())
    fp=FileDialog.asksaveasfile(title="Guardar configuracion", mode='w', defaultextension=".txt")
    if fp:
        fp.write(string_state+'\n')
        fp.write(str(rule)+'\n')
        fp.write(str(time)+'\n')
        fp.write(str(color))
        fp.close()
    else: return MessageBox.showerror("Error","Fichero no guardado")

#-----------------------------Cargar configuracion----------------------------------
def load_config(txtbox_init_state,txtbox_rule,txtbox_time,txtbox_color):
    fp=FileDialog.askopenfile( title="Abrir configuracion", filetypes =[('Archivo de texto', '*.txt')])
    if fp:
        data=fp.readlines()
        txtbox_init_state.delete(0,END)
        txtbox_rule.delete(0,END)
        txtbox_time.delete(0,END)
        txtbox_color.delete(0,END)
        txtbox_init_state.insert(0,data[0].rstrip("\n"))
        txtbox_rule.insert(0,data[1].rstrip("\n"))
        txtbox_time.insert(0,data[2].rstrip("\n"))
        txtbox_color.insert(0,data[3])

#-----------------------------Generar configuracion aleatoria----------------------------------
def random_config(txtbox_init_state,txtbox_rule,txtbox_time,txtbox_color):
    txtbox_init_state.delete(0,END)
    txtbox_rule.delete(0,END)
    txtbox_time.delete(0,END)
    txtbox_color.delete(0,END)
    txtbox_rule.insert(0,random.randint(0,255))
    txtbox_time.insert(0,random.randint(1,1000))
    random_len_state=random.randint(1,1000)
    random_state=""
    for cell in range(0,random_len_state):
        random_cell=random.random()
        if random_cell<0.5:
            random_state+='0'
        else:
            random_state+='1'
    txtbox_init_state.insert(0,random_state)
    random_color=str(random.randint(0,255))+" "+str(random.randint(0,255))+" "+str(random.randint(0,255))
    txtbox_color.insert(0,random_color)

#-----------------------------Imprimir el numero de celulas por anillo----------------------------------
def print_ncells(scrlledtxt_ncells, automata):
    ncells=number_cells(automata)
    scrlledtxt_ncells.configure(state="normal")
    scrlledtxt_ncells.delete(1.0,END)
    for element in ncells:
        scrlledtxt_ncells.insert(tk.INSERT,element)
    scrlledtxt_ncells.configure(state="disable")

#-----------------------------Seleccionar color----------------------------------
def choose_color(colortxt):
    color=ColorChooser.askcolor(title="Selecciona el color de la celula")
    colortxt.delete(0,END)
    colortxt.insert(0,color[0])

#-----------------------------Crear mapa de color para el automata----------------------------------
def create_colormap(color):
    rgb=tuple(re.findall('\S+',color))
    cell_colors=[(255,255,255),rgb]
    cell_colors=[(float(element[0])/255.0, float(element[1])/255.0,float(element[2])/255.0) for element in cell_colors]
    cmap=colors.ListedColormap(cell_colors)
    return cmap

#-----------------------------Interfaz del simulador----------------------------------
def ac_gui():
    #-----------------------------Crear widget root (Master frame)----------------------------------
    root = tk.Tk()
    root.wm_title("Automata Celular")
    #-----------------------------Inicializacion de variables de los widgets----------------------------------
    state = tk.StringVar()
    rule= tk.IntVar()
    time= tk.IntVar(root, value=1)
    color=tk.StringVar(root, value="0 0 0")

    #------------------------------Crear frame---------------------------------
    fig= Figure( dpi=100 ,figsize=(8,6) )

    #-----------------------------Crear area de dibujo de Tkinter----------------------------------
    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    #-----------------------Anadir barra de herramientas--------------------------
    toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.LEFT, expand=1)

    #-----------------------Definicion de widgets del simulador--------------------------
    label_initialstate=tk.Label(root, text="Ingrese el estado inicial")
    label_initialstate.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    entry_initialstate=tk.Entry(master=root, bg='white', textvariable=state)
    entry_initialstate.pack(side=tk.TOP, after=label_initialstate,fill=tk.X)
    
    label_rule=tk.Label(root, text="Ingrese la regla del AC")
    label_rule.pack(side=tk.TOP, after=entry_initialstate,fill=tk.X, expand=1)

    entry_rule=tk.Entry(master=root, bg='white', textvariable=rule)
    entry_rule.pack(side=tk.TOP, after=label_rule,fill=tk.X, expand=1)

    label_time=tk.Label(root, text="Ingrese las iteraciones del AC")
    label_time.pack(side=tk.TOP, after=entry_rule,fill=tk.X, expand=1)
    
    entry_time=tk.Entry(master=root, bg='white', textvariable=time)
    entry_time.pack(side=tk.TOP, after=label_time,fill=tk.X)

    label_color=tk.Label(root, text="Color de las celular RGB")
    label_color.pack(side=tk.TOP, after=entry_time,fill=tk.X, expand=1)
    
    entry_color=tk.Entry(master=root, bg='white', textvariable=color)
    entry_color.pack(side=tk.TOP, after=label_color,fill=tk.X)

    color_button = tk.Button(master=root, text="Seleccionar color", command=lambda:choose_color(entry_color))
    color_button.pack(side=tk.TOP, after=entry_color,fill=tk.X, expand=1)

    plot_button = tk.Button(master=root, text="Dibujar Automata", command=lambda:plot_automata(fig,state,rule,time,numcells_scrlledtxt,color))
    plot_button.pack(side=tk.TOP, after=color_button,fill=tk.X, expand=1)

    random_button = tk.Button(master=root, text="Randomizar Opciones", command=lambda:random_config(entry_initialstate,entry_rule,entry_time,entry_color))
    random_button.pack(side=tk.TOP, after=plot_button,fill=tk.X, expand=1)
    
    save_button = tk.Button(master=root, text="Guardar Configuracion", command=lambda:save_config(state,rule,time,color))
    save_button.pack(side=tk.TOP, after=random_button,fill=tk.X, expand=1)
    
    close_button = tk.Button(master=root, text="Cerrar", command=lambda:cerrar(root))
    close_button.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    load_button = tk.Button(master=root, text="Cargar Configuracion", command=lambda:load_config(entry_initialstate,entry_rule,entry_time,entry_color))
    load_button.pack(side=tk.TOP, before=close_button,fill=tk.X, expand=1)

    numcells_scrlledtxt=st.ScrolledText(master=root, width=30, height=20, state="disable")
    numcells_scrlledtxt.pack(side=tk.TOP, after=close_button)
    
    tk.mainloop()

#-----------------------Inicializacion del simulador--------------------------
if __name__ == "__main__":
    ac_gui()