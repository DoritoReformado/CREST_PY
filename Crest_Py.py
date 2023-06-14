#!/usr/bin/env python
# coding: utf-8

# In[4]:


import ee                       #Modulo de Earth Engine API
import datetime                 #Modulo que permite construir datos tipo fechas
import requests                 #Modulo que permite realizar links de descargas
import geopandas as gpd         #Modulo que permite la lectura de archivos .shp
from shapely.geometry import box #Modulo que permite extraer la informacion geografica de un shp
import rasterio                 #Modulo que permite la lectura de archivo TIF y descomponer su contenido
from rasterio.mask import mask  #Modulo que permite extraer los datos vacios en un TIF
from rasterio.transform import Affine   #Modulo que nos permite cambiar las dimensiones de una variable de rasterio
#import geemap as gee            #Modulo a emplear a futuro para la impresion de mapas
import locale 
import sys
import os
current_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_path)
import clipear as clp
import escritura as write
import Reescalar as scl
import Extensionlocal as ExtLocal
import crear    
ee.Initialize()


def Iniciar(Root):
    crear.crearDirectoriosCrest(Root)

# In[5]:
##########################################################################################################################################################
##########################################################################################################################################################
def Basics_singleImage(nombre_Archivo, shp_path, satelite, banda, Root, sistemaCoordenadas, cellsize, recortar, escalar):
    AreaShp = gpd.read_file(str(shp_path))
    areaProyecto = ee.FeatureCollection(AreaShp.__geo_interface__).geometry()
    imagen = ee.Image(str(satelite)).clip(areaProyecto)
    url = imagen.getDownloadUrl({
        'bands': [str(banda)], #dato del satelite a tratar
        'region': areaProyecto, #area limite del archivo
        'crs': 'EPSG:' + str(sistemaCoordenadas), #georeferenciacion del archivo
        'format': 'GEO_TIFF', #Formato de exportado
        'scale': 30,
    })
    response = requests.get(url)
    with open(str(Root)+'Temporales/Basics/Normal/'+str(nombre_Archivo)+'.tif', 'wb') as fd:
        fd.write(response.content)

    tif_path = str(Root)+'Temporales/Basics/Normal/'+str(nombre_Archivo)+'.tif'
    
    if recortar == True:
        output_path = str(Root)+'Temporales/Basics/Recortado/'+str(nombre_Archivo)+'.tif'
        tif_path = clp.clip_shp(tif_path, shp_path, output_path)


    if escalar == True:
        output_path = str(Root)+'Temporales/Basics/Escalado/'+str(nombre_Archivo)+'.tif'
        tif_path = scl.reescalar(tif_path, output_path, cellsize)

    

    write.escritura(tif_path,nombre_Archivo, Root,sistemaCoordenadas)
    print("Proceso terminado")


# In[6]:


##########################################################################################################################################################
##########################################################################################################################################################


def Basics_singleImage_Local(nombre_Archivo, tif_path, shp_path, Root, sistemaCoordenadas, cellsize, recortar, escalar):
    output_path = str(Root)+'Temporales/Basics/Normal/'+str(nombre_Archivo)+'.tif'
    ExtLocal.extension(tif_path, shp_path, output_path)


    #if recortar == True:
    #    output_path = str(Root)+'Temporales/Basics/Recortado/'+str(nombre_Archivo)+'.tif'
    #    tif_path = clp.clip_shp(tif_path, shp_path, output_path)


    if escalar == True:
        output_path = str(Root)+'Temporales/Basics/Escalado/'+str(nombre_Archivo)+'.tif'
        tif_path = scl.reescalar(tif_path, output_path, cellsize)


    # Abrir el archivo GeoTIFF con rasterio
    write.escritura(tif_path,nombre_Archivo, Root,sistemaCoordenadas)
    print("proceso terminado")



##########################################################################################################################################################
##########################################################################################################################################################

def Download_TimeSerie(nombre_Cuenca, nombre_Archivo, nombre_carpeta, satelite, Banda, cellsize, shp_path, start_date, end_date, MoD, Root, sistemaCoordenadas, recortar, escalar):
    AreaShp = gpd.read_file(str(shp_path))
    areaProyecto = ee.FeatureCollection(AreaShp.__geo_interface__).geometry()
    epsg_code = sistemaCoordenadas
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
            fechas.append(date+'01')
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