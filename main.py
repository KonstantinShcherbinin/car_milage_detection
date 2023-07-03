import os
import sys
from typing import List, Tuple
import numpy as np

import matplotlib.pyplot as plt
#import pytesseract
import cv2


def open_img(img_path):
    cardashboard_img = cv2.imread(img_path)
    cardashboard_img = cv2.cvtColor(cardashboard_img, cv2.COLOR_BGR2RGB)
    plt.imshow(cardashboard_img)
    plt.show()
    return cardashboard_img

def main(img_path):
    cardashboard_img_rgb = open_img(img_path)
    car_mileage_haar_cascade = cv2.CascadeClassifier()

if __name__ == '__main__':
    main(img_path)