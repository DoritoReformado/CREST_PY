#!/usr/bin/env python
# coding: utf-8

# In[4]:

import sys
import os
import ee                               #Modulo de Earth Engine API
import arcpy                            #Modulo ESRI Arcpy para el tratamiento de datos
import datetime                         #Modulo que permite construir datos tipo fechas
import urllib.request                   #Modulo que permite realizar links de descargas
import geopandas as gpd                 #Modulo que permite la lectura de archivos .shp
from shapely.geometry import box        #Modulo que permite extraer la informacion geografica de un shp
import rasterio                         #Modulo que permite la lectura de archivo TIF y descomponer su contenido
from rasterio.mask import mask          #Modulo que permite extraer los datos vacios en un TIF
from rasterio.transform import Affine   #Modulo que nos permite cambiar las dimensiones de una variable de rasterio
import Basics.clipear as clp
import Basics.escritura as write
import Basics.Reescalar as scl
import Basics.Extensionlocal as ExtLocal
import Basics.crear as crear
ee.Initialize()

Valores_Base = {
    'DEM': {'Nombre': 'DEM','nombre_Carpeta': 'Basics','Satelite': 'WWF/HydroSHEDS/03VFDEM', 'Banda': 'b1'},
    'FDR': {'Nombre': 'FDR','nombre_Carpeta': 'Basics','Satelite': 'WWF/HydroSHEDS/03DIR', 'Banda': 'b1'},
    'FAC': {'Nombre': 'FAC','nombre_Carpeta': 'Basics','Satelite': 'WWF/HydroSHEDS/15ACC', 'Banda': 'b1'},
    'PETs': {'Nombre': 'pet','nombre_Cuenca': '', 'nombre_Carpeta': 'PETs', 'Satelite': 'NASA/FLDAS/NOAH01/C/GL/M/V001', 'Banda': 'Evap_tavg'},
    'Rains': {'Nombre': 'rain','nombre_Cuenca': '', 'nombre_Carpeta': 'Rains', 'Satelite': 'NASA/FLDAS/NOAH01/C/GL/M/V001', 'Banda': 'Rainf_f_tavg'}
}

def nombreCuenca(nombre):
    input("Defina el nombre de la cuenca")
    Valores_Base['PET']['nombre_Cuenca'] = nombre
    Valores_Base['Rain']['nombre_Cuenca'] = nombre
    
def escritura(temp_file, Root, nombre_Archivo):
    raster = arcpy.Raster(temp_file)
    arcpy.conversion.RasterToASCII(raster, os.path.join(Root, nombre_Archivo+'.asc'))

def Iniciar(Root):
    Folder_Base = Root
    crear.crearDirectoriosCrest(Root)

temporal_folder = os.getenv('APPDATA') + '\\CRESTPY\\'

if not os.path.exists(temporal_folder):
    os.mkdir(temporal_folder)

##########################################################################################################################################################
##########################################################################################################################################################

def Basics_singleImage(nombre_Archivo, shp_path, Root, satelite = None, banda = None, cellsize = 0.0008, recortar = False, escalar = False):
    #verifica datos de entrada (no va aqui)
    if satelite == None:
        satelite = Valores_Base[nombre_Archivo]['Satelite']
    if banda == None:
        banda = Valores_Base[nombre_Archivo]['Banda']

    #descarga de la imagen por earth engin
    imagen = ee.Image(str(satelite)).clip(ee.FeatureCollection(gpd.read_file(str(shp_path)).__geo_interface__).geometry())
    url = imagen.getDownloadUrl({
        'bands': [str(banda)], #dato del satelite a tratar
        'format': 'GEO_TIFF', #Formato de exportado
    })
    
    #Descarga del archivo a una ruta temporal
    temp_file = os.path.join(temporal_folder,nombre_Archivo+'.tif')
    urllib.request.urlretrieve(url, temp_file)
    
    #pasar a formato Ascii
    escritura(temp_file, Root, nombre_Archivo)
    print("Proceso terminado")
    

##########################################################################################################################################################
##########################################################################################################################################################

