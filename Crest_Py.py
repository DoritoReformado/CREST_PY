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
import geemap as gee            #Modulo a emplear a futuro para la impresion de mapas
import locale                   
ee.Initialize()
locale.setlocale(locale.LC_ALL, 'es_ES')

# In[5]:
##########################################################################################################################################################
##########################################################################################################################################################
def Basics_singleImage(nombre_Cuenca, nombre_Archivo, shp_path, satelite, banda, cellsize, Root, sistemaCoordenadas):
    AreaShp = gpd.read_file(str(shp_path))
    areaProyecto = ee.FeatureCollection(AreaShp.__geo_interface__).geometry()
    imagen = ee.Image(str(satelite)).clip(areaProyecto)
    epsg_code = sistemaCoordenadas
    url = imagen.getDownloadUrl({
        'bands': [str(banda)], #dato del satelite a tratar
        'region': areaProyecto, #area limite del archivo
        'crs': 'EPSG:' + str(epsg_code), #georeferenciacion del archivo
        'crs_transform': [cellsize, 0, 0, 0, -cellsize, 0], #Delimitacion del tamaño de celda
        'format': 'GEO_TIFF', #Formato de exportado
    })
    #print(url)
    response = requests.get(url)
    with open(str(Root)+'Temporales/Basics/'+str(nombre_Archivo)+'.tif', 'wb') as fd:
        fd.write(response.content)
    ###############################################################
    def clip_shp (): #EN CONSTRUCCION
        tamanio_celda = cellsize
        # Leer el archivo TIFF
        with rasterio.open(str(Root)+'Temporales/Basics/'+str(nombre_Archivo)+'.tif') as src:
            # Leer el archivo shapefile
            shapefile = gpd.read_file(shp_path)

            # Obtener la geometría del shapefile (por ejemplo, la primera geometría)
            geometry = shapefile.to_crs(src.crs).geometry[0]

            # Realizar el recorte
            out_image, out_transform = mask(src, [geometry], crop=True)

            # Calcular la transformación afín con el nuevo tamaño de celda
            resx = tamanio_celda
            resy = -tamanio_celda
            new_transform = Affine(resx, out_transform.b, out_transform.c,
                                out_transform.d, resy, out_transform.f)

            # Ruta de salida para el nuevo archivo TIFF recortado con el nuevo tamaño de celda
            output_path = str(Root)+'Temporales/Basics/'+str(nombre_Archivo)+'.tif'

            # Actualizar los metadatos
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": new_transform
        })
            # Guardar el nuevo archivo TIFF recortado con el nuevo tamaño de celda
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(out_image)
    ################################################################
    
    # Abrir el archivo GeoTIFF con rasterio
    with rasterio.open(str(Root)+'Temporales/Basics/'+str(nombre_Archivo)+'.tif') as src:
        
        # Leer los datos de la banda 1 como un array NumPy
        data = src.read(1).astype('int32')
        if(src._nodatavals[0] == None):
            mascara = data == int(0)
            data[mascara] = -9999
        else:
            mascara = data == int(src._nodatavals[0])
            data[mascara] = -9999

        # Obtener los metadatos de la imagen
        profile = src.profile
        profile["nodata"] = -9999
        

    with open(str(Root)+'Basics/'+str(nombre_Archivo)+'.asc', "w") as dst:
        # Escribir los metadatos en el archivo ASCII
        dst.write("ncols {}\n".format(profile["width"]))
        dst.write("nrows {}\n".format(profile["height"]))
        dst.write("xllcorner {}\n".format(profile["transform"][2]))
        dst.write("yllcorner {}\n".format(profile["transform"][5]+ (profile["height"] * profile["transform"][4])))
        dst.write("cellsize {}\n".format(profile["transform"][0]))
        dst.write("NODATA_value {}\n".format(profile["nodata"]))

        # Escribir los datos en el archivo ASCII
        for row in data:
            dst.write(" ".join(str(x) if x != row[0] else str(x).lstrip() for x in row) + "\n")

    with rasterio.open(str(Root)+'Basics/'+str(nombre_Archivo)+'.asc', 'r+') as src:
        # Crea un objeto CRS basado en el código EPSG
        #print(src.crs)
        srs = rasterio.crs.CRS.from_epsg(epsg_code)

        # Establece el SRS en el objeto DatasetReader
        src.crs = srs

        #return src    
        src.close()
    print("Proceso terminado")
