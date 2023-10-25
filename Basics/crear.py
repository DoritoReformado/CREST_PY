import os
import requests
import urllib.request

def crearDirectoriosCrest(Root):
    ruta_appdata = os.environ['APPDATA'] + '\\CRESTPY\\'
    carpetasPrincipales = ["Basics", "Params", "States","PET", "Calibs", "Results", "Rain", "OBS","ICS"]
    carpetasTemporales = ["Basics","PET", "Rain"]
    Subcarpetas = ["Normal","Escalado","Recortado"]

    for i in range(len(carpetasPrincipales)):
        ruta_programa = str(Root)+str(carpetasPrincipales[i])
        if not os.path.exists(ruta_programa):
            os.makedirs(ruta_programa)

    for i in range(len(carpetasTemporales)):
        ruta_temp = str(ruta_appdata)+str(carpetasTemporales[i])
        if not os.path.exists(ruta_temp):
            os.makedirs(ruta_temp)
        for j in range(len(Subcarpetas)):
            if not os.path.exists(ruta_temp+"/"+str(Subcarpetas[j])):
                os.makedirs(ruta_temp+"/"+str(Subcarpetas[j]))
        j=0

    # Realizar la solicitud GET para descargar el archivo
    url = "http://hydro.ou.edu/files/Crest_Workshops/CRESTModel/v2_1/crest_v2_1.exe"
    urllib.request.urlretrieve(url, Root+"crest_v2_1.exe")
