import rasterio

def reescalar(input_file, output_file, cellsize):
    with rasterio.open(input_file) as src:
        profile = src.profile
        transform = src.transform

        # Calcula los nuevos tamaños de ancho y alto
        new_width = int(src.width * (src.res[0] / cellsize))
        new_height = int(src.height * (src.res[1] / cellsize))

        # Actualiza los valores en el perfil
        profile.update(width=new_width, height=new_height, transform=transform * src.transform.scale(
            (src.width / new_width), (src.height / new_height)))

        # Lee los datos de la imagen y reescala
        data = src.read(out_shape=(src.count, new_height, new_width))

    # Guarda la imagen reescalada en un nuevo archivo GeoTIFF
    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(data)

    tif_path = output_file
    return tif_path