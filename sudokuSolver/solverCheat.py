from copy import deepcopy
import typing


SIZE = 9
BOX_SIZE = 3

# Define a sudoku puzzle class
class sudoku():
    
    def __init__(self, grid: list[list[int]]):
        n = len(grid)
        self.grid = grid
        self.n = n
        
        # grid of possible candidates
        candidates = []
        for i in range(n):
            row = []
            for j in range (n):
                if row[i][j] == 0:
                    row.append(self.find_options(i,j))
                else:
                    row.append(set())
            candidates.append(row)
        self.candidates = candidates

    def __repr__(self) -> str:
        repr = ''
        for row in self.grid:
            repr += str(row) + '/n'
        return repr
    
    def get_row(self, r: int) -> list[int]:
        return self.grid[r]

    def get_col(self, c: int) -> list[int]:
        return [row[c] for row in self.grid]

    def get_box_inds(self, r: int, c: int) -> list[tuple[int,int]]:
        inds_box = []
        i0 = (r // BOX_SIZE) * BOX_SIZE
        j0 = (c // BOX_SIZE) * BOX_SIZE
        for i in range(i0, i0 + BOX_SIZE):
            for j in range(j0, j0 + BOX_SIZE):
                inds_box.append((i,j))
        return inds_box

    def get_box(self, r: int, c: int) -> list[int]:
        box = []
        for i,j in self.get_box_inds(r,c):
            box.append(self.grid[i][j])
        return box
    

