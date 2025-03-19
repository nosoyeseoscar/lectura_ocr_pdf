import cv2 as cv
import pytesseract as ocr
from pdf2image import convert_from_path

# Configurar la ruta de Tesseract (si no lo agregaste al PATH)
ocr.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

# Ruta del archivo PDF.
pdf = "ejemplo.pdf"

# Convertir el PDF a imágenes.
paginas = convert_from_path(pdf)

#Extraer texto de cada página.
texto_completo = ""
for i, pagina in enumerate(paginas):
    pagina.save(f"pagina_{i}.jpg", "JPEG")
    imagen = cv.imread(f"pagina_{i}.jpg")
    texto = ocr.image_to_string(imagen)
    texto_completo += texto

# Guardar el texto en un archivo.
with open("texto.txt", "w", encoding="utf-8") as f:
    f.write(texto_completo)

print("Texto extraído y guardado en texto.txt")
