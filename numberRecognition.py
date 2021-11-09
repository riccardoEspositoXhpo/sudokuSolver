"""
Predict an image
accepts image grid
return predicted grid
"""
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pytesseract

from settings import GRID_SIZE
from imageProcessing import scaleAndCenter


# for Windows users
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'




def extractNumberFromImage(img_grid):

    # ensure the directory exists or create it
    path = 'cleanedBoard/'

    if not os.path.exists(path):
        os.makedirs(path)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            image = img_grid[i][j]
            image = cv2.resize(image, (140, 140))
            
            thresh = 127  # mid point between 0 and 255
            

            # threshold the image
            gray = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
            
            # a typical processed sudoku square will contain borders. We eliminate them to simplify contour finding
            cutoff = 9 # 5% of size
            grayCropped = gray[cutoff:140-cutoff,cutoff:140-cutoff]

            # Find contours
            cnts = cv2.findContours(grayCropped, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)

                if (x < 10 or y < 10 or h < 10 or w < 10):
                    # Note the number is always placed in the center
                    # Since image is 140 x 140
                    # the number will be in the center
                    continue
                ROI = grayCropped[y:y + h, x:x + w]
                ROI = scaleAndCenter(ROI, 120)

                blackAndWhite = cv2.bitwise_not(ROI)
                # display_image(ROI)

                # Writing the cleaned cells
                cv2.imwrite("cleanedBoard/cell{}{}.png".format(i, j), blackAndWhite)
                

    return


def buildPuzzleFromImage():

    sudoku = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    
    xconfigs = '--psm 6 digits -c page_separator='''
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            
            cellName = 'cleanedBoard/cell{}{}.png'.format(i,j)
            exists = os.path.exists(cellName)
                    
            if not exists:

                sudoku[i][j] = 0
            
            else:
                
                cellImg = cv2.imread(cellName)
                string = pytesseract.image_to_string(cellImg, config = xconfigs)

                number = string.rstrip()
                
                # a 7 could be interpreted as a 1, but not viceversa
                # running a 7 with --psm 8 ensures it is captured properly, but won't work for other digits
                if number == '1' or number == '':
                    
                    string = pytesseract.image_to_string(cellImg, config = '--psm 8 digits -c page_separator=''' )
                    newNumber = string.rstrip()
                    
                    if newNumber == 7:
                        number = newNumber

                # if after the manipulation the string is still empty, we plug a zero
                try: 
                    number = int(number)

                except ValueError:
                    number = 0
                
                # Sources for image recognition
                # https://stackoverflow.com/questions/42881884/python-read-number-in-image-with-pytesseract
                # https://github.com/tesseract-ocr/tesseract/issues/3110 

                sudoku[i][j] = number

    return sudoku

# sudoku = buildPuzzleFromImage()