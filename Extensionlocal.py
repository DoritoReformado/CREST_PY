import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np

def extension(tif_file, shp_file, out_file):
    # Cargar el archivo SHP utilizando geopandas
    shapefile = gpd.read_file(shp_file)

    # Obtener la geometría del primer polígono del archivo SHP
    geometry = shapefile.geometry[0]

    # Obtener la extensión del shapefile
    minx, miny, maxx, maxy = geometry.bounds
    width = maxx - minx
    height = maxy - miny

    # Calcular el centro del cuadrado
    center_x = (maxx + minx) / 2
    center_y = (maxy + miny) / 2

    # Calcular el lado del cuadrado como la longitud máxima entre ancho y alto
    square_size = max(width, height)

    # Calcular las coordenadas de la esquina superior izquierda del cuadrado
    square_minx = center_x - square_size / 2
    square_miny = center_y - square_size / 2

    # Leer el archivo TIF utilizando rasterio
    with rasterio.open(tif_file) as src:
        # Definir la geometría del cuadrado
        square_geometry = gpd.GeoDataFrame({'geometry': [geometry]}, crs=shapefile.crs)
        square_geometry.geometry = square_geometry.buffer(square_size / 2, cap_style=3)

        # Recortar el TIF utilizando la geometría del cuadrado
        out_image, out_transform = mask(src, square_geometry.geometry, crop=True)

        # Obtener los metadatos del TIF recortado
        out_meta = src.meta.copy()

    # Actualizar los metadatos con la nueva transformación y tamaño
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    # Guardar el TIF recortado en un nuevo archivo
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(out_image)

    print("Archivo recortado guardado en:", out_file)

    return out_file

