# write a program that solves sudokus
# this will not be an AI but an algorithm
# objective is to make it as efficient and fast as possible


# step 1 - define the shape of the puzzle and input
## we will want an array of values forming a 9x9 grid

# step 2 - define the rules of the game
    # no repetition in column / row / box

# step 3 - iterate over each empty cell
    # for each cell assign possible values
    # if only 1 value, plug that in
    # we need to remove that value from all other options recursively

# step 4 - once no alternatives left, we need to start guessing
    # how I guess, is I plug in a two number one, see if it gets solved
    # if that is false, then it must be true the other one,
    # continue solving by iterating

# Step 5 - print solution

