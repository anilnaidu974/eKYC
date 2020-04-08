from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2

import flask
from src.utility.logfile import DvalLogger
from imutils.video import FileVideoStream
import numpy as np
import os
import logging


def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear


def detectBlink(video):


    # thresh = 0.25
    thresh = 0.20
    total_blinks = 0
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("src/liveliness_detection/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
    # cap=cv2.VideoCapture(0)
    flag=0

    # start the video stream thread
    # print("[INFO] starting video stream thread...")
    _dval_logger = DvalLogger.get_instance()
    _dval_logger.log("[INFO] starting video stream thread...",logging.INFO)
    cap = FileVideoStream(video).start()
    fileStream = True

    while True:

        if fileStream and not cap.more():
            break

        frame=cap.read()

        if frame is not None:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            for subject in subjects:
                shape = predict(gray, subject)
                shape = face_utils.shape_to_np(shape)#converting to NumPy Array
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                # ear = (leftEAR + rightEAR) / 2.0
                ear = max(leftEAR,rightEAR)
                # print("leftEAR : ",leftEAR)
                # print("rightEAR : ",rightEAR)
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                if ear < thresh:
                    flag += 1
                else:
                    if flag >= 2:
                        total_blinks += 1
                    flag = 0
   

    _dval_logger.log("Eye blinks detected : "+str(total_blinks),logging.INFO)
    return total_blinks





########################################################################################################################
