import os
import requests

def crearDirectoriosCrest(Root):
    carpetasPrincipales = ["Basics", "Params", "States","PET", "Calibs", "Results", "Rain", "OBS","ICS","Temporales"]
    for i in range(len(carpetasPrincipales)):
        if not os.path.exists(str(Root)+str(carpetasPrincipales[i])):
            os.makedirs(str(Root)+str(carpetasPrincipales[i]))
    carpetasTemporales = ["Basics","PET", "Rain"]
    Subcarpetas = ["Normal","Escalado","Recortado"]
    for i in range(len(carpetasTemporales)):
        if not os.path.exists(str(Root)+"Temporales/"+str(carpetasTemporales[i])):
            os.makedirs(str(Root)+"Temporales/"+str(carpetasTemporales[i]))
        for j in range(len(Subcarpetas)):
            if not os.path.exists(str(Root)+"Temporales/"+str(carpetasTemporales[i])+"/"+str(Subcarpetas[j])):
                os.makedirs(str(Root)+"Temporales/"+str(carpetasTemporales[i])+"/"+str(Subcarpetas[j]))
        j=0

    # Realizar la solicitud GET para descargar el archivo
    url = "http://hydro.ou.edu/files/Crest_Workshops/CRESTModel/v2_1/crest_v2_1.exe"
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Guardar el contenido del archivo en la ubicación de destino
        with open(str(Root)+"crest_v2_1.exe", 'wb') as archivo:
            archivo.write(response.content)