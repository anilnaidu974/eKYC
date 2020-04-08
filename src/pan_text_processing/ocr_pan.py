#!/usr/bin/env python
import os
import os.path
import json
import sys
import pytesseract
import re
import difflib
import csv
from PIL import Image
import cv2
import numpy as np
import logging

from src.pan_text_processing.image_preprocessing import image_processing
from src.pan_text_processing.text_preprocessing import remove_unordeded_text
from src.pan_text_processing.details_cleaning import cleaning_pan_details
from src.pan_text_processing.details_from_new_panType import get_details_for_newPanType
from src.pan_text_processing.details_from_old_panType import get_details_from_old_pan
from src.utility.logfile import DvalLogger



# path = sys.argv[1]
# path = "/home/anil/Downloads/panCards/raghu.jpg"

name = None
fname = None
dob = None
pan = None
nameline = []
dobline = []
panline = []
text0 = []
ordered_text = []
text2 = []

# govRE_str = '(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT\
#              |PARTMENT|ARTMENT|INDIA|NDIA|TAX|DEPART)$'
govRE_str = '(DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|TAX|DEPART)$'

numRE_str = '(Number|umber|Account|ccount|count|Permanent|\
             ermanent|manent)$'
fatherRE_str = '(Father|father|Fathers|Name)$'
dobRE_str = '(Date of Birth|Date|Birth)$'



def ocr_panCard(pan_image_path,UPLOAD_FOLDER):

    path = pan_image_path
    threshold_image_path = image_processing(path,UPLOAD_FOLDER)

    text = extract_text_from_threshold_image(threshold_image_path)

    if text == '':
        return False,False,False,False
    else:
        ordered_text = remove_unordeded_text(text)

        # print("Ordered text : ", ordered_text)
        panType = check_pan_type(ordered_text)
        # print("panType : ", panType)
        _dval_logger = DvalLogger.get_instance()
        _dval_logger.log("panType : "+str(panType),logging.DEBUG)

        if panType == "new":
            name,fname,pan,dob = get_details_for_newPanType(ordered_text,numRE_str,fatherRE_str,dobRE_str)
        else:
            name,fname,pan,dob = get_details_from_old_pan(ordered_text,govRE_str,numRE_str)



        name, fname, pan, dob = cleaning_pan_details(name,fname,pan,dob)

        # print("+++++++++++++++++++++++++++++++")
        # print("Name : ",name)
        # print("-------------------------------")
        # print("Father Name : ",fname)
        # print ("-------------------------------")
        # print("Date of Birth : ",dob)
        # print("-------------------------------")
        # print("PAN : ",pan)
        # print("-------------------------------")
        _dval_logger.log("+++++++++++++++++++++++++++++++",logging.DEBUG)
        _dval_logger.log("Name : "+str(name),logging.DEBUG)
        _dval_logger.log("-------------------------------",logging.DEBUG)
        _dval_logger.log("Father Name : "+str(fname),logging.DEBUG)
        _dval_logger.log("-------------------------------",logging.DEBUG)
        _dval_logger.log("Date of Birth : "+str(dob),logging.DEBUG)
        _dval_logger.log("-------------------------------",logging.DEBUG)
        _dval_logger.log("PAN : "+str(pan),logging.DEBUG)
        _dval_logger.log("-------------------------------",logging.DEBUG)

        return name,fname,pan,dob


def extract_text_from_threshold_image(threshold_image_path):
    text = pytesseract.image_to_string(Image.open(threshold_image_path))
    return text

def check_pan_type(ordered_text):

    panType = "old"
    for wordline in ordered_text:
        xx = wordline.split()
        if [w for w in xx if re.search(fatherRE_str, w)]:
            panType = "new"
    return panType

