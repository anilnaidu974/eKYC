import os
import flask
from flask import Flask, flash, request, redirect, url_for , render_template,g,session
from flask import jsonify
import pytesseract
import PIL.Image
import dlib
import difflib
import sys
from flask import send_from_directory
import json
import click
import os
import math
import datetime
import shutil
import csv
import numpy as np
from scipy.spatial import distance
import face_recognition.api as face_recognition
import logging
from datetime import timedelta
from src.database_operations.login import validate_login
from src.utility.logfile import DvalLogger
# from pan_text_processing.ocr_pan import ocr_panCard
# from liveliness_detection.detect_blinks import detectBlink
# from gesture_detection.gesture import getGestureNumber
# from database_operations.insert_form_details import insert_form_data
from src.main.request_handler import verify_gesture, verify_document_details, verify_liveliness


app = Flask(__name__,static_url_path="/estatic", static_folder='static')
app.secret_key = "eKYC@dataval007"
# app.permanent_session_lifetime = timedelta(minutes=15)


UPLOAD_FOLDER = os.path.join(os.getcwd(),"input_images")
DATABASE_FOLDER = os.path.join(os.getcwd(),"database")
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

USERNAME = "Undefined"
_dval_logger = None
LOG_DIR = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS\


@app.route('/eKYC')
def upload_file(): 
    _dval_logger.log("Remote IP Address : "+request.remote_addr,logging.INFO)
    return render_template('signIn.html')

@app.route('/eKYC/index')
def index_page():
    return render_template('index.html', value = USERNAME)
    # if session['login_status'] == False :
    #     return render_template('signIn.html')
    # else:
    #     return render_template('index.html', value = USERNAME)

@app.route('/eKYC/success')
def finish_page():
    return render_template('success.html',value = USERNAME)
    # if session['login_status'] == False :
    #     return render_template('signIn.html')
    # else:
    #     return render_template('success.html',value = USERNAME)

@app.route('/eKYC/face')
def new_file():
    return render_template('face_verify.html',value = USERNAME)
    # if session['login_status'] == False :
    #     return render_template('signIn.html')
    # else:
    #     return render_template('face_verify.html',value = USERNAME)

@app.route('/eKYC/login')
def logout():
    # session['login_status'] = False
    global USERNAME
    USERNAME = "Undefined"
    return render_template('signIn.html')


@app.route("/eKYC/login_check", methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        global USERNAME
        USERNAME = username
        # session['login_status'] = True
        # status = validate_login(username,password)
        status = True
        return {'status': status
                }

@app.route("/eKYC/photo", methods=['POST'])
def request_photo_matches():

    if request.method == 'POST':
        
        gesture_number = request.form.get('gesture')

        if 'liveImage' not in request.files:
            print("something")
            flash('No file part')
            return redirect(request.url)

        else:

            liveImage = flask.request.files.getlist("liveImage")
            return verify_gesture(liveImage,gesture_number)
           

@app.route("/eKYC/live", methods=['POST'])
def request_live_matches():

    if request.method == 'POST':
        
        eye_blink_count = request.form.get('blinks')

        if 'liveImage' not in request.files:
            print("something")
            flash('No file part')
            return redirect(request.url)

        elif 'recodedVideo' not in request.files:

            return {'status': False,
            'eye_blink_status':False
            
            }
            
            
        else:
            videoPath = os.path.join(UPLOAD_FOLDER, 'demo.mp4')
            with open(videoPath, 'wb') as destination:
                video_stream = request.files['recodedVideo'].read()
                destination.write(video_stream)
            uploaded_img1 = flask.request.files.getlist("liveImage")
            video_status = True

            return verify_liveliness(uploaded_img1,video_status,eye_blink_count)


@app.route("/eKYC/validate", methods=['POST'])
def request_text_matches():
    if 'cardImage' not in request.files:
        print("something")
        # flash('No file part')
        pan_data = {}
        pan_data['Name'] = "None"
        pan_data['Father Name'] = "None"
        pan_data['Date of Birth'] = "None"
        pan_data['PAN'] = "None"
        return {'status': False,
                'details':pan_data
                }
    else:
        
        card_img = flask.request.files.getlist("cardImage")
        # card_img = flask.request.files.getlist("cardImage")
        name = request.form.get('name')
        fname = request.form.get('fname')
        dob = request.form.get('dob')
        pan = request.form.get('pan')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        address = {}
        address["house"] = request.form.get('house_number')
        address["street_locality"] = request.form.get('street_locality')
        address["vtc"] = request.form.get('vtc')
        address["dist"] = request.form.get('district')
        address["state"] = request.form.get('state')
        address["pc"] = request.form.get('pincode')

        document_type_value = request.form.get('document_type_value')
        if document_type_value == 'pan':
            aadhar_img = flask.request.files.getlist("aadhar")
        else:
            aadhar_img = None
        return verify_document_details(card_img,name,fname,dob,pan,mobile,email,address,document_type_value,aadhar_img)

        





########################################################################################################################
if __name__ == '__main__':
    LOG_DIR = os.path.join(os.getcwd(),'logs')

    _dval_logger = DvalLogger.get_instance()
    _dval_logger.initialise_logging(LOG_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
