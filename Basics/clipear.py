import arcpy
import geopandas as gpd


def clip_shp (tif_path, shp_path, output_path):
    return tif_path

with arcpy.EnvManager(cellSizeProjectionMethod="PRESERVE_RESOLUTION"):
    out_raster = arcpy.sa.ExtractByMask("PruebitaLinda.tif", 
                                        r"Guarroco\Cuenca_Rio_Guarocó", 
                                        "INSIDE", 
                                        '-75.2422339545355 2.95359937879778 -74.9166666666666 3.19892586476436 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'); 
    out_raster.save(r"C:\Users\Jorge\Documents\ArcGIS\Projects\Procesamiento Informacion CREST\Procesamiento Informacion CREST.gdb\Extract_Prue1")
