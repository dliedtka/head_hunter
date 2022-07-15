#!/usr/bin/env python3

from flask import Flask, render_template, request
import pickle
import shutil
from PIL import Image, ImageDraw
import sys
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "abcdefg"

# global path to this directory 
dir_path = os.path.dirname(os.path.abspath(__file__))
# global path to dataset
dataset_dir = ""
# global counter for which image to label
img_idx = 0
# global data structure for labels
labels = []


def make_square(im, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def undo_label():
    global labels
    labels = labels[:-1]
    with open(f"{dir_path}/output/labels.pkl", "wb") as fout:
        pickle.dump(labels, fout)


def add_label(x, y, w, h):
    labels.append((x,y,w,h))
    with open(f"{dir_path}/output/labels.pkl", "wb") as fout:
        pickle.dump(labels, fout)


@app.route("/", methods=["POST", "GET"])
def index():
    '''
    This is the one and only page of the app, where you label and view labels.
    '''
    global img_idx

    if request.method == "POST":
        # undo
        if "undo" in request.form.keys():
            if img_idx > 0:
                # update data structure
                undo_label()
                img_idx -= 1
        
        # invalid submit
        elif img_idx >= len(os.listdir(dataset_dir)) or "" in [request.form.get("tl_x"), request.form.get("tl_y"), request.form.get("br_x"), request.form.get("br_y")]:
            pass
        
        # submit
        else:
            tl_x = int(request.form.get("tl_x"))
            tl_y = int(request.form.get("tl_y"))
            br_x = int(request.form.get("br_x"))
            br_y = int(request.form.get("br_y"))
            # x,y in center of image
            x = int((tl_x + br_x) / 2) - 760 # subtract constant from webpage layout
            y = int((tl_y + br_y) / 2) - 140 # subtract constant from webpage layout
            w = br_x - tl_x
            h = br_y - tl_y
            # height,width
            print (f"Top left: ({x},{y}), Width: {w}, Height: {h}")
            # update data structure
            add_label(x, y, w, h)
            # increment counter
            img_idx += 1

    # copy image just labeled to static directory
    if img_idx > 0:
        shutil.copy(f"{dataset_dir}/{os.listdir(dataset_dir)[img_idx-1]}", f"{dir_path}/static/just_labeled.jpg")
        first = False
    else:
        shutil.copy(f"{dataset_dir}/{os.listdir(dataset_dir)[img_idx]}", f"{dir_path}/static/just_labeled.jpg")
        first = True
    
    # copy image to be labeled to static directory
    if img_idx < len(os.listdir(dataset_dir)):
        shutil.copy(f"{dataset_dir}/{os.listdir(dataset_dir)[img_idx]}", f"{dir_path}/static/label_me.jpg")
        last = False
    else:
        last = True

    # modify labeled image
    last_img = Image.open(f"{dir_path}/static/just_labeled.jpg")
    # make square
    last_img = make_square(last_img)
    # resize to 500x500
    last_img = last_img.resize((500,500))
    # box coordinates
    x,y,w,h = labels[-1]
    x1 = x - int(w/2)
    y1 = y - int(h/2)
    x2 = x + int(w/2)
    y2 = y + int(h/2)
    # draw box
    box = ImageDraw.Draw(last_img)  
    box.rectangle([x1,y1,x2,y2], outline ="red")
    last_img.save(f"{dir_path}/static/just_labeled.jpg")

    # modify image to label
    if img_idx < len(os.listdir(dataset_dir)):
        cur_img = Image.open(f"{dir_path}/static/label_me.jpg")
        # make square
        cur_img = make_square(cur_img)
        # resize to 500x500
        cur_img = cur_img.resize((500,500))
        cur_img.save(f"{dir_path}/static/label_me.jpg")
        
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

    # make sure static directory exists for image display, output directory for labels
    if not os.path.exists(f"{dir_path}/static"):
        os.mkdir(f"{dir_path}/static")
    if not os.path.exists(f"{dir_path}/output"):
        os.mkdir(f"{dir_path}/output")

    # load data structure
    if os.path.exists(f"{dir_path}/output/labels.pkl"):
        with open(f"{dir_path}/output/labels.pkl", "rb") as fin:
            labels = pickle.load(fin)
    img_idx = len(labels)

    # run app
    app.run(debug=True)
