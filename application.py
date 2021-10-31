import os
import time
import glob
from copy import deepcopy

from flask import Flask, redirect, render_template, request, url_for, flash, session
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

    if request.method == "POST":

        # check if the post request has the file part
        if 'file' not in request.files:
 
            flash('No file part')
 
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.

        if file.filename == '':

            flash('No selected file')

            return redirect(request.url)

        if file and allowed_file(file.filename):
            
            startTime = time.time()

            # TODO - alert the user that we are working
             
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # remember fileName for other routes
            session['fileName'] = filename

            # # crops the image to just show the grid
            croppedImage = cropImage('images/'+ filename)
            print("Image Grid Cropped. Time: {} seconds.".format(time.time() - startTime))

            # extract numbers from the grid
            extractNumberFromImage(croppedImage)
            print("Number Images Extracted. Time: {} seconds.".format(time.time() - startTime))

            print("SUCCESS!")
            
            return redirect("/stage")
        
    else:

        # if I am getting this page I need to render the homePage
        return render_template("index.html")


@app.route("/stage", methods=["GET", "POST"])
def stage():

    # construct a sudoku array by interpreting the numbers on the page
    # TODO alert the user that we are working
    # rawPuzzle = buildPuzzleFromImage()

    # hardcode to speed up process
    rawPuzzle = [[2, 0, 0, 0, 5, 4, 0, 7, 6], [4, 0, 0, 8, 9, 0, 2, 0, 0], [7, 0, 0, 2, 0, 0, 0, 0, 0], [1, 0, 0, 3, 0, 0, 0, 8, 0], [0, 0, 8, 0, 0, 0, 6, 0, 0], [0, 3, 0, 0, 0, 8, 0, 0, 1], [0, 0, 0, 0, 0, 9, 0, 0, 3], [0, 0, 4, 0, 1, 3, 0, 0, 2], [3, 9, 0, 4, 7, 0, 0, 0, 8]]

    if request.method == "POST":

        
        
        return redirect("/solved")

    else:

        fileName = session.get('fileName', None)
        # if I am GETting this page I need to return the predicted puzzle
        return render_template("stage.html", fileName = fileName, rawPuzzle = rawPuzzle)


@app.route("/", methods=["GET"])
def solved():

    return render_template("solved.html")

