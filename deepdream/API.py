#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import json
import os
from random import randint

app = Flask(__name__)

"""
/opt/deepdream/inputs/
/home/shashank/PycharmProjects/DeepDream/inputs/
"""
UPLOAD_FOLDER = '/opt/deepdream/inputs/'
ALLOWED_EXTENSIONS = set(['jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET','POST'])
def index():
    if request.method == 'GET':

        html =  """

    <h1>Upload new File</h1>
    <p>Types of layer Operations: </p>
    <p>inception_3b/3x3_reduce, inception_3b/3x3</p>
    <p>inception_4b/3x3, inception_4b/3x3_reduce</p>
    <p>inception_4b/5x5_reduce, inception_4b/5x5</p>

    <form action="" method=post enctype=multipart/form-data>
    <h1>Enter Email Address</h1>
    <p><input type=text name=text>
    <h1>Upload image file</h1>
    <p> <input type=file name=file>
        <input type=submit value=Upload>
    </form>

    <p> Your photo will be run on Deep Dream and sent back to you the email you provided. </p>
    <p> This is because, processing on Deep Dream takes time and we do not want to keep you waiting </p>
    <p> We will email you the photo once it is done </p>

                """
        return html

    elif request.method == 'POST':
        user_ID = str(randint(0,9999))
        user_emailID = request.form['text']

        dct = {user_ID: user_emailID}

        with open('userData.json', 'r') as user_jsonfile:
            data = json.load(user_jsonfile)

        data.update(dct)

        with open('userData.json', 'w') as user_jsonfile:
            json.dump(data, user_jsonfile)

        """
        user_textfile = open("userData.txt", "a")
        user_textfile.write( "{}--{}\n".format(user_ID,user_emailID))
        user_textfile.close()
        """

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            main_file = filename.split('.')
            main_file = user_ID + "." + main_file[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], main_file))

            html =  """
                    <h1> Status </h1>
                    <p> Your photo will be processed and sent to your email at {} </p>
		    <p><a href="/upload/">BACK</a></p>
                    """.format(user_emailID)

            return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
