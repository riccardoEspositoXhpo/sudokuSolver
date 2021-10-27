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

# initialize options array of sudoku size with 9 possible options for each cell
options = [[set() for i in range(9)] for i in range(9)]


def main():

    global options

    startTime = time.time()
    fileName = "sudokuMini.csv"

    importPuzzles(fileName)

    pTimer = 0
    bTimer = 0

    for i in  range(len(grids)):
        
        # clear options array
        options = [[set() for i in range(9)] for i in range(9)]   
        
        # reduce puzzle scope
        pStart = time.time()
        puzzleCleaner(i)
        pEnd = time.time()

        pTimer += (pEnd - pStart)

        # apply brute force and backtracking
        bStart = time.time()
        bruteSolve(i)
        bEnd = time.time()

        bTimer += (bEnd - bStart)

    print(solutions)
    print(len(grids))                
    print("Time Elapsed: " + str(time.time() - startTime) + " seconds")
    print("Of Which " + str(pTimer) + " second for puzzleCleaner and " + str(bTimer) + "seconds for brute force")


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



def possibleValues(idx, y, x, n):
    
    global grids
    # function receives y and x position in the grid idx and checks if n is allowed

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

    # debugging time stats
    start = time.time()

    global grids
    global solvedGrids
    global options
    global solutions

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grids[i][y][x] == 0:
                for n in list(options[y][x]):

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
    else: 
        print("puzzle ->" + str(i) + " was not solved!")


def puzzleCleaner(i):

    global grids
    global options

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grids[i][y][x] == 0:
                for n in range(1, 10):
                    if possibleValues(i, y, x, n):
                        
                        options[y][x].add(n)
        
                if len(options[y][x]) == 1:
                    s = options[y][x]
                    for e in s:
                        break

                    grids[i][y][x] = e
                    
                    # recursively call function to find unique matches
                    puzzleCleaner(i)

    return


if __name__ == "__main__":
    main()

                