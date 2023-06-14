import geopandas as gpd
import rasterio
from rasterio.mask import mask

# Ruta del archivo TIF
tif_file = "ruta_del_archivo.tif"

# Ruta del archivo SHP
shp_file = "ruta_del_archivo.shp"
def extension(tif_file, shp_file, out_file):
    # Cargar el archivo SHP utilizando geopandas
    shapefile = gpd.read_file(shp_file)

    # Obtener la geometría del primer polígono del archivo SHP
    geometry = shapefile.geometry[0]

    # Leer el archivo TIF utilizando rasterio
    with rasterio.open(tif_file) as src:
        # Recortar el TIF utilizando la geometría del polígono
        out_image, out_transform = mask(src, [geometry], crop=True)

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
