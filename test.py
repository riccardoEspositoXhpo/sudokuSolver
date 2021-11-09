from settings import GRID_SIZE, BOX_SIZE, UPLOAD_FOLDER, ALLOWED_EXTENSIONS

webPuzzle = [[0, 7, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 9, 7, 4, 0], [8, 4, 0, 2, 0, 0, 0, 6, 0], [1, 0, 0, 0, 0, 6, 0, 0, 0], [3, 9, 0, 0, 0, 0, 0, 8, 5], [0, 0, 0, 3, 0, 0, 0, 0, 1], [0, 2, 0, 0, 0, 4, 0, 9, 3], [0, 5, 8, 1, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 1, 0]]

rawPuzzle = webPuzzle


def isPuzzleValid(puzzle):
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            
            validPuzzle = False
            for n in range(1, 10):
                validPuzzle = validPuzzle or possibleValues(puzzle, i, j, n)
    
    return validPuzzle

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


if __name__ == '__main__':
    print(isPuzzleValid(rawPuzzle))