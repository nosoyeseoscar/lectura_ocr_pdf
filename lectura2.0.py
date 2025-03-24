import cv2 as cv
import pytesseract as ocr
from pdf2image import convert_from_path
import os
import shutil
import json

# Configurar la ruta de Tesseract (si no lo agregaste al PATH)
ocr.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Procedimiento que mejora la calidad de la imagen.
def escala_grises(imagen):
    # Convertir a escala de grises.
    gris = cv.cvtColor(imagen, cv.COLOR_BGR2GRAY)
    # Aplicar umbral adaptativo, en caso necesario.
    # umbral = cv.adaptiveThreshold(gris, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    return gris

# Ruta del archivo PDF y carpeta temporales.
pdf = "ejemplo.pdf"
temporales = "./temp"

# Convertir el PDF a imágenes.
paginas = convert_from_path(pdf)

#crear carpeta temporales
if (os.path.exists(temporales)==False):
    os.mkdir(temporales)

# Estructura principal del JSON
resultado = {
    "prompt": "Un prompt",
    "data": []
}

#Extraer texto de cada página.
#texto_completo = ""
for i, pagina in enumerate(paginas, start=1):
    pagina.save(f"temp/pagina_{i}.jpg", "JPEG")
    imagen = cv.imread(f"temp/pagina_{i}.jpg")
    imagen = escala_grises(imagen)
    texto = ocr.image_to_string(imagen)
    lineas = texto.split("\n")
    for j, linea in enumerate(lineas, start=1):
        if linea.strip(): # Solo procesar si hay texto
            pagina_info = {
                "pagina": i,
                "renglon": j,
                "texto": linea
            }
            resultado["data"].append(pagina_info)
    #texto_completo += texto

# Guardar el texto en un archivo.
""" with open("texto.txt", "w", encoding="utf-8") as f:
    f.write(texto_completo) """

# Guardar los datos en un archivo JSON
with open("texto.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=4)

print("Datos guardados en texto.json")    

#limpiamos temporales.
try:
    print('Limpiando temporales...')
    shutil.rmtree(temporales)
    print('Limpieza terminada')

except:
    print('No se borraron los archivos temporales')

print("Texto extraído y listo para procesarse.")
