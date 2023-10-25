import arcpy
import os

def escritura(temp_file, Root, nombre_Archivo):
    raster = arcpy.Raster(temp_file)
    arcpy.conversion.RasterToASCII(raster, os.path.join(Root, nombre_Archivo+'.asc'))