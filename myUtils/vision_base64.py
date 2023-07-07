import base64
import os
import cv2
from PIL import Image



def encode_save_img(file_path):
    file_name = os.path.basename(file_path)
    img_enc_path = ''.join([
        os.path.dirname(file_path),
        '\\',
        os.path.splitext(file_name)[0],
        '.base64'
    ])
    #with open(file_path, 'r', encoding='utf-8') as f:
    #    img = Image.open(f)
    img = cv2.imread(file_path)
    img_enc = base64.b64encode(img)
    img_enc.save(img_enc_path)
    return img_enc_path

def encode_img(file_path):
    img = cv2.imread(file_path)
    return base64.b64encode(img)