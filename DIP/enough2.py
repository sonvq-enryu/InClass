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

im = cv2.imread('input.png', 0)

result = remove_line(im)

thresh = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 217, -1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
result = cv2.dilate(thresh, kernel, iterations=1)
cv2.imshow('t', result)
result = cv2.bitwise_or(result, thresh)
ret, thresh_2 = cv2.threshold(result, 64, 255, cv2.THRESH_BINARY)
cv2.imshow('thresh', result)
cv2.waitKey()