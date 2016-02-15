#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
import threading
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = '/opt/deepdream/'
ALLOWED_EXTENSIONS = set(['jpg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class MyThread(threading.Thread):
    
    def run(self):
        os.system("python deepdream.py")
        

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

    <h1>Upload new File</h1>
    <p>Pass query parameters also. IP/upload/?layer=""</p>
    <p>Types of layers: inception_3b/3x3_reduce  ,  inception_3a/3×3 , inception_4a/3×3_reduce , inception_4d/5×5 </p>

    <form action="" method=post enctype=multipart/form-data>
    <p> <input type=file name=file>
        <input type=submit value=Upload>
    </form>
                """
        return html

    elif request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            main_file = filename.split('.')
            main_file = "input" + "." + main_file[1]
	    output_file = "output.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], main_file))

            ##### TAKES TIME ##############
            newThread = MyThread()
	    newThread.start()
            ###### NEEDS THREADING #######

            return send_from_directory(app.config['UPLOAD_FOLDER'],
                               output_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



