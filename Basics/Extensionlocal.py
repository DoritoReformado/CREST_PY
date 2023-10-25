import geopandas as gpd
import arcpy

def extension(tif_file, shp_file, out_file):
    raster = arcpy.Raster(tif_file)
    # Cargar el archivo SHP utilizando geopandas
    shapefile = gpd.read_file(shp_file)
    extensiones = shapefile.geometry[0]

    # Obtener la extensión del shapefile
    minx, miny, maxx, maxy = extensiones.bounds

    #clipear dem mediante arcpy
    arcpy.management.Clip(raster, #cargar el raster
                          "{} {} {} {}".format(minx,miny,maxx,maxy), #extension del archivo shp
                          out_file, "", "-9999","NONE","MAINTAIN_EXTENT")

    print("Archivo recortado guardado en:", out_file)

    return out_file

