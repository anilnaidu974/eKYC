import os
import flask
from flask import Flask, flash, request, redirect, url_for , render_template,g
from flask import jsonify
import pytesseract
import PIL.Image
from PIL import Image
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
import difflib
import face_recognition.api as face_recognition
import re
import logging


from src.database_operations.login import validate_login
from src.pan_text_processing.ocr_pan import ocr_panCard
from src.liveliness_detection.detect_blinks import detectBlink
from src.gesture_detection.gesture import getGestureNumber
from src.database_operations.insert_form_details import insert_form_data
from src.aadhar_card_processing.aadhar_card import get_aadhar_card_details
from src.utility.logfile import DvalLogger

UPLOAD_FOLDER = os.path.join(os.getcwd(),"input_images")
# UPLOAD_FOLDER = os.getcwd() + "/src/input_images"
DATABASE_FAIL_FOLDER = os.path.join(os.getcwd(),"database/fail_cases")
DATABASE_PASS_FOLDER = os.path.join(os.getcwd(),"database/pass_cases")
# print("**************** : ",UPLOAD_FOLDER)
# UPLOAD_FOLDER = "../input_images"
# DATABASE_FAIL_FOLDER = "../database/fail_cases"
# DATABASE_PASS_FOLDER = "../database/pass_cases"

def verify_document_details(card_img,name,fname,dob,DNumber,mobile,email,address,document_type_value,aadhar_img):
    address = handle_multiple_spaces(address)
    _dval_logger = DvalLogger.get_instance()
    _dval_logger.log("Verifying document details",logging.INFO)
    primary_image_path = os.path.join(UPLOAD_FOLDER,"card.jpg")
    aadhar_image_path = os.path.join(UPLOAD_FOLDER,"aadhar.jpg")
    card_img[0].save(primary_image_path)

    if document_type_value == 'pan':
        aadhar_img[0].save(aadhar_image_path)
        aadhar_data = get_aadhar_card_details(aadhar_image_path)
        aadhar_details = aadhar_data['details']
        name_ocr,fname_ocr,pan_ocr,dob_ocr = ocr_panCard(primary_image_path,UPLOAD_FOLDER)

        # Making tuples of data
        data = {}
        data['Name'] = name_ocr
        data['Father Name'] = fname_ocr
        data['Date of Birth'] = dob_ocr
        data['Number'] = pan_ocr
        data['Address'] = aadhar_details['Address']
        ocr_status = validate_document_details(name,fname,dob,DNumber,mobile,email,address,data,primary_image_path)
        address_status,address_fileds_status =  verify_address(address,aadhar_details['Address'])

        if address_status == False:
            ocr_status = False

        if ocr_status:
            address_str = address_json_to_string(address)
            # insert_form_data(name, fname, dob, DNumber, mobile, email, address_str)
        return {'status': ocr_status,
                'address_status':address_status,
                'address_fileds_status':address_fileds_status,
                'details':data
                }

    elif document_type_value == 'aadhar':
        aadhar_data = get_aadhar_card_details(primary_image_path)
        aadhar_details = aadhar_data['details']
        ocr_status = validate_document_details(name,fname,dob,DNumber,mobile,email,address,aadhar_details,primary_image_path)
        address_status,address_fileds_status  =  verify_address(address,aadhar_details['Address'])

        if address_status == False:
            ocr_status = False

        if ocr_status:
            address_str = address_json_to_string(address)
            # insert_form_data(name, fname, dob, DNumber, mobile, email, address_str)
        return {'status': ocr_status,
                'address_status':address_status,
                'address_fileds_status':address_fileds_status,
                'details':aadhar_details
                }

def address_json_to_string(address):
    address_str = address['house'] + "," + address['street_locality'] +  "," + address['vtc'] + "," + address['dist'] + "," +\
					  address['state'] + "," + address['pc']
    return address_str


def handle_multiple_spaces(address):
    address['house'] = re.sub(' +', ' ', address['house'])
    address['street_locality'] = re.sub(' +', ' ', address['street_locality'])
    address['vtc'] = re.sub(' +', ' ', address['vtc'])
    address['dist'] = re.sub(' +', ' ', address['dist'])
    address['state'] = re.sub(' +', ' ', address['state'])
    address['pc'] = re.sub(' +', ' ', address['pc'])
    return address
    

