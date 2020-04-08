import os
import os.path
import re
from PIL import Image
import cv2
import numpy as np

def image_processing(path,UPLOAD_FOLDER):
    new_path =set_dpi(path,UPLOAD_FOLDER)
    threshold_image_path = apply_threshold(new_path,UPLOAD_FOLDER)
    return threshold_image_path

def set_dpi(path,UPLOAD_FOLDER):
    # set dpi to (300,300)
    im = Image.open(path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    #     temp_file = '/home/anil/Downloads/panCards/gray.png'
    #     temp_filename = temp_file.name
    # new_path = '/home/anil/Machine_learning/e-KYC/input_images/card_dpi.png'
    new_path = os.path.join(UPLOAD_FOLDER,"card_dpi.png")
    im_resized.save(new_path, dpi=(300, 300))
    return new_path

def apply_threshold(path,UPLOAD_FOLDER):
    img = Image.open(path)
    img = img.convert('RGBA')
    pix = img.load()

    img_hsv = cv2.imread(path, cv2.COLOR_BGR2HSV)
    hue, sat, val = img_hsv[:, :, 0], img_hsv[:, :, 1], img_hsv[:, :, 2]
    mean = np.mean(img_hsv[:, :, 2])
    # print("value mean : ", mean)
    # threshold = int((mean * 85) / 155)
    # for y in range(img.size[1]):
    #     for x in range(img.size[0]):
    #         if pix[x, y][0] < threshold or pix[x, y][1] < threshold or pix[x, y][2] < threshold:
    #             pix[x, y] = (0, 0, 0, 255)
    #         else:
    #             pix[x, y] = (255, 255, 255, 255)


    if mean > 200:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 140 or pix[x, y][1] < 140 or pix[x, y][2] < 140:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
    
    elif 170 < mean <= 200:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 120 or pix[x, y][1] < 120 or pix[x, y][2] < 120:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
    
    elif 140 < mean <= 170:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 95 or pix[x, y][1] < 95 or pix[x, y][2] < 95:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
    
    elif 125 < mean <= 140:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 65 or pix[x, y][1] < 75 or pix[x, y][2] < 75:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
    elif 110 < mean <= 125:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 60 or pix[x, y][1] < 60 or pix[x, y][2] < 60:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
    else:
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 55 or pix[x, y][1] < 55 or pix[x, y][2] < 55:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
    # threshold_image_path = '/home/anil/Machine_learning/e-KYC/input_images/ocr_card.png'
    threshold_image_path = os.path.join(UPLOAD_FOLDER, "ocr_card.png")
    img.save(threshold_image_path)
    return threshold_image_path
