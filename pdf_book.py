import os
import cv2
import numpy as np

from glob import glob
from base import pdf

HEIGHT = 1200

def get_ratio(img):
    h, w = img.shape
    w = w/h
    h = 1
    return h, w

def calc_ratio(h_ratio, w_ratio):
    return int(HEIGHT * h_ratio), int(HEIGHT * w_ratio)

def remove_background(img):
    _, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    return cv2.add(img, threshold)

def histogram_compress(img):
    img = np.array(img/25, dtype=np.int) * 25
    img[img>235] = 255
    img = np.array(img, dtype=np.float32)
    return img

def resize(img):    
    height, width = calc_ratio(*get_ratio(img))
    return cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)

def image_to_page(path, save_path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    cleaned = remove_background(img)
    resized = resize(cleaned)    
    compressed = histogram_compress(resized)
    
    cv2.imwrite(save_path, compressed)

def get_jpg_path_list(path):
    filelist = []
    for filename in glob(os.path.join(path, "*.jpg")):
        filelist.append(filename)
    return filelist

def images_to_pages(path):
    path_list = get_jpg_path_list(path)
    for load_path in path_list:
        save_path = os.path.join("1_image2page", load_path).replace("jpg", "png")
        image_to_page(load_path, save_path)


path = os.path.join("art")
images_to_pages(path)


#load_path = "bb/0017.jpg"
#save_path = "result.jpg"
#page = image_to_page(load_path, save_path)




