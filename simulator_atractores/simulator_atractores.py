import itertools as it
import networkx as nx
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pygraphviz as pgv


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

dicc=[0,1]
long=2
lista=[list(elem) for elem in list(it.product(dicc,repeat=long))]

rule=decode_rules(54)

nodos=[]
aristas=[]

for vertice in lista:
    while True:
        next=[int(elem) for elem in next_state(rule,vertice)]
        verticeStr=int(''.join(map(str,vertice)),2)
        nextStr=int(''.join(map(str,next)),2)
        if (verticeStr,nextStr) in aristas:
            break
        nodos.append(verticeStr)
        aristas.append((verticeStr,nextStr))
        vertice=next

G=nx.Graph()
G.add_nodes_from(nodos)
G.add_edges_from(aristas)

pos = nx.nx_agraph.graphviz_layout(G, prog='twopi', args='')

plt.figure(figsize=(8, 8))
nx.draw_networkx(G,pos,node_size=50,font_size=6, arrows=True, arrowsize=6)
plt.axis('equal')
plt.show()

def ac_gui():
    #-----------------------------Crear widget root (Master frame)----------------------------------
    root = tk.Tk()
    root.wm_title("Diagrama de ciclos")
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
    label_rule=tk.Label(root, text="Ingrese la regla del AC")
    label_rule.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    entry_rule=tk.Entry(master=root, bg='white', textvariable=state)
    entry_rule.pack(side=tk.TOP, after=label_rule,fill=tk.X)
    
    label_len=tk.Label(root, text="Ingrese la regla del AC")
    label_len.pack(side=tk.TOP, after=entry_rule,fill=tk.X, expand=1)

    entry_len=tk.Entry(master=root, bg='white', textvariable=rule)
    entry_len.pack(side=tk.TOP, after=label_len,fill=tk.X, expand=1)

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

    random_button = tk.Button(master=root, text="Randomizar Opciones", command=lambda:random_config(entry_rule,entry_rule,entry_time,entry_color))
    random_button.pack(side=tk.TOP, after=plot_button,fill=tk.X, expand=1)
    
    save_button = tk.Button(master=root, text="Guardar Configuracion", command=lambda:save_config(state,rule,time,color))
    save_button.pack(side=tk.TOP, after=random_button,fill=tk.X, expand=1)
    
    close_button = tk.Button(master=root, text="Cerrar", command=lambda:cerrar(root))
    close_button.pack(side=tk.TOP, fill=tk.X, expand=1)
    
    load_button = tk.Button(master=root, text="Cargar Configuracion", command=lambda:load_config(entry_rule,entry_rule,entry_time,entry_color))
    load_button.pack(side=tk.TOP, before=close_button,fill=tk.X, expand=1)

    numcells_scrlledtxt=st.ScrolledText(master=root, width=30, height=20, state="disable")
    numcells_scrlledtxt.pack(side=tk.TOP, after=close_button)
    
    tk.mainloop()

#-----------------------Inicializacion del simulador--------------------------
if __name__ == "__main__":
    ac_gui()
