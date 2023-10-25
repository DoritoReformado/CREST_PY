import tkinter as tk
from tkinter import ttk
class Datos:
    datos = {
        'DEM': {'Nombre': 'DEM', 'nombre_Carpeta': 'Basics', 'Satelite': 'WWF/HydroSHEDS/03VFDEM', 'Banda': 'b1'},
        'FDR': {'Nombre': 'FDR', 'nombre_Carpeta': 'Basics', 'Satelite': 'WWF/HydroSHEDS/03DIR', 'Banda': 'b1'},
        'FAC': {'Nombre': 'FAC', 'nombre_Carpeta': 'Basics', 'Satelite': 'WWF/HydroSHEDS/15ACC', 'Banda': 'b1'},
        'PETs': {'Nombre': 'pet', 'nombre_Cuenca': '', 'nombre_Carpeta': 'PETs', 'Satelite': 'NASA/FLDAS/NOAH01/C/GL/M/V001', 'Banda': 'Evap_tavg'},
        'Rains': {'Nombre': 'rain', 'nombre_Cuenca': '', 'nombre_Carpeta': 'Rains', 'Satelite': 'NASA/FLDAS/NOAH01/C/GL/M/V001', 'Banda': 'Rainf_f_tavg'}
    }

    def __init__(self):
        self.nombre_cuenca = input("Defina el nombre de la cuenca: ")
        self.datos['PETs']['nombre_Cuenca'] = self.nombre_cuenca
        self.datos['Rains']['nombre_Cuenca'] = self.nombre_cuenca
        print(self.datos)
        
    def variar_satelite(self, nombre, satelite, banda):
        self.datos[str(nombre)]['Satelite'] = satelite
        self.datos[str(nombre)]['Banda'] = banda

#data = Datos()
#Funciones

def hola():
    mensaje = caja_de_texto.get()
    print(mensaje)
    etiqueta["text"] = mensaje

#inicia la interfaz grafica
ventana = tk.Tk()
ventana.geometry("600x800")

#añadir texto en forma de etiqueta
etiqueta = tk.Label(ventana, text = 'Hola Mundo')
etiqueta.pack(fill = tk.BOTH, expand= False)

#Entrada de texto
caja_de_texto = tk.Entry(ventana, font='Arial15')
caja_de_texto.pack()

#Boton
boton = tk.Button(ventana, text = 'Boton para decir hola', command = lambda: hola())
boton.pack()



ventana.mainloop()