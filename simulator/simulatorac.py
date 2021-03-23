#IMPORTAMOS LIBRERIAS NECESARIAS.
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import automata as ac


#-----------------------------BOTÓN "cerrar"----------------------------------
def cerrar(frame):
    frame.quit()     
    frame.destroy()

def plot_automata(figure,txtbox_init_state,txtbox_rule,txtbox_time):
    init_state=[int(element) for element in list(str(txtbox_init_state.get()))]
    rule=int(txtbox_rule.get())
    time=int(txtbox_time.get())
    rule_array=ac.decode_rules(rule)
    print(init_state)
    user_automata=ac.create_automata(init_state,rule_array,time)
    a=figure.add_subplot(1,2,1).imshow(user_automata, cmap="binary", aspect="equal")#AÑADIR "subbplot"
    b=figure.add_subplot(1,2,2).imshow(user_automata, cmap="gray", aspect="equal")#AÑADIR "subbplot"
    
    return a,b
    



def ac_gui():
    root = tk.Tk()
    root.wm_title("Automata Celular")
    state = tk.StringVar()
    rule= tk.IntVar()
    time= tk.IntVar()

    #------------------------------CREAR GRAFICA---------------------------------
    fig= Figure( dpi=100 ,figsize=(8,6) )
    #fig.add_subplot(1,2,1).imshow(np.zeros((100,100),dtype=int), cmap="gray", aspect="equal")#AÑADIR "subbplot"
    #fig.add_subplot(1,2,2).imshow(np.zeros((100,100),dtype=int), cmap="binary", aspect="equal")#AÑADIR "subbplot"

    canvas = FigureCanvasTkAgg(fig, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    #-----------------------AÑADIR BARRA DE HERRAMIENTAS--------------------------
    toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.LEFT, expand=1)

    label_initialstate=tk.Label(root, text="Ingrese el estado inicial")
    label_initialstate.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    entry_initialstate=tk.Entry(master=root, bg='white', textvariable=state)
    entry_initialstate.pack(side=tk.TOP, after=label_initialstate,fill=tk.X)
    
    label_rule=tk.Label(root, text="Ingrese la regla del AC")
    label_rule.pack(side=tk.TOP, after=entry_initialstate,fill=tk.X, expand=1)

    entry_rule=tk.Entry(master=root, bg='white', textvariable=rule)
    entry_rule.pack(side=tk.TOP, after=label_rule,fill=tk.X)

    label_time=tk.Label(root, text="Ingrese las iteraciones del AC")
    label_time.pack(side=tk.TOP, after=entry_rule,fill=tk.X, expand=1)
    
    entry_time=tk.Entry(master=root, bg='white', textvariable=time)
    entry_time.pack(side=tk.TOP, after=label_time,fill=tk.X)

    plot_button = tk.Button(master=root, text="Plot", command=lambda:plot_automata(fig,state,rule,time))
    plot_button.pack(side=tk.TOP, after=entry_time,fill=tk.X, expand=1)
    
    save_button = tk.Button(master=root, text="Guardar Configuracion", command=lambda:cerrar(root))
    save_button.pack(side=tk.TOP, after=plot_button,fill=tk.X, expand=1)
    
    close_button = tk.Button(master=root, text="Cerrar", command=lambda:cerrar(root))
    close_button.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    load_button = tk.Button(master=root, text="Cargar Configuracion", command=lambda:cerrar(root))
    load_button.pack(side=tk.TOP, before=close_button,fill=tk.X, expand=1)
    
    tk.mainloop()

if __name__ == "__main__":
    ac_gui()

  