def validate_document_details(name,fname,dob,DNumber,mobile,email,address,data,image_path):

    current_datetime = datetime.datetime.now()
    database_fail_path = os.path.join(DATABASE_FAIL_FOLDER, str(current_datetime)+"_card.jpg")
    database_pass_path = os.path.join(DATABASE_PASS_FOLDER, str(current_datetime)+"_card.jpg") 

    if name == data['Name'] and fname == data['Father Name'] and dob == data['Date of Birth'] and DNumber == data['Number']:
        ocr_status = True
        shutil.copy(image_path, database_pass_path)
    else:
        ocr_status = False
        shutil.copy(image_path, database_fail_path)

    return ocr_status

def verify_address(address,address_from_doc):

    address_fileds_status = {}
    address_fileds_status['house'] = False
    address_fileds_status['street_locality'] = False
    address_fileds_status['vtc'] = False
    address_fileds_status['state'] = False
    address_fileds_status['dist'] = False
    address_fileds_status['pc'] = False
    address_status = True
    street_locality_str = ''

    if address_from_doc.get("street"):
        street_locality_str += address_from_doc["street"]

    if address_from_doc.get("loc"):
        if street_locality_str != '':
            street_locality_str += ','
        street_locality_str += address_from_doc["loc"]

    if address_from_doc["house"].upper() == address["house"].upper():
        address_fileds_status['house'] = True
    else:
        address_status = False

    if address_from_doc["vtc"].upper() == address["vtc"].upper():
        address_fileds_status['vtc'] = True
    else:
        address_status = False

    if address_from_doc["state"].upper() == address["state"].upper():
        address_fileds_status['state'] = True

    else:
        address_status = False

    if address_from_doc["pc"].upper() == address["pc"].upper():
        address_fileds_status['pc'] = True

    else:
        address_status = False

    if address_from_doc["dist"].upper() == address["dist"].upper():
        address_fileds_status['dist'] = True

    else:
        address_status = False

    # if address_from_doc["house"].upper() == address["house"].upper() and address_from_doc["vtc"].upper() == address["vtc"].upper() \
    #      and address_from_doc["state"].upper() == address["state"].upper() and address_from_doc["pc"] == address["pc"]:
    #     address_status = True

    # else:
    #     address_status = False

    seq=difflib.SequenceMatcher(None, address["street_locality"],street_locality_str)
    distance=seq.ratio()*100
    
    if distance > 80:
        address_fileds_status['street_locality'] = True

    else:
        address_status = False

    # if address_status == True:
    #     if distance > 80:
    #         address_status = True
    #     else:
    #         address_status = False
    return address_status,address_fileds_status


def verify_gesture(liveImage,gesture_number):
    _dval_logger = DvalLogger.get_instance()
    _dval_logger.log("Gesture verification module is Processing",logging.INFO)
    pan_image_path = os.path.join(UPLOAD_FOLDER,"card.jpg")
    person_image_path = os.path.join(UPLOAD_FOLDER,"person.jpg")
    # uploaded_img2[0].save(pan_image_path)
    current_datetime = datetime.datetime.now()
    database_fail_path = os.path.join(DATABASE_FAIL_FOLDER, str(current_datetime) + "_person.jpg")
    database_pass_path = os.path.join(DATABASE_PASS_FOLDER, str(current_datetime) + "_person.jpg")
    liveImage[0].save(person_image_path)
    

    # gesture Identification
    identified_gesture_number = getGestureNumber(person_image_path)


    if str(identified_gesture_number) == gesture_number:
        gesture_status = True
        shutil.copy(person_image_path, database_pass_path)
    else:
        gesture_status = False
        shutil.copy(person_image_path, database_fail_path)

    # print("gesture number : ",gesture_number)
    # print("identified gesture number : ",identified_gesture_number)
    # print("gesture_status : ",gesture_status)
    
    _dval_logger.log("gesture number : "+str(gesture_number),logging.DEBUG)
    _dval_logger.log("identified gesture number : "+str(identified_gesture_number),logging.DEBUG)
    _dval_logger.log("gesture_status : "+str(gesture_status),logging.DEBUG)


    # face matching
    camera_pic = query_image_embeddings(person_image_path)
    pan_card  = query_image_embeddings(pan_image_path)
    if not pan_card :
        # print("No face found in uploaded card")
        _dval_logger.log("No face found in uploaded card",logging.INFO)
        distance = 0
    elif not camera_pic:
        # print("No face found in Live Image")
        _dval_logger.log("No face found in Live Image",logging.INFO)
        distance = 0
    else:
        distance = face_distance(camera_pic, pan_card)
    # print("CONFIDENCE SCORE ",distance)
    _dval_logger.log("CONFIDENCE SCORE : "+str(distance),logging.DEBUG)
    if distance>80:
        bool = True
    else:
        bool = False
    return {'status': bool,
            'gesture_status':gesture_status
            }


