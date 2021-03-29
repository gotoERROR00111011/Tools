"""
workflow
1. pdf to images
2. convert image gray
3. convert image color
4. handwork (select color or grayscale image)
5. images to pdf
6. 이 코드는 grayscale png -> pdf -> png 변환은 실패한다.
   변환해야 한다면 LibreOffice Draw -> 내보내기 -> HTML 을 사용하면 된다.
"""

import os
import cv2
import numpy as np

from base.pdf import *
from base.path import *

def get_ratio(img):
    h, w = (img.shape[0], img.shape[1])
    w = w/h
    h = 1
    return h, w

def remove_background(img):
    if len(img.shape)==2:
        _, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
    img = cv2.add(img, threshold)
    return img

def histogram_compress(img):
    img = np.array(img/25, dtype=np.int) * 25
    img[img > 235] = 255
    img = np.array(img, dtype=np.float32)
    return img

def resize(img, height=1200):
    h, w = get_ratio(img)
    h = int(height * h)
    w = int(height * w)
    return cv2.resize(img, dsize=(w, h), interpolation=cv2.INTER_AREA)

def imwrite(trg_path, img):
    #한국어 경로 문제 처리
    extension = os.path.splitext(trg_path)[1]
    result, encoded_img = cv2.imencode(extension, img)
    with open(trg_path, mode='w+b') as f:
        encoded_img.tofile(f)

def convert_page(src_path, mode):
    ff = np.fromfile(src_path, np.uint8)
    img = cv2.imdecode(ff, mode)
    img = remove_background(img)
    return resize(img)

def get_all_paths(src_path, trg_path, extension):
    files = []
    for d in get_dirs(src_path):
        mkdir(d.replace(src_path, trg_path))
        for f in get_files(d, extension):
            files.append(f)
    return files
    

if __name__ == "__main__":
    mode = ["0_original", "1_pdf_to_images", "2_convert_gray", "3_convert_color", "4_images_to_pdf"]
    select = 1

    if mode[select] == "1_pdf_to_images":
        src_path = mode[0]
        trg_path = mode[1]
        pdfs = get_all_paths(src_path, trg_path, "*.pdf")

        for pdf in pdfs:
            trg_dir = pdf.replace(src_path, trg_path)
            trg_dir = trg_dir.replace(".pdf", "")
            mkdir(trg_dir)
            pdf_to_images(pdf, trg_dir)
    

    if mode[select] == "2_convert_gray":
        src_path = mode[1]
        trg_path = mode[2]
        images = get_all_paths(src_path, trg_path, "*.png")
        
        for image in images:
            trg = image.replace(src_path, trg_path)
            img = convert_page(image, cv2.IMREAD_GRAYSCALE)
            img = histogram_compress(img)
            imwrite(trg, img)

    
    if mode[select] == "3_convert_color":
        src_path = mode[1]
        trg_path = mode[3]
        images = get_all_paths(src_path, trg_path, "*.png")
        
        for image in images:
            trg = image.replace(src_path, trg_path)
            img = convert_page(image, cv2.IMREAD_COLOR)
            imwrite(trg, img)
        
    
    if mode[select] == "4_images_to_pdf":
        src_path = mode[2]
        trg_path = mode[4]
        dirs = get_dirs(src_path)

        for d in dirs:
            mkdir(d.replace(src_path, trg_path))
            images = get_files(d, "*.png")
            if len(images) > 0:
                trg = d.replace(src_path, trg_path) + ".pdf"
                images_to_pdf(images, trg)
