#Estado inicial del modelo

Actualmente existen ciertos bugs que deben ser corregidos, en un principio cuando se importan archivos locales del computador como tifs existe la tendencia de descuadrar la escala del tif impidiendo la correcta aplicacion del modelo. En segunda instancia existe la problematica de tener muchas veces la misma funcion por lo que sintetizar funciones podria reducir la carga de trabajo de futuros cambios. tambien, la generacion de un corte a los archivos en el area de proyecto requerida generan un reescalado que no es deseado, esos serian los problemas que subyacen en la generacion de archivos en este modelo inicial. Futuros Commits trabajaran estos apartados y el release alpha 0.1 deberia permitir al usuario mediante la generacion de las carpetas correspondientes y los Tifs necesarios el correr el modelo de forma nativa.

En proximas funcionalidades deben poder crearse archivos para la calibracion del modelo y finalmente que el modelo pueda ser corrido nativamente en python, el producto final es la posibilidad de descargar esta libreria y que todo corra nativamente, opcionalmente se podria omitir el modelo crest.exe implementando el ejecutable directamente en el archivo pero esto requerira ayuda profesional. de momento los insumos infaltables para la construccion de un modelo crest serian.

1. un shp de la ubicacion del proyecto
2. el tamaño de la celda 
3. el caso de analisis (simulacion o calibracion //demas casos de analisis a trabajar en el futuro)
4. en caso de querer correr una simulacion los parametros necesarios estandarizados en un txt, la idea es poder estandarizar todo con un mascara de calibracion.