import sys
import time
import numpy as np
import pandas as pd

sys.setrecursionlimit(10000)

grids = []
solvedGrids = []
solutions = 0


# define global variables
GRID_SIZE = 9
BOX_SIZE = 3

# solve the puzzle
def main():
    # print initial puzzle state
    
    startTime = time.time()

    fileName = "sudokuMini.csv"


    importPuzzles(fileName)

    for i in  range(len(grids)):

        # I want to limit the size of the problem first
        # I the puzzleCleaner
        #then I pass the result to BruteSovle
        puzzleCleaner(i)

        bruteSolve(i)

    print(solutions)
    print(len(grids))                
    print("Time Elapsed: " + str(time.time() - startTime) + " seconds")


def importPuzzles(fileName):
    
    global grids
    global solvedGrids

    with open("sudokuSolver/" + fileName, "r") as file: 
        reader = pd.read_csv(file)
        for index,row in reader.iterrows():
            

            puzzle = list(map(int,row[0]))
            puzzle = np.reshape(puzzle, (GRID_SIZE,GRID_SIZE))
            solution = list(map(int,row[1]))
            solution = np.reshape(solution, (GRID_SIZE,GRID_SIZE))
            
            grids.append(puzzle)
            solvedGrids.append(solution)

            # arrayTest = np.reshape(listTest, dtype=int)
            


    return False


# function receives y and x position in the grid and checks if number is allowed
def possibleValues(idx, y, x, n):
    
    global grids

    # check 1 - does n exist on same row
    for i in range(GRID_SIZE):
        if grids[idx][y][i] == n:
            return False
    
    # check 2 - does n exist on same column
    for i in range(GRID_SIZE):
        if grids[idx][i][x] == n:
            return False
    
    # check 3 - does n exist in the same box
    rowStart = (y // 3) * 3
    colStart = (x // 3) * 3
    
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            if grids[idx][rowStart + i][colStart + j] == n:
                return False
    
    # n is a valid candidate
    return True


def bruteSolve(i):  

    global grids
    global solvedGrids
    global options
    global solutions
    options = []

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grids[i][y][x] == 0:
                for n in range(1, GRID_SIZE + 1):

                    # find if a number can be inserted
                    if possibleValues(i, y, x, n):
                            
                        # assign number to grid
                        grids[i][y][x] = n

                        # recursively call solve to finish puzzle
                        bruteSolve(i)

                        # if the above returns we backtrack and set it to 0
                        grids[i][y][x] = 0

                return 

    if np.array_equiv(grids[i],solvedGrids[i]):
        solutions+= 1
        print(i+1, solutions)
    
    else: 
        print("puzzle ->" + str(i) + " was not solved!")


def puzzleCleaner(i):

    global grids
    # global options

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grids[i][y][x] == 0:
                options = []
                for n in range(1, GRID_SIZE + 1):
                    if possibleValues(i, y, x, n):
                        
                        options.append(n)

                if len(options) == 1:
                    
                    grids[i][y][x] = options[0]
                    
                    # recursively call function to find unique matches
                    puzzleCleaner(i)
    
    return


if __name__ == "__main__":
    main()

                