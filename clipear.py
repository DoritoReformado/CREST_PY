import rasterio
import geopandas as gpd
from rasterio.mask import mask  
from rasterio.transform import Affine

def clip_shp (tif_path, shp_path, output_path): #EN CONSTRUCCION
    # Leer el archivo TIFF
    with rasterio.open(tif_path) as src:
        # Leer el archivo shapefile
        shapefile = gpd.read_file(shp_path)

        # Obtener la geometría del shapefile (por ejemplo, la primera geometría)
        geometry = shapefile.to_crs(src.crs).geometry[0]

        # Realizar el recorte
        out_image, out_transform = mask(src, [geometry], crop=True)

        # Calcular la transformación afín con el nuevo tamaño de celda
        resx = src.transform.a
        resy = src.transform.e
        new_transform = Affine(resx, out_transform.b, out_transform.c,
                                out_transform.d, resy, out_transform.f)

        # Ruta de salida para el nuevo archivo TIFF recortado con el nuevo tamaño de celda

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
    
    
    tif_path = output_path
    return tif_path