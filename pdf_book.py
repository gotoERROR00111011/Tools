"""
workflow
1. pdf to images
2. convert image gray
3. convert image gray
4. handwork (select color or grayscale image)
5. images to pdf
"""

import os
import cv2
import numpy as np

from glob import glob

from base.pdf import *
from base.path import *

HEIGHT = 1200

def get_ratio(img):
    h, w = (img.shape[0], img.shape[1])
    w = w/h
    h = 1
    return h, w

def remove_background(img):
    _, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    return cv2.add(img, threshold)

def histogram_compress(img):
    img = np.array(img/25, dtype=np.int) * 25
    img[img>235] = 255
    img = np.array(img, dtype=np.float32)
    return img

def resize(img):
    h, w = get_ratio(img)
    h = int(HEIGHT * h)
    w = int(HEIGHT * w)
    return cv2.resize(img, dsize=(w, h), interpolation=cv2.INTER_AREA)

def copy_dirs(src_path, trg_path):  
    dir_list = get_dirs(src_path)
    for d in dir_list:
        mkdir(d.replace(src_path, trg_path))

def imwrite(trg_path, img):
    #한국어 경로 해결
    extension = os.path.splitext(trg_path)[1] 
    result, encoded_img = cv2.imencode(extension, img)
    with open(trg_path, mode='w+b') as f:
        encoded_img.tofile(f)

def convert_page(src_path, trg_path):
    ff = np.fromfile(src_path, np.uint8)
    img = cv2.imdecode(ff, cv2.IMREAD_GRAYSCALE)

    cleaned = remove_background(img)
    resized = resize(cleaned)
    compressed = histogram_compress(resized)
    
    imwrite(trg_path, compressed)

def convert_page_color(src_path, trg_path):
    ff = np.fromfile(src_path, np.uint8)
    img = cv2.imdecode(ff, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
    img = cv2.add(img, threshold)

    resized = resize(img)
    
    imwrite(trg_path, resized)


if __name__ == "__main__":
    mode = ""
    #mode = "pdf to images"
    #mode = "convert image gray"
    #mode = "convert image color"
    #mode = "수작업 - gray or color, 손가락 지우기"
    #mode = "images to pdf"

    if mode == "pdf to images":
        src_path = "0_original"
        trg_path = "1_pdf_to_images"
        dirs = get_dirs(src_path)

        copy_dirs(src_path, trg_path)
        pdfs = []
        for d in dirs:
            for f in get_files(d, "*.pdf"):
                pdfs.append(f)

        for pdf in pdfs:
            trg_dir = pdf.replace(src_path, trg_path)
            trg_dir = trg_dir.replace(".pdf", "")
            mkdir(trg_dir)
            pdf_to_images(pdf, trg_dir)
    

    if mode == "convert image gray":
        src_path = "1_pdf_to_images"
        trg_path = "2_convert_gray"
        dirs = get_dirs(src_path)

        copy_dirs(src_path, trg_path)
        images = []
        for d in dirs:
            for f in get_files(d, "*.png"):
                images.append(f)
        
        for image in images:
            trg = image.replace(src_path, trg_path)
            convert_page(image, trg)

    
    if mode == "convert image color":
        src_path = "1_pdf_to_images"
        trg_path = "3_convert_color"
        dirs = get_dirs(src_path)

        copy_dirs(src_path, trg_path)
        images = []
        for d in dirs:
            for f in get_files(d, "*.png"):
                images.append(f)
        
        for image in images:
            trg = image.replace(src_path, trg_path)
            convert_page_color(image, trg)
        
    if mode == "images to pdf":
        src_path = "2_convert_gray"
        trg_path = "4_images_to_pdf"
        dirs = get_dirs(src_path)

        copy_dirs(src_path, trg_path)
        
        for d in dirs:
            images = get_files(d, "*.png")
            if len(images) > 0:
                trg = d.replace(src_path, trg_path) + ".pdf"
                images_to_pdf(images, trg)

