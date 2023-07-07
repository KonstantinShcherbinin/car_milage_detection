import os
import sys
#sys.path.append('C:\\Users\\shers\\car_milage_detection\\yolov5')
#from ultralytics.yolo.utils.checks import check_requirements
from typing import List, Tuple
import numpy as np


import matplotlib.pyplot as plt
import pytesseract
import cv2

from myUtils.img_rotation import get_rotated
from aimodels.yolo import ModelLoader
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\shers\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

YOLO_ROTATE = 'model_weights/work_yolo_sts_rotate.pt'

def open_img(img_path):
    cardashboard_img = cv2.imread(img_path)
    cardashboard_img = cv2.cvtColor(cardashboard_img, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(cardashboard_img, 100, 140, cv2.THRESH_BINARY)
    blackAndWhiteImage_bit = cv2.bitwise_not(blackAndWhiteImage)
    plt.imshow(blackAndWhiteImage)
    plt.show()
    print(pytesseract.image_to_string(blackAndWhiteImage))
    #print(pytesseract.image_to_string(cardashboard_img, lang='rus'))
    #return cardashboard_img

def main(img_path):
    cardashboard_img_rgb = open_img(img_path)
    #rot_model_processor = ModelLoader(weights=YOLO_ROTATE)
    #get_rotated(cardashboard_img_rgb, rot_model_processor)
    #car_mileage_haar_cascade = cv2.CascadeClassifier()

if __name__ == '__main__':
    main('C:\\Users\\shers\\car_milage_detection\\data\\autoservice_priem_305_1388952_13.jpg')