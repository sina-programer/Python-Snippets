# https://github.com/UB-Mannheim/tesseract/wiki  # check for the installation
from PIL import Image  # 10.3.0
import pytesseract  # 0.3.10
import numpy as np

path = "image.png"
image = Image.open(path)
matrix = np.array(image)
transcript = pytesseract.image_to_string(matrix)
print(transcript)
