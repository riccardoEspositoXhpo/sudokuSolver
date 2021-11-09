# Sudoku Solver

## Why 

I often find myself doing sudokus in my spare time. However, it is often the case that I do not have the answers to my puzzles.
For this reason I decided to build an app which would solve sudokus for me, so I can reference the solution if I get stuck.

## What 

This is a web app built in python (flask) and deployed on a web server. The logic lives in python code, and is accompanied by HTML, CSS, Javascript to create the full experience.

## How

Please note the original implementation was inspired by this guide - https://becominghuman.ai/image-processing-sudokuai-opencv-45380715a629

Many of the functions used have been taken from here and adapted for my specific use. 

### Upload Image

* The user lands on index.html and is prompted to upload an image
* There are only 3 supported image types, png, jpg and jpeg. This is because we want to avoid rogue files being uploaded to the server
* The app validates that the file is valid and, if so, starts processing it

### Image Processing

* As soon as the image is loaded, we apply a Gaussian Blur to facilitate image recognition
* We find the edges of the page
* Use the knowledge of these edges to rotate and crop the image
* The image is then split into 81 sub-images, one for each cell, and saved

### Number Recognition

* The cells are processed further to facilitate number recognition
* Processings include applying grayscale to the image and converting them to black and white
* The result is a set of "cleaned" board cells with black background and white text
* These are individually passed to "pytesseract" for image recognition
* Recognizing some fallacies of the engine, we capture some common mistakes (i.e. confusing a 7 for a 1)
* The output is a sudoku puzzle array

### Stage

* We present the user with a web page showing the original image and the computer's interpretation of the image side by side
* The table cells are editable, and the user can check if the algorithm was correct
* If not, the user can modify the cells directly
* Javascript code ensures we can only enter numbers in the cells
* Once the submit button is clicked, Javascript function will loop through the latest version of the table, figure out the numbers and build a new array
* The "puzzleArray" is sent back to flask using an ajax POST request

### Solve Puzzle

* With the input confirmed, the script first validates that the puzzle is valid. This is done by ensuring that every cell has at least one option to put a number
* Assuming the puzzle is valid, it is sent to puzzleCleaner. This function loops through the cells and constructs a list of possible values that could go in there. This will drastically improve the performance of bruteSolve
* BruteSolve is a recursive algorithm that uses backtracking in order to solve the puzzle. Essentially it tries to assign a value to a cell, keeps solving the puzzle until it finds an "error" (i.e a cell that has no possible values). If that is the case, it picks a different number for the original cell
* While inefficient for humans, a script can execute this in seconds, making it an efficient way to solve the puzzle

### Solved

* A new page is rendered with the final solution to the puzzle and is displayed to the user

## How to Run

* Download or clone the repo
* Install Requirements

```
pip install -r requirements.txt

```

* Run from command line:

```

flask run

```

* App is deployed on localhost by default at 127.0.0.1:5000