def Basics_singleImage_Local(nombre_Archivo, tif_path, shp_path, Root, sistemaCoordenadas = 4326, cellsize= 0.0008, recortar = False, escalar = False):
    output_path = str(Root)+'Temporales/Basics/Normal/'+str(nombre_Archivo)+'.tif'
    tif_path = ExtLocal.extension(tif_path, shp_path, output_path)
    if recortar == True:
        output_path = str(Root)+'Temporales/Basics/Recortado/'+str(nombre_Archivo)+'.tif'
        tif_path = clp.clip_shp(tif_path, shp_path, output_path)
    if escalar == True:
        output_path = str(Root)+'Temporales/Basics/Escalado/'+str(nombre_Archivo)+'.tif'
        tif_path = scl.reescalar(tif_path, output_path, cellsize)
        print(tif_path)
    # Abrir el archivo GeoTIFF con rasterio
    write.escritura(tif_path,nombre_Archivo, Root,sistemaCoordenadas)
    print("proceso terminado")

##########################################################################################################################################################
##########################################################################################################################################################

def Download_TimeSerie(nombre_carpeta, Root, shp_path, start_date, end_date, nombre_Cuenca = None, nombre_Archivo = None, satelite = None, Banda = None, cellsize = 0.0008,  MoD = 'm', recortar = False, escalar = True):
    
    if nombre_Cuenca == None and Valores_Base['PETs']['nombre_Cuenca'] == "":
        nombreCuenca(nombre_Cuenca)
    
    if nombre_Archivo == None: 
        nombre_Archivo = Valores_Base[nombre_carpeta]['Nombre']
    
    if satelite == None:
        satelite = Valores_Base[nombre_carpeta]['Satelite']
    
    if Banda == None:
        Banda = Valores_Base[nombre_carpeta]['Banda']
    
    AreaShp = gpd.read_file(str(shp_path))
    areaProyecto = ee.FeatureCollection(AreaShp.__geo_interface__).geometry()
    # Carga la colección de imágenes Landsat 8 Surface Reflectance
    collection = ee.ImageCollection(str(satelite)) \
        .filterBounds(areaProyecto) \
        .filterDate(start_date, end_date) \
        .sort(str(Banda))

    # Imprime el número de imágenes en la colección
    #print('Número de imágenes en la colección:', collection.size().getInfo())
    fechas = []
    # Descarga cada imagen de la colección
    for i in range(collection.size().getInfo()):
        # Obtiene la imagen actual de la colección
        image = ee.Image(collection.toList(collection.size()).get(i))

        # Obtiene la fecha de la imagen actual
        if (MoD == "m"):
            date = ee.Date(image.get('system:time_start')).format('YYYYMM').getInfo()
            fechas.append(date)
        else:
            date = ee.Date(image.get('system:time_start')).format('YYYYMMDD').getInfo()
            fechas.append(date)
        #print(date)

    # Crear un archivo ASCII a partir de los datos de la imagen
    for i in range(collection.size().getInfo()):
        #for i in range(10):
        #print(i)
        #print('collection size ' + str(collection.size().getInfo()))
        url = image.getDownloadUrl({
            'bands': [str(Banda)],
            'region': areaProyecto,
            'crs': 'EPSG:' + str(epsg_code),
            'scale':30,
            'format': 'GEO_TIFF',
        })
        #print(url)
        response = requests.get(url)
        tif_path = str(Root)+'Temporales/'+str(nombre_carpeta)+'/Normal/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif'
        with open(tif_path, 'wb') as fd:
            fd.write(response.content)
        #print(i)
        if recortar == True:
            output_path = str(Root)+'Temporales/'+str(nombre_carpeta)+'/Recortado/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif'
            tif_path = clp.clip_shp(tif_path, shp_path, output_path)


        if escalar == True:
            output_path = str(Root)+'Temporales/'+str(nombre_carpeta)+'/Escalado/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif'
            tif_path = scl.reescalar(tif_path, output_path, cellsize)
        output_path = str(Root)+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.asc'
        # Guardar el nuevo archivo TIFF recortado con el nuevo tamaño de celda
        write.escritura_SerieTiempo(tif_path, output_path, sistemaCoordenadas)
    print("proceso terminado")