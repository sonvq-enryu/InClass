import cv2
import os
import numpy as np

def remove_line(im):
    rev = im.copy()
    thresh = cv2.threshold(rev, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(rev, [c], -1, (255,255,255), 2)
    return rev

def top(im):
    boxes = []
    thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                    cv2.THRESH_BINARY, 3, 1)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            if w > 10 and w < 40 and h > 35 and h < 70 and y < 200: # control box in top half image and control number of box
                boxes += [((x, y), (x+w, y+h))]
    return boxes


def line4(im):
    boxes = []
    _, thresh = cv2.threshold(im, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2, 2), np.uint8)
    im = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                    cv2.THRESH_BINARY, 5, 1)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 195 and y < 270:
                boxes += [((x, y), (x+w, y+h))]
    return boxes

def line5(im):
    boxes = []

    thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                    cv2.THRESH_BINARY, 5, 1)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 265 and y < 325 and x < 165:
                boxes += [((x, y), (x+w, y+h))]

    blur = cv2.GaussianBlur(im, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 45, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 265 and y < 325 and x > 165:
                boxes += [((x, y), (x+w, y+h))]

    return boxes

def line6(im):
    boxes = []
    _, thresh = cv2.threshold(im, 50, 255, cv2.THRESH_BINARY)
    blur = cv2.GaussianBlur(thresh, (13, 13), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                    cv2.THRESH_BINARY, 7, 8)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 250 and cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if w > 10 and w < 40 and h > 35 and h < 70 and y > 325:
                boxes += [((x, y), (x+w, y+h))]
    return boxes

if __name__ == "__main__":
    im = cv2.imread("./last/image.png")
    gray = remove_line(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    boxes = []
    boxes += top(gray)
    boxes += line4(gray)
    boxes += line5(gray)
    boxes += line6(gray)
    for i, (x, y) in enumerate(boxes):
        cv2.rectangle(im, x, y, (0, 0, 255), 2)
    cv2.imshow('result', im)
    cv2.imwrite('boundingbox.png', im)
    cv2.waitKey()
