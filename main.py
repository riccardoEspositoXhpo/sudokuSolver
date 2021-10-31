import time
import os
import glob
from copy import deepcopy

from settings import GRID_SIZE, BOX_SIZE
from imageProcessing import cropImage
from numberRecognition import extractNumberFromImage, buildPuzzleFromImage
 
solvedGrid = []


def main():

    startTime = time.time()

    # removes any files from previous runs
    cleanFiles()
    
    fileName = 'images/sudoku_3.jpg'

    # crops the image to just show the grid
    croppedImage = cropImage(fileName)

    print("Image Grid extracted")

    # extract numbers from the grid
    extractNumberFromImage(croppedImage)

    # construct a sudoku array by interpreting the numbers on the page
    rawPuzzle = buildPuzzleFromImage()

    print(rawPuzzle)
    # hardcoded for now, will be result of image processing
    rawPuzzle = [[2, 0, 0, 0, 5, 4, 0, 7, 6], [4, 0, 0, 8, 9, 0, 2, 0, 0], [7, 0, 0, 2, 0, 0, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 8, 0], [0, 0, 8, 0, 0, 0, 6, 0, 0], [0, 3, 0, 0, 0, 8, 0, 0, 1], [0, 0, 0, 0, 0, 9, 0, 0, 3], [0, 0, 4, 0, 1, 3, 0, 0, 2], [3, 9, 0, 4, 7, 0, 0, 0, 8]]

    print(rawPuzzle)
    # reduce puzzle scope
    grid, options =  puzzleCleaner(rawPuzzle)

    # apply brute force and backtracking to solve puzzle
    bruteSolve(grid,options)

    print(solvedGrid)

    print("Time Elapsed: " + str(time.time() - startTime) + " seconds")
    

def puzzleCleaner(grid):

    options = [[set() for i in range(9)] for i in range(9)]   

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possibleValues(grid, y, x, n):
                        
                        options[y][x].add(n)
        
                '''My solver logic was stupid. I need to implement some intelligent checks se ho balle
                    I think the plan is to first grab the options and then fiddle with them to reduce the scope further.
                    This should be worth a few brownie points. penseró a magical sudoku techniques '''
                # if len(options[y][x]) == 1:
                #     s = options[y][x]
                #     for e in s:
                #         break

                #     grid[y][x] = e
                    
                #     # recursively call function to find unique matches
                #     puzzleCleaner(grid)
    
    return grid, options


def bruteSolve(grid,options):  

    global solvedGrid

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                for n in list(options[y][x]):

                    # find if a number can be inserted
                    if possibleValues(grid, y, x, n):
                            
                        # assign number to grid
                        grid[y][x] = n

                        # recursively call bruteSolve to finish puzzle
                        bruteSolve(grid, options)

                        # if the above returns we backtrack and set it to 0
                        grid[y][x] = 0
                
                return
    
    solvedGrid = deepcopy(grid)


def possibleValues(grid, y, x, n):
    
    # function receives y and x position in the grid idx and checks if n is allowed

    # check 1 - does n exist on same row
    for i in range(GRID_SIZE):
        if grid[y][i] == n:
            return False
    
    # check 2 - does n exist on same column
    for i in range(GRID_SIZE):
        if grid[i][x] == n:
            return False
    
    # check 3 - does n exist in the same box
    rowStart = (y // 3) * 3
    colStart = (x // 3) * 3
    
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            if grid[rowStart + i][colStart + j] == n:
                return False
    
    # n is a valid candidate
    return True


def cleanFiles():

    for f in glob.glob('cleanedBoard/*'):
        os.remove(f)
    
    for f in glob.glob('board/*'):
        os.remove(f)

if __name__ == "__main__":
    main()

                