import os
import time
import glob
from copy import deepcopy

from flask import Flask, redirect, render_template, request, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename

# custom libraries
from settings import GRID_SIZE, BOX_SIZE, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from imageProcessing import cropImage
from numberRecognition import extractNumberFromImage, buildPuzzleFromImage
 
# global variable to host solution
solvedGrid = []

# configure application
app = Flask(__name__)

# configure app
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


# check is filename is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# define index page
@app.route("/", methods=["GET", "POST"])
def index():

    # clean lingering files
    cleanFiles()

    if request.method == "POST":

        # check if the post request has the file part
        if 'file' not in request.files:
 
            flash('No file part')
 
            return redirect('/')

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':

            flash('No selected file')

            return redirect('/')

        if file and allowed_file(file.filename):
            
            startTime = time.time()

            # TODO - alert the user that we are working
             
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # remember fileName for other routes
            session['fileName'] = filename

            # crops the image to just show the grid
            croppedImage = cropImage('static/images/'+ filename)
            print("Image Grid Cropped. Time: {} seconds.".format(time.time() - startTime))

            # extract numbers from the grid
            extractNumberFromImage(croppedImage)
            print("Number Images Extracted. Time: {} seconds.".format(time.time() - startTime))
            
            # construct a sudoku array by interpreting the numbers on the page
            rawPuzzle = buildPuzzleFromImage()
            
            # save data for next route
            session['rawPuzzle'] = rawPuzzle

            print("Puzzle Built. Time: {} seconds.".format(time.time() - startTime))
            
            return redirect("/stage")
        
    else:

        return render_template("index.html")


@app.route("/stage", methods=["GET", "POST"])
def stage():

    global solvedGrid

    if request.method == "GET":

        message = ''

        # clean lingering files
        cleanFiles()

        fileName = session.get('fileName', None)
        rawPuzzle = session.get('rawPuzzle', None)

        if isPuzzleValid(rawPuzzle) == False:

            message = 'We have detected an inconsistency with number recognition. Please amend puzzle before proceeding.'
                
        return render_template("stage.html", fileName = fileName, rawPuzzle = rawPuzzle, message = message)
   
    elif request.method == "POST":

        fileName = session.get('fileName', None)
        rawPuzzle = session.get('rawPuzzle', None)
        message = 'The puzzle has been solved!'
                   
        webPuzzle = request.get_json()
        print(webPuzzle)
        
        # the post request is being sent twice, the second time with a value of None
        if webPuzzle != None:
            
            if isPuzzleValid(webPuzzle) == True:
                
                rawPuzzle = webPuzzle

                # reduce puzzle scope
                grid, options =  puzzleCleaner(rawPuzzle)

                # apply brute force and backtracking to solve puzzle
                bruteSolve(grid,options)
            
            else:
                message = 'The puzzle provided is not valid and cannot be solved.'
                return redirect("/solved")

        # there are two requests arriving simultaenously, we allow for the block of code above to execute
        time.sleep(2)
        session['message'] = message
        
        return redirect("/solved")


@app.route("/solved", methods=["GET"])
def solved():

    global solvedGrid

    fileName = session.get('fileName', None)
    message = session.get('message', None)

    return render_template("solved.html", fileName = fileName, rawPuzzle = solvedGrid, message = message)


'''---------------------------------------------------------------------------------------------------'''

def puzzleCleaner(grid):

    if grid == None:
        return None, None

    options = [[set() for i in range(9)] for i in range(9)]   

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possibleValues(grid, y, x, n):
                        
                        options[y][x].add(n)
        
    
    return grid, options


def bruteSolve(grid,options):  

    if grid == None or options == None:
        return None

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

def isPuzzleValid(puzzle):

    # safety check for empty puzzles
    if puzzle == None:
        return True

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            
            validPuzzle = False
            for n in range(1, 10):

                validPuzzle = validPuzzle or possibleValues(puzzle, y, x, n)


    return validPuzzle