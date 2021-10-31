import pytesseract
import cv2
import os
import pathlib


print(pathlib.Path(__file__).parent.resolve())
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

xconfigs = '--psm 8 digits -c page_separator='''


# img = cv2.imread('cleanedBoard/cell33.png')
#img = cv2.imread('cleanedBoard/cell55.png')
img = cv2.imread('cleanedBoard/cell30.png')

text = pytesseract.image_to_string(img, config = xconfigs)

print(text)

# https://stackoverflow.com/questions/42881884/python-read-number-in-image-with-pytesseract
# https://github.com/tesseract-ocr/tesseract/issues/3110 
# magic trick stolen from h

print(os.getcwd())
