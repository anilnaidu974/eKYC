import numpy as np
import cv2
from sklearn.externals import joblib
import argparse

def detect_face(img, faceCascade):
    faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(110, 110)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    return faces


def calc_hist(img):
    histogram = [0] * 3
    for j in range(3):
        histr = cv2.calcHist([img], [j], None, [256], [0, 256])
        histr *= 255.0 / histr.max()
        histogram[j] = histr
    return np.array(histogram)


def predict_spoof(path):

    img = cv2.imread(path)
    clf = None
    clf = joblib.load("/home/anil/Downloads/test.pkl")

    cascPath = "/home/anil/Machine_learning/e-KYC/spoof_detect/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detect_face(img_gray, faceCascade)
    print("No of faces : ",len(faces))
    # measures[count%sample_number]=0
    for i, (x, y, w, h) in enumerate(faces):

        roi = img[y:y+h, x:x+w]
        img_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
        img_luv = cv2.cvtColor(roi, cv2.COLOR_BGR2LUV)

        ycrcb_hist = calc_hist(img_ycrcb)
        luv_hist = calc_hist(img_luv)

        feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
        feature_vector = feature_vector.reshape(1, len(feature_vector))

        prediction = clf.predict_proba(feature_vector)
        prob = prediction[0][1]

        sample_number = 1
        count = 0
        measures = np.zeros(sample_number, dtype=np.float)

        measures[count % sample_number] = prob

        print(measures, np.mean(measures))
        text = "True"
        if 0 not in measures:
            if np.mean(measures) >= 0.7:
                text = "False"
                
        print("Status: ",text)

    return text
    