# In[6]:


##########################################################################################################################################################
##########################################################################################################################################################


def Basics_singleImage_Local(nombre_Cuenca, nombre_Archivo, cellsize, tif_path, shp_path, Root, sistemaCoordenadas):
    AreaShp = gpd.read_file(str(shp_path))
    areaProyecto = ee.FeatureCollection(AreaShp.__geo_interface__).geometry()
    epsg_code = sistemaCoordenadas
    # Tamaño de celda deseado en unidades de la imagen
    tamanio_celda = cellsize  #incompatibilidad con el tamaño de celda

    # Leer el archivo TIFF
    def clip(): #En Construccion
        with rasterio.open(tif_path) as src:
            # Leer el archivo shapefile
            shapefile = gpd.read_file(shp_path)

            # Obtener la geometría del shapefile (por ejemplo, la primera geometría)
            geometry = shapefile.to_crs(src.crs).geometry[0]

            # Realizar el recorte
            out_image, out_transform = mask(src, [geometry], crop=True)

            # Calcular la transformación afín con el nuevo tamaño de celda
            resx = tamanio_celda
            resy = -tamanio_celda
            new_transform = Affine(resx, out_transform.b, out_transform.c,
                                out_transform.d, resy, out_transform.f)

            # Ruta de salida para el nuevo archivo TIFF recortado con el nuevo tamaño de celda
            output_path = str(Root)+'Temporales/Basics/'+str(nombre_Archivo)+'.tif'

            # Actualizar los metadatos
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": new_transform,
                "crs": src.crs,
                "dtype": out_image.dtype,
                "nodata": out_image.nodata,
                "compress": "lzw",
                "photometric": "RGB",
                "res": (resx, resy)
            })

           # Guardar el nuevo archivo TIFF recortado con el nuevo tamaño de celda
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(out_image)


    # Abrir el archivo GeoTIFF con rasterio
    with rasterio.open(str(Root)+'Temporales/Basics/'+str(nombre_Archivo)+'.tif') as src:
        # Leer los datos de la banda 1 como un array NumPy
        data = src.read(1).astype('int32')
        if(src._nodatavals[0] == None):
            mascara = data == int(0)
            data[mascara] = -9999
        else:
            mascara = data == int(src._nodatavals[0])
            data[mascara] = -9999
        # Obtener los metadatos de la imagen
        profile = src.profile
        
        # Actualizar el tamaño de celda en el perfil
        new_transform = rasterio.Affine(tamanio_celda, profile["transform"][1], profile["transform"][2],
                                    profile["transform"][3], -tamanio_celda, profile["transform"][5])
        profile["transform"] = new_transform

        profile["nodata"] = -9999


    with open(str(Root)+'Basics/'+str(nombre_Archivo)+'.asc', "w") as dst:
        # Escribir los metadatos en el archivo ASCII
        dst.write("ncols {}\n".format(profile["width"]))
        dst.write("nrows {}\n".format(profile["height"]))
        dst.write("xllcorner {}\n".format(profile["transform"][2]))
        dst.write("yllcorner {}\n".format(profile["transform"][5] + (profile["height"] * profile["transform"][4])))
        dst.write("cellsize {}\n".format(profile["transform"][0]))
        dst.write("NODATA_value {}\n".format(profile["nodata"]))

        # Escribir los datos en el archivo ASCII
        for row in data:
            dst.write(" ".join(str(x) if x != row[0] else str(x).lstrip() for x in row) + "\n")
    
    with rasterio.open(str(Root)+'Basics/'+str(nombre_Archivo)+'.asc', 'r+') as src:
        # Crea un objeto CRS basado en el código EPSG
        #print(src.crs)
        srs = rasterio.crs.CRS.from_epsg(epsg_code)

        # Establece el SRS en el objeto DatasetReader
        src.crs = srs

        #return src   
        src.close()
    print("proceso terminado")



##########################################################################################################################################################
##########################################################################################################################################################

