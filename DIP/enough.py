import cv2
import numpy as np

def remove_line(im):
    temp = im.copy()
    thresh = cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(temp, [c], -1, (255,255,255), 2)
    return temp


def handle(colorim, im):
    result = remove_line(im)
    # kernel = np.ones((3, 3), np.uint8) / 9
    # result = cv2.filter2D(result, -1, kernel)
    # CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(64, 64))
    result = clahe.apply(result)

    ret,thresh = cv2.threshold(result , 64, 255, cv2.THRESH_BINARY)

    # erode
    kernel = np.ones((8, 8), np.uint8)
    result = cv2.erode(thresh, kernel, iterations = 1)   
    # cv2.imshow('thresh', thresh)
    result = cv2.bitwise_or(im , result)

    thresh = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                    cv2.THRESH_BINARY, 9, 1)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 280 and cv2.contourArea(cnt) < 850:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 15 and w > 7:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow('im', image)
    cv2.waitKey()


image = cv2.imread('input.png')
# im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
im = cv2.imread('input.png', 0)
handle(image, im)