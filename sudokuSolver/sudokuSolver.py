import sys
import time
import numpy as np
import pandas as pd

sys.setrecursionlimit(10000)


# grid = [
#     [5,3,0,0,7,0,0,0,0],
#     [6,0,0,1,9,5,0,0,0],
#     [0,9,8,0,0,0,0,6,0],
#     [8,0,0,0,6,0,0,0,3],
#     [4,0,0,8,0,3,0,0,1],
#     [7,0,0,0,2,0,0,0,6],
#     [0,6,0,0,0,0,2,8,0],
#     [0,0,0,4,1,9,0,0,5],
#     [0,0,0,0,8,0,0,7,9]
# ]

grids = []
solvedGrids = []
solutions = 0

# define global variables
GRID_SIZE = 9
BOX_SIZE = 3

# solve the puzzle
def main():
    # print initial puzzle state
    
    importPuzzles()

    # print(grids[0])
    for i in range(len(grids)):

        solvePuzzle(grids[i],solvedGrids[i])

    print(solutions)                
        
def importPuzzles():
    
    global grids
    global solvedGrids

    with open("sudokuSolver/sudokuTiny.csv", "r") as file: 
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
def possibleValues(grid, y, x, n):
    
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


def solvePuzzle(grid, solved):  

    global grids
    global solutions

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                for n in range(1, GRID_SIZE + 1):

                    # find if a number can be inserted
                    if possibleValues(grid, y, x, n):

                        # assign number to grid
                        grid[y][x] = n

                        # recursively call solve to finish puzzle
                        solvePuzzle(grid, solved)

                        # if the above returns we backtrack and set it to 0
                        grid[y][x] = 0

                return 

    if np.array_equiv(grid,solved):
        solutions+= 1
        print(solutions)


if __name__ == "__main__":
    main()

                