def Download_TimeSerie(nombre_Cuenca, nombre_Archivo, nombre_carpeta, satelite, scope, cellsize, shp_path, start_date, end_date, MoD, Root, sistemaCoordenadas):
    AreaShp = gpd.read_file(str(shp_path))
    areaProyecto = ee.FeatureCollection(AreaShp.__geo_interface__).geometry()
    tamanio_celda = cellsize 
    epsg_code = sistemaCoordenadas
    # Carga la colección de imágenes Landsat 8 Surface Reflectance
    collection = ee.ImageCollection(str(satelite)) \
        .filterBounds(areaProyecto) \
        .filterDate(start_date, end_date) \
        .sort(str(scope))

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
            'bands': [str(scope)],
            'region': areaProyecto,
            'crs': 'EPSG:' + str(epsg_code),
            'crs_transform': [cellsize, 0, 0, 0, -cellsize, 0],
            'format': 'GEO_TIFF',
        })
        #print(url)
        response = requests.get(url)
        with open(str(Root)+'Temporales/'+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif', 'wb') as fd:
            fd.write(response.content)
        #print(i)
        def clip(): #EN CONST
            # Leer el archivo TIFF
            with rasterio.open(str(Root)+'Temporales/'+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif') as src:
                # Leer el archivo shapefile
                shapefile = gpd.read_file(shp_path)

                # Obtener la geometría del shapefile (por ejemplo, la primera geometría)
                geometry = shapefile.to_crs(src.crs).geometry[0]

                # Realizar el recorte
                out_image, out_transform = mask(src, [geometry], crop=True)

                # Calcular la transformación afín con el nuevo tamaño de celda
                resx = tamanio_celda
                resy = -tamanio_celda
                new_transform = Affine(resx, out_transform.b, out_transform.c,
                                    out_transform.d, resy, out_transform.f)

                # Ruta de salida para el nuevo archivo TIFF recortado con el nuevo tamaño de celda
                output_path = str(Root)+'Temporales/'+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif'

                # Actualizar los metadatos
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": new_transform
                })
            
                # Guardar el nuevo archivo TIFF recortado con el nuevo tamaño de celda
                with rasterio.open(output_path, "w", **out_meta) as dest:
                    dest.write(out_image)

        #print(i)
        # Abrir el archivo GeoTIFF con rasterio
        with rasterio.open(str(Root)+'Temporales/'+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.tif') as src:
            # Leer los datos de la banda 1 como un array NumPy
            data = src.read(1).astype('int32')
            if(src._nodatavals[0] == None):
                mascara = data == int(0)
                data[mascara] = -9999
            else:
                mascara = data == int(src._nodatavals[0])
                data[mascara] = -9999
            # Obtener los metadatos de la imagen
            profile = src.profile
            
            # Actualizar el tamaño de celda en el perfil
            new_transform = rasterio.Affine(tamanio_celda, profile["transform"][1], profile["transform"][2],
                                        profile["transform"][3], -tamanio_celda, profile["transform"][5])
            profile["transform"] = new_transform

            profile["nodata"] = -9999
        #print(i)
        with open(str(Root)+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.asc', "w") as dst:
            # Escribir los metadatos en el archivo ASCII
            dst.write("ncols {}\n".format(profile["width"]))
            dst.write("nrows {}\n".format(profile["height"]))
            dst.write("xllcorner {}\n".format(profile["transform"][2]))
            dst.write("yllcorner {}\n".format(profile["transform"][5]+ (profile["height"] * profile["transform"][4])))
            dst.write("cellsize {}\n".format(profile["transform"][0]))
            dst.write("NODATA_value {}\n".format(profile["nodata"]))
            # Escribir los datos en el archivo ASCII
            for row in data:
                dst.write(" ".join(str(x) if x != row[0] else str(x).lstrip() for x in row) + "\n")
            print(i)

    # Crear un archivo ASCII a partir de los datos de la imagen
    for i in range(collection.size().getInfo()):
        with rasterio.open(str(Root)+str(nombre_carpeta)+'/'+str(nombre_Cuenca)+'.'+str(nombre_Archivo)+'.'+str(fechas[i])+'.asc', 'r+') as src:
            # Crea un objeto CRS basado en el código EPSG
            #print(src.crs)
            srs = rasterio.crs.CRS.from_epsg(epsg_code)

            # Establece el SRS en el objeto DatasetReader
            src.crs = srs  
            src.close()
    print("proceso terminado")