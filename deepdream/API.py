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
    layer = request.args.get('layer')

    d = {}

    if layer != None:
 
        d['layer'] = layer
        d['maxwidth'] = 1000
    
        with open('settings.json', 'w') as file_data:
            json.dump(d, file_data)
       
    if request.method == 'GET':
        html =  """
    <div align="center">
    <h1>Dockerized Deep Dream Web Service</h1>
    

    <form action="" method=post enctype=multipart/form-data>
    <h1>Enter Email Address</h1>
    <p><input type=text name=text>

    <h1>Select layer type</h1>
    <p>"No idea which layer to select? Click this <a href="https://studiointrovert.wordpress.com/2015/07/08/deep-dreaming-layers"><b>link</b></a> to see the example outputs of layers"</p>
    <p><input type=radio name=type value=inception_3b/3x3_reduce>inception_3b/3x3_reduce<br>
    <p><input type=radio name=type value=inception_3b/5x5_reduce>inception_3b/5x5_reduce<br>
    <p><input type=radio name=type value=inception_3a/output>inception_3a/output<br>

    <p><input type=radio name=type value=inception_4a/3x3>inception_4a/3x3<br>
    <p><input type=radio name=type value=inception_4c/pool>inception_4c/pool<br>
    <p><input type=radio name=type value=inception_5a/1x1>inception_5a/1x1<br>
        
    <h1>Enter max width</h1>
    <p>(For faster processing, enter values between 500-1000)</p>
    <p><input type=text name=width>

    <h1>Upload image file</h1>
    <p> <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    <p> Your photo will be run on Deep Dream and sent back to you to the email you provided. </p>
    <p> This is because, processing on Deep Dream takes time and we do not want to keep you waiting. </p>
    <p> We will email you the photo once it is done. </p>
    </div>
                """
        return html

    elif request.method == 'POST':
        user_ID = str(randint(0,9999))
        user_emailID = request.form['text']
        user_layer_type = request.form['type']
        user_width = request.form['width']

        dct = {user_ID: [user_emailID, user_layer_type, user_width]}


        with open('userData.json', 'r') as user_jsonfile:
            data = json.load(user_jsonfile)

        data.update(dct)

        with open('userData.json', 'w') as user_jsonfile:
            json.dump(data, user_jsonfile)

        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            main_file = filename.split('.')
            main_file = user_ID + "." + main_file[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], main_file))

            html =  """
		    <div align="center">
                    <h1> Status </h1>
                    <p> Your photo will be processed and sent to your email at {} </p>
                    <p><a href="/upload/">BACK</a></p>
                    </div>
                    """.format(user_emailID)

            return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
