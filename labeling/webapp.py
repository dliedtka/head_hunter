#!/usr/bin/env python3

from flask import Flask, render_template
import shutil
from PIL import Image
import sys
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdefg"

# global path to this directory 
dir_path = os.path.dirname(os.path.abspath(__file__))
# global path to dataset
dataset_dir = ""
# global counter for which image to label
img_idx = 1#0


@app.route("/")
def index():
    '''
    This is the one and only page of the app, where you label and view labels.
    '''
    first, last = False, False 
    # copy image just labeled to static directory
    if img_idx > 0:
        shutil.copy(f"{dataset_dir}/{os.listdir(dataset_dir)[img_idx-1]}", f"{dir_path}/static/just_labeled.jpg")
    else:
        first = True
    # copy image to be labeled to static directory
    if img_idx < len(os.listdir(dataset_dir)):
        shutil.copy(f"{dataset_dir}/{os.listdir(dataset_dir)[img_idx]}", f"{dir_path}/static/label_me.jpg")
    else:
        last = True

    # need to get images width, shrink/expand to fit page
    last_width, last_height, cur_width, cur_height = None, None, None, None
    if img_idx > 0:
        last_im = Image.open(f"{dir_path}/static/just_labeled.jpg")
        last_width, last_height = last_im.size
    if img_idx < len(os.listdir(dataset_dir)):
        cur_im = Image.open(f"{dir_path}/static/label_me.jpg")
        cur_width, cur_height = cur_im.size
    
    # may have to scale javascript drawn box then
    print (cur_width, cur_height)

    return render_template("index.html", first=first, last=last)


if __name__ == "__main__":
    # get directory where dataset images live
    if len(sys.argv) < 2:
        print ("Give path to directory of dataset images as argument.")
        exit()
    if sys.argv[1][0] == '/':
        dataset_dir = sys.argv[1]
    elif sys.argv[1][0] == '~':
        dataset_dir = f"{os.path.expanduser('~')}/{sys.argv[1][1:]}"
    else:
        dataset_dir = f"{dir_path}/{sys.argv[1]}"
    if not os.path.isdir(dataset_dir):
        print ("Argument is not a directory.")
        exit()

    # make sure a static directory exists for web app
    if not os.path.exists(f"{dir_path}/static"):
        os.mkdir(f"{dir_path}/static")

    # run app
    app.run(debug=True)
