#IMPORTAMOS LIBRERIAS NECESARIAS.
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

#------------------------------CREAR VENTANA---------------------------------
root = tk.Tk()
root.wm_title("Automata Celular")


#------------------------------CREAR GRAFICA---------------------------------
ac= Figure( dpi=100 ,figsize=(8,6) )
ac.add_subplot(1,2,1).imshow(np.zeros((100,100),dtype=int), cmap="gray", aspect="equal")#AÑADIR "subbplot"
ac.add_subplot(1,2,2).imshow(np.zeros((100,100),dtype=int), cmap="binary", aspect="equal")#AÑADIR "subbplot"

canvas = FigureCanvasTkAgg(ac, master=root)  # CREAR AREA DE DIBUJO DE TKINTER.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


#-----------------------AÑADIR BARRA DE HERRAMIENTAS--------------------------
toolbar = NavigationToolbar2Tk(canvas, root)# barra de iconos
toolbar.update()
canvas.get_tk_widget().pack(side=tk.LEFT, expand=1)


#-----------------------------BOTÓN "cerrar"----------------------------------
def cerrar():
    root.quit()     
    root.destroy()

close_button = tk.Button(master=root, text="cerrar", command=cerrar)
close_button.pack(side=tk.TOP, fill=tk.X, expand=1)
save1_button = tk.Button(master=root, text="Gssssardar", command=cerrar)
save1_button.pack(side=tk.TOP, before=close_button,fill=tk.X, expand=1)
save_button = tk.Button(master=root, text="GUardar", command=cerrar)
save_button.pack(side=tk.TOP, before=close_button,fill=tk.X, expand=1)



tk.mainloop()