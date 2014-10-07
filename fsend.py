#!/usr/bin/python

import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import uuid

UPLOAD_FOLDER = '.'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_request
def before_request():
    if request.get_data() != '':
        rdm = uuid.uuid4().get_hex()
        os.makedirs(rdm)
        file = open(UPLOAD_FOLDER + '/' + rdm + request.path, 'w+')
        file.write(request.get_data())
        file.close()
        return '\nhttp://' + request.host + '/' + rdm + '\n'

@app.route('/<string:hashstr>/<string:filename>', methods=['GET'])
def return_file(hashstr, filename):
    return send_from_directory(UPLOAD_FOLDER + '/' + hashstr, filename)

@app.route('/<string:hashstr>', methods=['GET'])
def middleware(hashstr):
    return redirect(hashstr + '/' + os.listdir(hashstr)[0])

if __name__ == "__main__":
    app.run(debug=True)
