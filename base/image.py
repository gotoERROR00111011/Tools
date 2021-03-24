import cv2
from matplotlib import pyplot as plt

def show_image(img):
    cv2.imshow("Window", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_image(path, mode=cv2.IMREAD_COLOR):
    return cv2.imread(path, mode)

def save_image(path, img):
    cv2.imwrite(path, img)

def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresholding(img, tresh, value=255, mode=cv2.THRESH_BINARY):
    _, threshold = cv2.threshold(img, tresh, value, mode)
    return threshold

def masking(img, mask):
    return cv2.bitwise_and(img, mask)

def add(img1, img2):
    return cv2.add(img1, img2)

def diff(img1, img2):
    return cv2.absdiff(img1, img2)

def resize(img, height, width):
    return cv2.resize(img, dsize=(width, height), interpolation=cv2.INTER_AREA)
    #return cv2.resize(img, dsize=(0, 0), fx=0.3, fy=0.7, interpolation=cv2.INTER_AREA)

def resize_height(img, height):
    h, w, _ = img.shape
    w = int(height * w/h)
    h = height
    return resize(img, h, w)

def to_clear_png(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    return np.dstack((page, alpha))

def get_histogram(img):
    plt.hist(img.ravel(), 256, [0,256]); 
    plt.show()


