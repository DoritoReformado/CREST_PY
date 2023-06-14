import rasterio
from rasterio.warp import reproject

def escritura(tif_path, nombre_Archivo, Root, sistemaCoordenadas):
    epsg_code = sistemaCoordenadas
    # Abrir el archivo GeoTIFF con rasterio
    with rasterio.open(tif_path) as src:      
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


def escritura_SerieTiempo(tif_path, output_path, sistemaCoordenadas):
    
    sistemaCoordenadas
    # Abrir el archivo GeoTIFF con rasterio
    with rasterio.open(tif_path) as src:      
        # Leer los datos de la banda 1 como un array NumPy
        data = src.read(1)
        if(src._nodatavals[0] == None):
            mascara = data == int(0)
            data[mascara] = -9999
        else:
            mascara = data == int(src._nodatavals[0])
            data[mascara] = -9999

        # Obtener los metadatos de la imagen
        profile = src.profile
        profile["nodata"] = -9999
        

    with open(output_path, "w") as dst:
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

    with rasterio.open(output_path, 'r+') as src:
        # Crea un objeto CRS basado en el código EPSG
        #print(src.crs)
        srs = rasterio.crs.CRS.from_epsg(sistemaCoordenadas)

        # Establece el SRS en el objeto DatasetReader
        src.crs = srs

        #return src    
        src.close()