def verify_liveliness(uploaded_img1,video_status,eye_blink_count):
    _dval_logger = DvalLogger.get_instance()
    _dval_logger.log("Liveliness detection module is Processing",logging.INFO)
    videoPath = os.path.join(UPLOAD_FOLDER, 'demo.mp4')
    # with open(videoPath, 'wb') as destination:
    #     video_stream = request.files['recodedVideo'].read()
    #     destination.write(video_stream)

    current_datetime = datetime.datetime.now()
    database_fail_path = os.path.join(DATABASE_FAIL_FOLDER, str(current_datetime) + "_video.mp4")
    database_pass_path = os.path.join(DATABASE_PASS_FOLDER, str(current_datetime) + "_video.mp4")

    # print("^^^^^^^^^^^^^^^^^^^^^^^^^ ",flask.request.files['liveImage'])

    uploaded_img1 = flask.request.files.getlist("liveImage")
    # uploaded_img2 = flask.request.files.getlist("cardImage")
    pan_image_path = os.path.join(UPLOAD_FOLDER,"card.jpg")
    person_image_path = os.path.join(UPLOAD_FOLDER,"person.jpg")
    # uploaded_img2[0].save(pan_image_path)
    uploaded_img1[0].save(person_image_path)

    


    # video processing
    if video_status == True:
        blinks_identified = detectBlink(videoPath)
        if (blinks_identified-2) <= int(eye_blink_count) <= (blinks_identified+2) or blinks_identified >= 1:
            eye_blinks_status = True
            shutil.copy(videoPath, database_pass_path)
        else:
            eye_blinks_status = False
            shutil.copy(videoPath, database_fail_path)
    else:
        eye_blinks_status = False
        shutil.copy(videoPath, database_fail_path)

    # if blinks_identified >= 1 :
    #     eye_blinks_status = True
    # print("real : ",eye_blink_count)
    # print("Identified : ",blinks_identified)
    # print("eye_blinks_status : ",eye_blinks_status)
   
    _dval_logger.log("real : "+str(eye_blink_count),logging.DEBUG)
    _dval_logger.log("Identified : "+str(blinks_identified),logging.DEBUG)
    _dval_logger.log("eye_blinks_status : "+str(eye_blinks_status),logging.DEBUG)



    # face matching
    camera_pic = query_image_embeddings(person_image_path)
    pan_card  = query_image_embeddings(pan_image_path)
    if not pan_card :
        # print("No face found in uploaded card")
        _dval_logger.log("No face found in uploaded card",logging.INFO)
        distance = 0
    elif not camera_pic:
        # print("No face found in Live Image")
        _dval_logger.log("No face found in Live Image",logging.INFO)
        distance = 0
    else:
        distance = face_distance(camera_pic, pan_card)
    # print("CONFIDENCE SCORE ",distance)
    _dval_logger.log("CONFIDENCE SCORE : "+str(distance),logging.DEBUG)
    if distance>85:
        bool = True
    else:
        bool = False
    return {'status': bool,
            'eye_blink_status':eye_blinks_status
            
            }



def face_distance(face_encodings, face_to_compare):
    distances = []
    result = []
    """
    Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
    for each comparison face. The distance tells you how similar the faces are.

    :param faces: List of face encodings to compare
    :param face_to_compare: A face encoding to compare against
    :return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
    """
    # return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]
    if len(face_encodings) == 0:

        return np.empty((0))
    else:
        for face_encoding in face_encodings:
            result.append(np.linalg.norm(face_encoding - face_to_compare))

    for x in result:
        # print(x)
        distances.append((1 - math.pow(x, 2) / 2) * 100)
    distances = np.asarray(distances)
    distances = max(distances)
    return distances


def extract_text_from_image(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text

def query_image_embeddings(filename):
    image_to_check = os.path.join('saved_pictures/', filename)
    unknown_image = face_recognition.load_image_file(image_to_check)
    # Scale down image if it's giant so things run a little faster
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)
    # unknown face encodings
    basename = os.path.splitext(os.path.basename(image_to_check))[0]
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    _dval_logger = DvalLogger.get_instance()
    if len(unknown_encodings) > 1:
        # click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(basename))
        _dval_logger.log("WARNING: More than one face found in {}. Only considering the first face.".format(basename),logging.WARNING)
    if len(unknown_encodings) == 0:
        unknown_encodings = []
        # click.echo("WARNING: No faces found in {}. Ignoring file.".format(basename))
        _dval_logger.log("WARNING: No faces found in {}. Ignoring file.".format(basename),logging.WARNING)
        # sys.exit(" Exiting since no faces found")
    return unknown_encodings

